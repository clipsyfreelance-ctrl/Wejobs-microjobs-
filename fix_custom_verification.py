#!/usr/bin/env python3
"""
Script untuk mengganti form verifikasi dengan halaman HTML custom
"""

import os
import re
from pathlib import Path

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Konfirmasi lokasi
    cwd = os.getcwd()
    if 'Wejobs-microjobs' not in cwd:
        print('[GAGAL] Bukan di folder Wejobs-microjobs!')
        return

    file_path = 'src/components/PaymentVerificationManager.tsx'
    content = read_file(file_path)
    print('[OK] File dibaca')

    # 1. Tambahkan state baru
    state_pattern = r'(const \[verificationModalOpen, setVerificationModalOpen\] = useState\(false\);)'
    state_replacement = r'\1\n  const [customVerificationPage, setCustomVerificationPage] = useState<string | null>(null);'
    
    if 'customVerificationPage' in content:
        print('[OK] State customVerificationPage sudah ada')
    else:
        content = re.sub(state_pattern, state_replacement, content)
        if 'customVerificationPage' in content:
            print('[OK] State customVerificationPage berhasil ditambahkan')
        else:
            print('[GAGAL] Gagal menambahkan state')
            return

    # 2. Ubah handleOpenVerification
    func_pattern = r'(const handleOpenVerification = \(channel: PaymentChannelConfig\) => \{)(.*?)(// Check existing verification for prefill)'
    func_replacement = r'''\1
    // Cek apakah channel termasuk dalam 6 channel dengan halaman custom
    const customChannels = ['bsi', 'bca', 'bri', 'dana', 'ovo', 'gopay'];
    if (customChannels.includes(channel.code)) {
      setCustomVerificationPage(`/verification-pages/${channel.code}.html`);
      return;
    }

    if (channel.status === 'maintenance' || channel.status === 'coming_soon') {
      setChannelInfoModal(channel);
      return;
    }

    if (eligibilityStatus !== 'eligible') {
      showToast(
        'error',
        '⚠️ Anda wajib mengajukan verifikasi kelayakan (Eligible) dan disetujui Admin terlebih dahulu sebelum memverifikasi rekening.'
      );
      return;
    }

    // Check existing verification for prefill\3'''
    
    content = re.sub(func_pattern, func_replacement, content, flags=re.DOTALL)
    if 'customChannels' in content:
        print('[OK] handleOpenVerification berhasil diubah')
    else:
        print('[GAGAL] Gagal mengubah handleOpenVerification')
        return

    # 3. Tambahkan JSX modal custom
    modal_pattern = r'(\{verificationModalOpen && selectedChannel && \()'
    custom_modal = '''
      {/* ========================================== */}
      {/* MODAL CUSTOM: HALAMAN VERIFIKASI HTML */}
      {/* ========================================== */}
      {customVerificationPage && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-0 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full h-full max-w-4xl max-h-[95vh] bg-white dark:bg-neutral-900 rounded-none sm:rounded-3xl overflow-hidden relative">
            <button
              type="button"
              onClick={() => setCustomVerificationPage(null)}
              className="absolute top-4 right-4 z-10 p-2 rounded-full bg-black/50 hover:bg-black/70 text-white cursor-pointer transition-colors"
            >
              ✕
            </button>
            <iframe
              src={customVerificationPage}
              className="w-full h-full"
              style={{ border: 'none' }}
              sandbox="allow-scripts allow-same-origin"
            />
          </div>
        </div>
      )}
'''
    content = re.sub(modal_pattern, custom_modal + r'\1', content)
    if 'MODAL CUSTOM' in content:
        print('[OK] JSX modal custom berhasil ditambahkan')
    else:
        print('[GAGAL] Gagal menambahkan JSX modal custom')
        return

    # Write file
    write_file(file_path, content)
    print('[OK] File berhasil diupdate')

    print('\n✅ SCRIPT SELESAI - Semua perubahan berhasil')
    print('📝 Silakan jalankan: npm run dev')

if __name__ == '__main__':
    main()
