path = "src/components/AdminDashboard.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

broken = """  PaymentAccountVerification,
} from '../types';
import { db } from '../firebase';
import {
  collection, query, where, getDocs, doc, updateDoc,
} from 'firebase/firestore';
PAYMENT_CHANNELS,
  getPaymentChannelByCode,
} from '../types';"""

fixed = """  PaymentAccountVerification,
  PAYMENT_CHANNELS,
  getPaymentChannelByCode,
} from '../types';
import { db } from '../firebase';
import {
  collection, query, where, getDocs, doc, updateDoc,
} from 'firebase/firestore';"""

if broken in content:
    content = content.replace(broken, fixed, 1)
    print("[OK] Import berhasil diperbaiki.")
else:
    print("[GAGAL] Pattern tidak ketemu persis. Perlu cek manual.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
