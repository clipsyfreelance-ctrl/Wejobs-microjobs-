path = "src/components/AuthModals.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """          {/* Quick Demo Credentials Info */}
          <div className="mt-4 p-2.5 rounded-lg bg-neutral-100 dark:bg-neutral-800/80 text-[11px] text-neutral-500 dark:text-neutral-400 flex items-center justify-between">
            <span>Demo Member:</span>
            <button
              type="button"
              onClick={() => {
                setLoginEmail('alex.writer@wejobs.com');
                setLoginPassword('wejobs123');
              }}
              className="text-orange-600 dark:text-orange-400 font-semibold hover:underline cursor-pointer"
            >
              Auto-Fill (alex.writer@wejobs.com)
            </button>
          </div>

"""

if old in content:
    content = content.replace(old, "", 1)
    print("[OK] Blok Demo Member berhasil dihapus.")
else:
    print("[GAGAL] Pattern tidak ketemu, cek manual.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

