import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.1 Safari/537.36"
}

semua_berita = []  # tempat menyimpan semua hasil

page = 1
while True:
    if page == 1:
        url = "https://pajak.go.id/id/berita-page"
    else:
        url = f"https://pajak.go.id/id/berita-page?page={page}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Gagal mengakses {url} : {e}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all('div', class_='views-row')

    if not items:
        print(f"❌ Tidak ada berita ditemukan di halaman {page}. Selesai.")
        break

    print(f"📄 Mengambil data dari halaman {page}...")

    for item in items:
        judul_tag = item.find('a')
        judul = judul_tag.text.strip() if judul_tag else "Tidak ada judul"
        link = "https://pajak.go.id" + judul_tag['href'] if judul_tag else "Tidak ada link"
        tanggal_tag = item.find('span', class_='date-display-single')
        tanggal = tanggal_tag.text.strip() if tanggal_tag else "Tidak ada tanggal"

        semua_berita.append({
            "Judul": judul,
            "Tanggal": tanggal,
            "Link": link
        })

    page += 1
    time.sleep(2)  # jeda supaya aman

# Simpan ke Excel
df = pd.DataFrame(semua_berita)
df.to_excel("berita_pajak.xlsx", index=False)
print(f"✅ Data berhasil disimpan ke berita_pajak.xlsx ({len(semua_berita)} berita)")
