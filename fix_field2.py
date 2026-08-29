path = "src/components/AdminDashboard.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """      const pVerList: any[] = pVerSnap.docs.map((d) => ({ id: d.id, ...(d.data() as any) }));"""

new = """      const pVerList: any[] = pVerSnap.docs.map((d) => {
        const data: any = d.data();
        return { id: d.id, ...data, submittedAt: data.requestedAt };
      });"""

if old in content:
    content = content.replace(old, new, 1)
    print("[OK] Field submittedAt berhasil ditambahkan sebagai alias.")
else:
    print("[GAGAL] Pattern tidak ketemu, cek manual.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
