path = "src/components/TaskDetailPage.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """  const handleClaim = async () => {
    if (!user) {
      onOpenLogin();
      return;
    }

    setClaiming(true);
    setClaimError(null);
    try {
      const success = await onClaimTask(task.id);
      if (success) {
        setClaimSuccess(true);
      }
    } catch (err: any) {
      setClaimError(err.message || 'Failed to claim task.');
    } finally {
      setClaiming(false);
    }
  };"""

new = """  const handleClaim = async () => {
    if (!user) {
      onOpenLogin();
      return;
    }

    if (user.recipientStatus !== 'verified') {
      setClaimError('Silakan verifikasi akun pembayaran Anda terlebih dahulu sebelum mengerjakan tugas.');
      return;
    }

    setClaiming(true);
    setClaimError(null);
    try {
      const success = await onClaimTask(task.id);
      if (success) {
        setClaimSuccess(true);
      }
    } catch (err: any) {
      setClaimError(err.message || 'Failed to claim task.');
    } finally {
      setClaiming(false);
    }
  };"""

if old in content:
    content = content.replace(old, new, 1)
    print("[OK] handleClaim berhasil ditambah pengecekan verifikasi.")
else:
    print("[GAGAL] Pattern tidak ketemu, cek manual.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
