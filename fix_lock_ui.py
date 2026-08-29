path = "src/components/TaskDetailPage.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Tambah variabel isLocked setelah isFull
old_var = "  const isFull = task.remainingSlots <= 0 || task.status === 'full';"
new_var = old_var + "\n  const needsVerification = !!user && user.recipientStatus !== 'verified';"
if old_var in content:
    content = content.replace(old_var, new_var, 1)
    print("[OK] Variabel needsVerification ditambahkan.")
else:
    print("[GAGAL] Baris isFull tidak ketemu.")

# 2. Ganti tombol supaya kondisinya mencakup needsVerification
old_button = """            {!claimSuccess && (
              <button
                type="button"
                disabled={isFull || claiming}
                onClick={handleClaim}
                className={`w-full sm:w-auto px-8 py-2.5 rounded-xl font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer ${
                  isFull
                    ? 'bg-neutral-300 dark:bg-neutral-800 text-neutral-500 cursor-not-allowed'
                    : 'bg-orange-500 hover:bg-orange-600 text-white shadow-orange-500/25'
                }`}
              >
                {claiming ? (
                  <span>Reserving Slot...</span>
                ) : isFull ? (
                  <span>Task Full</span>
                ) : user ? (
                  <span>Take Job & Claim Slot (${task.payment.toFixed(2)} USD)</span>
                ) : (
                  <span>Sign In to Take Job</span>
                )}
              </button>
            )}"""

new_button = """            {!claimSuccess && (
              <button
                type="button"
                disabled={isFull || claiming || needsVerification}
                onClick={handleClaim}
                className={`w-full sm:w-auto px-8 py-2.5 rounded-xl font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer ${
                  isFull || needsVerification
                    ? 'bg-neutral-300 dark:bg-neutral-800 text-neutral-500 cursor-not-allowed'
                    : 'bg-orange-500 hover:bg-orange-600 text-white shadow-orange-500/25'
                }`}
              >
                {claiming ? (
                  <span>Reserving Slot...</span>
                ) : isFull ? (
                  <span>Task Full</span>
                ) : needsVerification ? (
                  <span>🔒 Verifikasi Akun Diperlukan</span>
                ) : user ? (
                  <span>Take Job & Claim Slot (${task.payment.toFixed(2)} USD)</span>
                ) : (
                  <span>Sign In to Take Job</span>
                )}
              </button>
            )}"""

if old_button in content:
    content = content.replace(old_button, new_button, 1)
    print("[OK] Tombol berhasil diupdate.")
else:
    print("[GAGAL] Blok tombol tidak ketemu.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
