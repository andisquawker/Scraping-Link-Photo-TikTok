# Import Library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException
)
import logging
import time

# Konfigurasi Logging
logging.basicConfig(
    level=logging.INFO,  # Mengatur level logging ke INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format pesan log
    handlers=[logging.FileHandler("scraping_log.log"), logging.StreamHandler()]
)

# Konfigurasi Browser
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Agar browser tetap terbuka setelah skrip selesai
options.add_argument("--disable-notifications")  # Menonaktifkan notifikasi browser
options.add_argument("--mute-audio")  # Menonaktifkan audio di browser
options.add_argument("--disable-blink-features=AutomationControlled")  # Menghindari deteksi otomatisasi
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--user-data-dir=")  # Menyimpan profil pengguna untuk memuat cookie

# Inisialisasi Variabel
username_tiktok = input("Masukkan nama file (tanpa ekstensi): ").strip()  # Nama file output
file_path = f"{username_tiktok}.txt"  # Path file output
max_same_links = 10  # Jumlah maksimum link yang sama untuk menghentikan proses

# Baca File
try:
    with open(file_path, "r", encoding="utf-8") as file:
        existing_links = set(file.read().splitlines())  # Membaca link yang sudah ada di file
except FileNotFoundError:
    logging.info("File tidak ditemukan, membuat file baru.")
    existing_links = set()

# Inisialisasi Driver
try:
    driver = webdriver.Chrome(options=options)  # Memulai driver Chrome
    driver.get(f"https://www.tiktok.com/@{username_tiktok}")  # Membuka halaman profil TikTok
    time.sleep(5)  # Tunggu statis agar halaman termuat sepenuhnya
except WebDriverException as e:
    logging.error(f"Gagal memulai driver: {e}")
    exit()

# Scroll dan Kumpulkan Link
pause_time = 3  # Waktu tunggu setelah scrolling
new_links = set()  # Set untuk menyimpan link baru
same_links_count = 0  # Counter untuk menghitung link yang sama

try:
    while True:
        # Scroll ke bawah
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script("return document.body.scrollHeight") > 0
        )

        # Tunggu agar konten termuat
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-e2e="user-post-item"]'))
        )

        # Temukan elemen video
        div_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-e2e="user-post-item"]')
        for div in div_elements:
            links = div.find_elements(By.TAG_NAME, 'a')
            for link in links:
                url = link.get_attribute('href')
                if url and '/photo/' in url:
                    if url in existing_links:
                        same_links_count += 1
                        if same_links_count >= max_same_links:
                            logging.info(f"Proses berhenti karena menemukan {max_same_links} link yang sama.")
                            raise StopIteration
                    else:
                        new_links.add(url)
                        print(f"Link Baru {url}")

        # Hentikan jika tinggi halaman tidak berubah
        new_height = driver.execute_script("return document.body.scrollHeight")
        last_height = getattr(driver, "last_height", 0)
        if new_height == last_height:
            logging.info("Scrolling selesai: Tidak ada konten baru.")
            break
        driver.last_height = new_height

except (NoSuchElementException, TimeoutException) as e:
    logging.warning(f"Error saat mencari elemen: {e}")
except StopIteration:
    pass
except Exception as e:
    logging.error(f"Error tidak terduga: {e}")
finally:
    driver.quit()

# Simpan Link Baru ke File
if new_links:
    with open(file_path, "a", encoding="utf-8") as file:
        for link in sorted(new_links):
            file.write(link + "\n")
    logging.info(f"Link baru berhasil disimpan ke file: {file_path}")
else:
    logging.info("Tidak ada link baru yang ditemukan.")
