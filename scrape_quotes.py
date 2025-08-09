import requests
from bs4 import BeautifulSoup
import csv

# Buka file CSV untuk ditulis
with open('quotes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Quote', 'Author'])  # header

    page = 1
    while True:
        url = f"https://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)

        # Berhenti kalau halaman tidak ditemukan
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        # Ambil data dari setiap quote
        for quote in quotes:
            text = quote.find('span', class_='text').text.strip()
            author = quote.find('small', class_='author').text.strip()
            writer.writerow([text, author])

        print(f"Selesai halaman {page}")
        page += 1

print("✅ Semua kutipan sudah disimpan ke 'quotes.csv'")
