import re

path = "src/components/PaymentVerificationManager.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Tambah import Firebase setelah import lucide-react
old_import = "} from 'lucide-react';"
new_import = old_import + """
import { db } from '../firebase';
import { collection, addDoc, doc, updateDoc, getDocs, query, where } from 'firebase/firestore';"""
content = content.replace(old_import, new_import, 1)

def replace_function(content, func_name, new_body, label):
    pattern = re.compile(
        r"const " + func_name + r" = async \([^)]*\) => \{.*?\n  \};",
        re.DOTALL
    )
    new_content, count = pattern.subn(new_body, content, count=1)
    if count == 1:
        print(f"[OK] {label} berhasil diganti.")
    else:
        print(f"[GAGAL] {label} TIDAK ditemukan/diganti. Cek manual!")
    return new_content

# 2. Ganti fetchVerifications
new_fetch = """const fetchVerifications = async () => {
    setLoadingVerifications(true);
    try {
      const q = query(
        collection(db, 'paymentVerifications'),
        where('userId', '==', user.id)
      );
      const snap = await getDocs(q);
      const list: PaymentAccountVerification[] = snap.docs.map((d) => ({ id: d.id, ...(d.data() as any) }));
      list.sort((a, b) => (b.requestedAt || '').localeCompare(a.requestedAt || ''));
      setVerifications(list);
    } catch (err) {
      console.warn('Failed to load payment verifications', err);
    } finally {
      setLoadingVerifications(false);
    }
  };"""
content = replace_function(content, "fetchVerifications", new_fetch, "fetchVerifications")

# 3. Ganti handleRequestEligibility
new_eligibility = """const handleRequestEligibility = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittingEligibility(true);
    try {
      await updateDoc(doc(db, 'users', user.id), {
        payoutEligibilityStatus: 'pending',
        payoutEligibilityNote: eligibilityReason,
        payoutEligibilityRequestedAt: new Date().toISOString(),
      });

      setEligibilityStatus('pending');
      setEligibilityModalOpen(false);
      setEligibilityReason('');
      showToast('success', '✅ Pengajuan verifikasi kelayakan berhasil dikirim! Menunggu konfirmasi Super Admin.');
      if (onRefreshUserData) await onRefreshUserData();
    } catch (err: any) {
      showToast('error', err.message || 'Terjadi kesalahan saat mengajukan kelayakan.');
    } finally {
      setSubmittingEligibility(false);
    }
  };"""
content = replace_function(content, "handleRequestEligibility", new_eligibility, "handleRequestEligibility")

# 4. Ganti handleSubmitAccountVerification
new_submit = """const handleSubmitAccountVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedChannel) return;

    if (!accountHolderName.trim()) {
      setFormError('Nama pemilik rekening wajib diisi sesuai identitas terdaftar.');
      return;
    }

    if (!accountNumber.trim()) {
      setFormError('Nomor rekening / nomor handphone e-wallet wajib diisi.');
      return;
    }

    setSubmittingVerification(true);
    setFormError(null);

    try {
      await addDoc(collection(db, 'paymentVerifications'), {
        userId: user.id,
        userEmail: user.email,
        userName: user.fullName,
        bankCode: selectedChannel.code,
        bankName: selectedChannel.name,
        channelStatus: selectedChannel.status,
        channelNote: selectedChannel.description,
        accountHolderName: accountHolderName.trim(),
        accountNumber: accountNumber.trim(),
        proofUrl: proofFile?.url || '',
        proofFileName: proofFile?.name || '',
        userNotes: userNotes.trim(),
        status: 'pending',
        requestedAt: new Date().toISOString(),
      });

      setVerificationModalOpen(false);
      setSelectedChannel(null);
      await fetchVerifications();
      if (onRefreshUserData) await onRefreshUserData();
      showToast(
        'success',
        `✅ Pengajuan verifikasi ${selectedChannel.name} berhasil dikirim! Menunggu konfirmasi Super Admin.`
      );
    } catch (err: any) {
      setFormError(err.message || 'Terjadi kesalahan saat memverifikasi rekening.');
    } finally {
      setSubmittingVerification(false);
    }
  };"""
content = replace_function(content, "handleSubmitAccountVerification", new_submit, "handleSubmitAccountVerification")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Selesai.")
