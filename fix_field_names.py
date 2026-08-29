path = "src/components/AdminDashboard.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """      const eligList: any[] = usersSnap.docs.map((d) => {
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
      });"""

new = """      const eligList: any[] = usersSnap.docs.map((d) => {
        const u: any = d.data();
        return {
          id: d.id,
          userId: d.id,
          userEmail: u.email,
          userName: u.fullName,
          currentBalance: u.availableBalance || 0,
          completedJobsCount: u.completedJobsCount || 0,
          reason: u.payoutEligibilityNote || '',
          status: 'pending',
          createdAt: u.payoutEligibilityRequestedAt || new Date().toISOString(),
        };
      });"""

if old in content:
    content = content.replace(old, new, 1)
    print("[OK] Nama field eligibility berhasil disesuaikan.")
else:
    print("[GAGAL] Pattern tidak ketemu, cek manual.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
