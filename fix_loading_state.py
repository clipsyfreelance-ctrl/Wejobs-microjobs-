#!/usr/bin/env python3
"""
Script untuk menambahkan loading state pada modal custom
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

    # 1. Tambahkan state loading
    state_pattern = r'(const \[customVerificationPage, setCustomVerificationPage\] = useState<string \| null>\(null\);)'
    state_replacement = r'\1\n  const [isCustomPageLoading, setIsCustomPageLoading] = useState(true);'
    
    if 'isCustomPageLoading' in content:
        print('[OK] State isCustomPageLoading sudah ada')
    else:
        content = re.sub(state_pattern, state_replacement, content)
        if 'isCustomPageLoading' in content:
            print('[OK] State isCustomPageLoading berhasil ditambahkan')
        else:
            print('[GAGAL] Gagal menambahkan state')
            return

    # 2. Tambahkan reset loading saat modal dibuka
    # Cari di handleOpenVerification bagian setCustomVerificationPage
    open_pattern = r'(setCustomVerificationPage\(`/verification-pages/\$\{channel\.code\}\.html`\);)'
    open_replacement = r'\1\n      setIsCustomPageLoading(true);'
    
    content = re.sub(open_pattern, open_replacement, content)
    if 'setIsCustomPageLoading(true);' in content:
        print('[OK] Reset loading ditambahkan ke handleOpenVerification')
    else:
        print('[GAGAL] Gagal menambahkan reset loading')

    # 3. Tambahkan reset loading saat modal ditutup
    close_pattern = r'(onClick=\{\(\) => setCustomVerificationPage\(null\)\})'
    close_replacement = r'onClick={() => { setCustomVerificationPage(null); setIsCustomPageLoading(true); }}'
    
    content = re.sub(close_pattern, close_replacement, content)
    if 'setIsCustomPageLoading(true);' in content and 'setCustomVerificationPage(null);' in content:
        print('[OK] Reset loading ditambahkan ke tombol tutup')
    else:
        print('[GAGAL] Gagal menambahkan reset loading ke tombol tutup')

    # 4. Ganti JSX modal custom dengan versi yang ada loading
    custom_modal_pattern = r'(\{customVerificationPage && \([\s\S]*?<iframe[\s\S]*?\/>[\s\S]*?<\/div>[\s\S]*?<\/div>[\s\S]*?\)\})'
    
    new_modal = '''{customVerificationPage && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-0 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full h-full max-w-4xl max-h-[95vh] bg-white dark:bg-neutral-900 rounded-none sm:rounded-3xl overflow-hidden relative">
            {/* Loading Spinner */}
            {isCustomPageLoading && (
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-white dark:bg-neutral-900 z-20">
                <div className="w-12 h-12 border-4 border-neutral-200 dark:border-neutral-700 border-t-blue-600 dark:border-t-blue-400 rounded-full animate-spin"></div>
                <p className="mt-4 text-sm text-neutral-600 dark:text-neutral-400 font-medium">Memuat halaman verifikasi...</p>
              </div>
            )}
            
            <button
              type="button"
              onClick={() => { setCustomVerificationPage(null); setIsCustomPageLoading(true); }}
              className="absolute top-4 right-4 z-10 p-2 rounded-full bg-black/50 hover:bg-black/70 text-white cursor-pointer transition-colors"
            >
              ✕
            </button>
            
            <iframe
              src={customVerificationPage}
              className="w-full h-full"
              style={{ border: 'none' }}
              sandbox="allow-scripts allow-same-origin"
              onLoad={() => setIsCustomPageLoading(false)}
              onError={() => setIsCustomPageLoading(false)}
            />
          </div>
        </div>
      )}'''
    
    # Cari dan ganti modal custom
    # Kita cari berdasarkan pola yang lebih sederhana
    if '{customVerificationPage && (' in content:
        # Cari posisi modal custom
        start = content.find('{customVerificationPage && (')
        if start != -1:
            # Cari akhir modal (cari }) yang menutup
            # Kita cari dengan menghitung kurung
            depth = 0
            end = start
            in_string = False
            for i in range(start, len(content)):
                char = content[i]
                if char == '"' or char == "'":
                    in_string = not in_string
                if not in_string:
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
            
            if end > start:
                old_modal = content[start:end]
                # Cek apakah sudah ada loading
                if 'isCustomPageLoading' in old_modal and 'Loading Spinner' in old_modal:
                    print('[OK] Loading sudah ada di modal')
                else:
                    content = content[:start] + new_modal + content[end:]
                    print('[OK] Modal custom diupdate dengan loading')
            else:
                print('[GAGAL] Tidak dapat menemukan akhir modal')
                return

    # Write file
    write_file(file_path, content)
    print('[OK] File berhasil diupdate')

    print('\n✅ SCRIPT SELESAI - Loading state berhasil ditambahkan')
    print('📝 Silakan jalankan: npm run dev')

if __name__ == '__main__':
    main()
