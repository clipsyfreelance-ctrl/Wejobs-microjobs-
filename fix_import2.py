path = "src/components/AdminDashboard.tsx"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Cari baris index yang mengandung fragment kunci
new_lines = []
skip_mode = False
firebase_block = []
inserted = False

i = 0
while i < len(lines):
    line = lines[i]
    if "PaymentAccountVerification," in line:
        new_lines.append(line)
        new_lines.append("  PAYMENT_CHANNELS,\n")
        new_lines.append("  getPaymentChannelByCode,\n")
        new_lines.append("} from '../types';\n")
        new_lines.append("import { db } from '../firebase';\n")
        new_lines.append("import {\n")
        new_lines.append("  collection, query, where, getDocs, doc, updateDoc,\n")
        new_lines.append("} from 'firebase/firestore';\n")
        i += 1
        # Lewati baris-baris lama sampai ketemu "import { AvatarDisplay }"
        while i < len(lines) and "import { AvatarDisplay }" not in lines[i]:
            i += 1
        inserted = True
        continue
    new_lines.append(line)
    i += 1

if inserted:
    print("[OK] Import berhasil disusun ulang.")
else:
    print("[GAGAL] Marker 'PaymentAccountVerification,' tidak ditemukan.")

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
