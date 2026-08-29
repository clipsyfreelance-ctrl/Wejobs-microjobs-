import re

path = "src/components/AdminDashboard.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Tambah import Firebase — cari baris import types lalu tambah di bawahnya
marker = "  PaymentAccountVerification,"
if marker in content and "from '../firebase'" not in content:
    content = content.replace(
        marker,
        marker + "\n} from '../types';\nimport { db } from '../firebase';\nimport {\n  collection, query, where, getDocs, doc, updateDoc,\n} from 'firebase/firestore';\n// __PLACEHOLDER_CLOSE__",
        1
    )
    # Perbaiki penutup import asli yang mungkin ganda — hapus duplikat "} from '../types';" yang lama
    content = content.replace("// __PLACEHOLDER_CLOSE__\n", "", 1)

def replace_function(content, func_name, new_body, label):
    pattern = re.compile(
        r"const " + func_name + r" = async \([^)]*\) => \{.*?\n  \};",
        re.DOTALL
    )
    new_content, count = pattern.subn(lambda m: new_body, content, count=1)
    if count == 1:
        print(f"[OK] {label} berhasil diganti.")
    else:
        print(f"[GAGAL] {label} TIDAK ditemukan/diganti. Cek manual!")
    return new_content

# 2. Ganti fetchAdminVerificationData
new_fetch = """const fetchAdminVerificationData = async () => {
    try {
      setLoadingEligibility(true);
      const usersSnap = await getDocs(
        query(collection(db, 'users'), where('payoutEligibilityStatus', '==', 'pending'))
      );
      const eligList: any[] = usersSnap.docs.map((d) => {
        const u: any = d.data();
        return {
          id: d.id,
          userId: d.id,
          userEmail: u.email,
          userName: u.fullName,
          userBalance: u.availableBalance || 0,
          completedJobsCount: u.completedJobsCount || 0,
          reason: u.payoutEligibilityNote || '',
          status: 'pending',
          requestedAt: u.payoutEligibilityRequestedAt || '',
        };
      });
      setEligibilityRequests(eligList);
      setLoadingEligibility(false);

      setLoadingPaymentVerifications(true);
      const pVerSnap = await getDocs(
        query(collection(db, 'paymentVerifications'), where('status', '==', 'pending'))
      );
      const pVerList: any[] = pVerSnap.docs.map((d) => ({ id: d.id, ...(d.data() as any) }));
      setPaymentVerifications(pVerList);
      setLoadingPaymentVerifications(false);
    } catch (err) {
      console.warn('Failed to load admin verifications data', err);
    } finally {
      setLoadingEligibility(false);
      setLoadingPaymentVerifications(false);
    }
  };"""
content = replace_function(content, "fetchAdminVerificationData", new_fetch, "fetchAdminVerificationData")

# 3. Ganti handleReviewEligibilityAction
new_elig_action = """const handleReviewEligibilityAction = async (action: 'approve' | 'reject') => {
    if (!selectedEligibility) return;
    setProcessingEligibility(true);
    try {
      await updateDoc(doc(db, 'users', selectedEligibility.userId), {
        payoutEligibilityStatus: action === 'approve' ? 'eligible' : 'rejected',
        payoutEligibilityNote: eligibilityFeedback || (action === 'approve' ? 'Memenuhi kelayakan penarikan dana.' : 'Pengajuan belum memenuhi syarat kelayakan.'),
        payoutEligibilityReviewedAt: new Date().toISOString(),
      });
      setSelectedEligibility(null);
      setEligibilityFeedback('');
      await fetchAdminVerificationData();
    } catch (err: any) {
      alert(err.message || 'Terjadi kesalahan sistem.');
    } finally {
      setProcessingEligibility(false);
    }
  };"""
content = replace_function(content, "handleReviewEligibilityAction", new_elig_action, "handleReviewEligibilityAction")

# 4. Ganti handleReviewPaymentVerificationAction
new_payver_action = """const handleReviewPaymentVerificationAction = async (action: 'approve' | 'reject') => {
    if (!selectedPaymentVerification) return;
    setProcessingPaymentVerification(true);
    try {
      await updateDoc(doc(db, 'paymentVerifications', selectedPaymentVerification.id), {
        status: action === 'approve' ? 'verified' : 'rejected',
        adminFeedback: verificationFeedback || (action === 'approve' ? 'Rekening telah diverifikasi dan aktif.' : 'Data rekening tidak sesuai dengan identitas terdaftar.'),
        reviewedAt: new Date().toISOString(),
      });
      if (action === 'approve') {
        await updateDoc(doc(db, 'users', selectedPaymentVerification.userId), {
          recipientStatus: 'verified',
        });
      }
      setSelectedPaymentVerification(null);
      setVerificationFeedback('');
      await fetchAdminVerificationData();
    } catch (err: any) {
      alert(err.message || 'Terjadi kesalahan sistem.');
    } finally {
      setProcessingPaymentVerification(false);
    }
  };"""
content = replace_function(content, "handleReviewPaymentVerificationAction", new_payver_action, "handleReviewPaymentVerificationAction")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Selesai.")
