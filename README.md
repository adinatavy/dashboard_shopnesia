# Shopnesia Executive Dashboard 📊🌲

Shopnesia Executive Dashboard adalah dashboard analitik bisnis e-commerce premium yang dirancang dengan performa tinggi dan estetika visual modern. Memanfaatkan skema warna bernuansa alam (*forest & moss green*) yang harmonis, dashboard ini memberikan kenyamanan visual sekaligus kedalaman informasi analitis bagi jajaran eksekutif.

---

## 🎨 Panduan Desain & Palet Warna

Dashboard ini menerapkan skema warna bertema alam yang konsisten:
- **Primary Moss Green (`#38470B`)**: Digunakan untuk elemen utama dan teks penting.
- **Dark Forest Green (`#2E3710`)**: Latar belakang navigation menu.
- **Light Accent Green (`#8CA052`)**: Gradasi dan aksen positif.
- **Secondary Sand/Tan (`#A0855B`)**: Garis pembatas sekunder.
- **Accent Red (`#C05C5C`)**: Penurunan performa (tren negatif).
- **Background Cream (`#F9F6F2`)**: Warna dasar halaman web.

---

## ⚙️ Fitur-Fitur Sistem

- **Sparkline Mingguan**: Tren naik (hijau) atau turun (merah) mingguan pada metrik utama.
- **Pagination Dinamis**: Membatasi tabel "Ringkasan Bulanan" maksimal 10 baris per halaman.
- **Pre-Sorted Pagination**: Pengurutan kolom yang dihitung sebelum data disajikan per halaman.
- **In-Place Row Editor**: Form interaktif berikon material `:material/edit:` untuk memutasi data.
- **Material Icons**: Seluruh aksi kontrol menggunakan ikon Material Design asli, bebas dari emoticon.

---

## 🛠️ Persyaratan Sistem

Pastikan library berikut terinstall (didefinisikan dalam `requirements.txt`):
- `streamlit` (Disarankan versi >= 1.35.0 untuk dukungan Material Icons)
- `pandas`
- `plotly`
- `openpyxl` (untuk membaca file dataset)

---

## 🚀 Cara Menjalankan Aplikasi

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd dashboard_shopnesia
   ```

2. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan server Streamlit:**
   ```bash
   streamlit run tugas_dashboard.py
   ```
