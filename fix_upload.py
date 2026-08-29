path = "src/components/PaymentVerificationManager.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      setFormError('Ukuran file maksimal 5 MB.');
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setProofFile({
        name: file.name,
        url: reader.result as string,
      });
      setFormError(null);
    };
    reader.readAsDataURL(file);
  };"""

new = """  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      setFormError('Ukuran file maksimal 5 MB.');
      return;
    }

    const img = new Image();
    const reader = new FileReader();
    reader.onload = () => {
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const maxWidth = 900;
        const scale = Math.min(1, maxWidth / img.width);
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        const ctx = canvas.getContext('2d');
        ctx?.drawImage(img, 0, 0, canvas.width, canvas.height);
        const compressedUrl = canvas.toDataURL('image/jpeg', 0.6);

        if (compressedUrl.length > 900000) {
          setFormError('Gambar masih terlalu besar setelah dikompres. Coba foto dengan resolusi lebih kecil.');
          return;
        }

        setProofFile({
          name: file.name,
          url: compressedUrl,
        });
        setFormError(null);
      };
      img.src = reader.result as string;
    };
    reader.readAsDataURL(file);
  };"""

if old in content:
    content = content.replace(old, new, 1)
    print("[OK] handleFileUpload berhasil diganti dengan versi kompresi gambar.")
else:
    print("[GAGAL] Pattern tidak ketemu, cek manual.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
