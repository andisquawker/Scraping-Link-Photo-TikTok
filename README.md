# TikTok Photo Links Scraper

## Deskripsi
Skrip ini digunakan untuk mengumpulkan semua tautan photo dari profil pengguna TikTok. Skrip akan melakukan scrolling otomatis pada halaman profil pengguna, mendeteksi semua tautan photo yang ada, dan menyimpannya ke dalam file teks. Skrip juga dilengkapi dengan mekanisme untuk mencegah duplikasi tautan dan mengatur batas penghentian berdasarkan jumlah tautan yang sama.

## Fitur
- Scraping otomatis semua tautan photo dari profil TikTok.
- Penyimpanan tautan ke dalam file teks tanpa duplikasi.
- Mekanisme penghentian otomatis jika tidak ada tautan baru.
- Konfigurasi logging untuk mencatat proses scraping.
- Menggunakan Selenium untuk mengotomatisasi browser.

## Persyaratan
- Python 3.x
- Google Chrome
- Selenium WebDriver

## Cara Penggunaan
1. Instal dependensi menggunakan file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Pastikan **ChromeDriver** sesuai dengan versi Google Chrome yang terpasang.
3. Jalankan skrip:
   ```bash
   python Scraping Link Photo TikTok.py
   ```
4. Masukkan nama pengguna TikTok (username profil tanpa ekstensi).
5. Tautan photo akan disimpan dalam file dengan nama `username.txt`.

## Struktur Log
- **INFO**: Memberikan informasi status normal seperti awal scraping atau penyimpanan file.
- **WARNING**: Memberikan peringatan jika ada elemen yang tidak ditemukan.
- **ERROR**: Memberikan detail kesalahan yang menyebabkan proses berhenti.


## Catatan
- Perhatikan kebijakan privasi dan syarat layanan dari TikTok saat menggunakan skrip ini.
- Skrip ini hanya untuk keperluan pendidikan dan pengarsipan. Gunakan dengan tanggung jawab penuh.

## Lisensi
Proyek ini dirilis di bawah lisensi MIT.
