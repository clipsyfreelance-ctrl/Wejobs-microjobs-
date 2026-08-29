import re

path = "src/components/AuthModals.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Tambah import Firebase setelah import lucide-react
old_import = "import { X, Lock, Mail, User as UserIcon, Phone, MapPin, AlertCircle, ShieldAlert, CheckCircle2, KeyRound } from 'lucide-react';"
new_import = old_import + """
import { auth, db } from '../firebase';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  sendPasswordResetEmail,
  signOut,
} from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';"""
content = content.replace(old_import, new_import, 1)

# 2. Ganti handleLoginSubmit
old_login = """  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);

    if (!loginCaptchaToken) {
      setLoginError('Please complete the security CAPTCHA verification.');
      return;
    }

    setLoginLoading(true);
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: loginEmail,
          password: loginPassword,
          captchaToken: loginCaptchaToken,
        }),
      });
      const data = await res.json();
      if (data.success && data.user) {
        onAuthSuccess(data.user, data.token, data.redirect);
        onClose();
      } else {
        setLoginError(data.error || 'Failed to authenticate.');
      }
    } catch (err) {
      setLoginError('Network error connecting to WEJOBS server.');
    } finally {
      setLoginLoading(false);
    }
  };"""

new_login = """  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);

    if (!loginCaptchaToken) {
      setLoginError('Please complete the security CAPTCHA verification.');
      return;
    }

    setLoginLoading(true);
    try {
      const cred = await signInWithEmailAndPassword(auth, loginEmail, loginPassword);
      const snap = await getDoc(doc(db, 'users', cred.user.uid));
      if (!snap.exists()) {
        setLoginError('Profil pengguna tidak ditemukan.');
        await signOut(auth);
        return;
      }
      const profile: any = snap.data();
      if (profile.banned) {
        setLoginError('Akun Anda telah dinonaktifkan oleh admin.');
        await signOut(auth);
        return;
      }
      const token = await cred.user.getIdToken();
      const user: User = { id: cred.user.uid, emailVerified: cred.user.emailVerified, ...profile };
      onAuthSuccess(user, token, '/dashboard');
      onClose();
    } catch (err: any) {
      setLoginError(err.message || 'Failed to authenticate.');
    } finally {
      setLoginLoading(false);
    }
  };"""

content = content.replace(old_login, new_login, 1)

# 3. Ganti handleRegisterSubmit
old_register = """  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegError(null);

    if (regPassword !== regConfirmPassword) {
      setRegError('Passwords do not match.');
      return;
    }

    if (!agreeTerms || !agreePrivacy) {
      setRegError('You must agree to the Terms of Service and Privacy Policy.');
      return;
    }

    if (!regCaptchaToken) {
      setRegError('Please complete the anti-bot CAPTCHA verification.');
      return;
    }

    setRegLoading(true);
    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fullName: regFullName,
          email: regEmail,
          phone: regPhone,
          address: regAddress,
          password: regPassword,
          avatarId: regAvatarId,
          builtinAvatarId: regAvatarId,
          captchaToken: regCaptchaToken,
        }),
      });
      const data = await res.json();
      if (data.success && data.user) {
        onAuthSuccess(data.user, data.token, '/dashboard');
        onClose();
      } else {
        setRegError(data.error || 'Failed to create account.');
      }
    } catch (err) {
      setRegError('Network connection error.');
    } finally {
      setRegLoading(false);
    }
  };"""

new_register = """  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegError(null);

    if (regPassword !== regConfirmPassword) {
      setRegError('Passwords do not match.');
      return;
    }

    if (!agreeTerms || !agreePrivacy) {
      setRegError('You must agree to the Terms of Service and Privacy Policy.');
      return;
    }

    if (!regCaptchaToken) {
      setRegError('Please complete the anti-bot CAPTCHA verification.');
      return;
    }

    setRegLoading(true);
    try {
      const cred = await createUserWithEmailAndPassword(auth, regEmail, regPassword);
      const profileData = {
        fullName: regFullName,
        email: regEmail,
        phone: regPhone,
        address: regAddress,
        role: 'user',
        avatarType: 'builtin',
        builtinAvatarId: regAvatarId,
        avatarId: regAvatarId,
        recipientStatus: 'unverified',
        createdAt: new Date().toISOString(),
        rating: 0,
        reviewCount: 0,
        completedJobsCount: 0,
        availableBalance: 0,
        pendingBalance: 0,
        balance: 0,
        banned: false,
      };
      await setDoc(doc(db, 'users', cred.user.uid), profileData);
      const token = await cred.user.getIdToken();
      const user: User = { id: cred.user.uid, emailVerified: cred.user.emailVerified, ...profileData };
      onAuthSuccess(user, token, '/dashboard');
      onClose();
    } catch (err: any) {
      setRegError(err.message || 'Failed to create account.');
    } finally {
      setRegLoading(false);
    }
  };"""

content = content.replace(old_register, new_register, 1)

# 4. Ganti handleAdminLoginSubmit
old_admin = """  const handleAdminLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdminError(null);

    if (!adminCaptchaToken) {
      setAdminError('Please complete the security challenge.');
      return;
    }

    setAdminLoading(true);
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: adminEmail,
          password: adminPassword,
          captchaToken: adminCaptchaToken,
        }),
      });
      const data = await res.json();
      if (data.success && data.user) {
        if (data.user.role !== 'admin' && data.user.role !== 'super_admin') {
          setAdminError('Unauthorized: Account does not have administrative privileges.');
          return;
        }
        onAuthSuccess(data.user, data.token, '/admin');
        onClose();
      } else {
        setAdminError(data.error || 'Invalid admin credentials.');
      }
    } catch (err) {
      setAdminError('Network error connecting to admin service.');
    } finally {
      setAdminLoading(false);
    }
  };"""

new_admin = """  const handleAdminLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdminError(null);

    if (!adminCaptchaToken) {
      setAdminError('Please complete the security challenge.');
      return;
    }

    setAdminLoading(true);
    try {
      const cred = await signInWithEmailAndPassword(auth, adminEmail, adminPassword);
      const snap = await getDoc(doc(db, 'users', cred.user.uid));
      if (!snap.exists()) {
        setAdminError('Profil admin tidak ditemukan di Firestore.');
        await signOut(auth);
        return;
      }
      const profile: any = snap.data();
      if (profile.role !== 'admin' && profile.role !== 'super_admin') {
        setAdminError('Unauthorized: Account does not have administrative privileges.');
        await signOut(auth);
        return;
      }
      const token = await cred.user.getIdToken();
      const user: User = { id: cred.user.uid, emailVerified: cred.user.emailVerified, ...profile };
      onAuthSuccess(user, token, '/admin');
      onClose();
    } catch (err: any) {
      setAdminError(err.message || 'Invalid admin credentials.');
    } finally {
      setAdminLoading(false);
    }
  };"""

content = content.replace(old_admin, new_admin, 1)

# 5. Ganti handleForgotSubmit supaya beneran kirim email reset password
old_forgot = """  const handleForgotSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setForgotLoading(true);
    setTimeout(() => {
      setForgotLoading(false);
      setForgotSubmitted(true);
    }, 600);
  };"""

new_forgot = """  const handleForgotSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setForgotLoading(true);
    try {
      await sendPasswordResetEmail(auth, forgotEmail);
    } catch (err) {
      // Sengaja tidak menampilkan error spesifik, demi keamanan (mencegah email enumeration)
    } finally {
      setForgotLoading(false);
      setForgotSubmitted(true);
    }
  };"""

content = content.replace(old_forgot, new_forgot, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Selesai! Semua bagian berhasil diganti.")
