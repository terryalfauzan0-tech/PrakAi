# TikTok Demand & Behavior Insight AI 🚀

Aplikasi berbasis AI untuk menganalisis perilaku konsumen dan potensi permintaan bisnis berdasarkan komentar video TikTok secara real-time.

## 🌟 Fitur Utama
- **Real-Time Data Acquisition**: Mengambil data komentar dan metadata resmi langsung dari link TikTok menggunakan TikWM API.
- **AI-Powered Sentiment Classification**: Klasifikasi otomatis komentar ke dalam 4 kategori strategis:
  - 🟢 Positif Ingin Beli (High Intent)
  - 🔵 Positif Tidak Ingin Beli (Positive Sentiment)
  - 🔴 Negatif (Feedback/Complaint)
  - 🟡 Pertanyaan (Potential Lead)
- **Business Insights & Estimates**:
  - **Estimasi Pembeli**: Proyeksi jumlah pembeli berdasarkan ekstrapolasi data sampel ke total komentar video.
  - **Rekomendasi Produksi**: Saran jumlah stok awal (120% dari estimasi pembeli) untuk menghindari *stockout*.
- **Smart Recommendation**: Saran strategi bisnis otomatis (Smart CTA, Evaluasi Produk, dsb) berdasarkan dominasi kategori komentar.
- **Interactive Dashboard**: Visualisasi Chart.js, filter kategori, dan daftar komentar dengan label warna.
- **Premium UI**: Desain modern SaaS, responsif, dan mendukung Dark Mode.

## 🛠️ Tech Stack
- **Backend**: Python (FastAPI, Uvicorn)
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6+)
- **Visualization**: Chart.js
- **Data Source**: TikWM API (Requests & Asyncio)
- **Icons**: FontAwesome 6

## 🚀 Instalasi & Cara Menjalankan

### Prasyarat
- Python 3.8 atau versi lebih baru
- Koneksi Internet (untuk scraping data TikTok)

### Langkah-langkah
1. **Clone atau Download Proyek**
   Simpan file ke dalam folder kerja Anda.

2. **Instal Dependensi**
   Buka terminal/command prompt di folder proyek dan jalankan:
   ```bash
   pip install fastapi uvicorn requests pydantic
   ```

3. **Jalankan Aplikasi**
   Eksekusi file `main.py`:
   ```bash
   python main.py
   ```

4. **Buka di Browser**
   Akses dashboard melalui URL berikut:
   [http://localhost:8000](http://localhost:8000)

## 📁 Struktur Proyek
- `main.py`: Entry point aplikasi dan endpoint API.
- `scraper.py`: Modul untuk mengambil data teks dan metadata dari TikTok.
- `analyzer.py`: Logika pemrosesan bahasa alami (NLP) dan klasifikasi kategori.
- `static/`: Berisi aset frontend (HTML, CSS, JS).

## 💡 Catatan Teknis
Aplikasi ini menggunakan metode **Sampling & Extrapolation**. Jika sebuah video memiliki puluhan ribu komentar, sistem akan mengambil sampel ribuan komentar terbaru, menganalisis distribusinya, lalu memproyeksikan hasilnya ke total jumlah komentar resmi agar mendapatkan estimasi bisnis yang mendekati kenyataan.

---
Dibuat oleh Tim AI UNY - Semester 4
