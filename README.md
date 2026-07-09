# Shopnesia Executive Dashboard 📊🌲

Shopnesia Executive Dashboard adalah dashboard analitik bisnis e-commerce premium yang dirancang dengan performa tinggi dan estetika visual modern. Memanfaatkan skema warna bernuansa alam (*forest & moss green*) yang harmonis, dashboard ini memberikan kenyamanan visual sekaligus kedalaman informasi analitis bagi jajaran eksekutif.

---

## 🎨 Panduan Desain & Palet Warna

Dashboard ini menerapkan skema warna bertema alam yang konsisten:
- **Primary Moss Green (`#38470B`)**: Digunakan untuk elemen utama dan teks penting.
- **Dark Forest Green (`#2E3710`)**: Digunakan sebagai latar belakang sidebar navigation menu.
- **Light Accent Green (`#8CA052`)**: Digunakan untuk gradasi, aksen, dan indikator positif.
- **Secondary Sand/Tan (`#A0855B`)**: Digunakan untuk garis pembatas dan dekorasi sekunder.
- **Accent Red (`#C05C5C`)**: Digunakan khusus untuk indikator penurunan performa (tren negatif).
- **Background Cream (`#F9F6F2`)**: Warna dasar halaman web untuk kenyamanan membaca.

---

## ✨ Fitur-Fitur Utama & Layout Modern

### 1. Sticky Header Banner (Paling Atas)
- Banner judul utama (`Shopnesia Executive Dashboard`) diposisikan sebagai elemen **Sticky/Fixed** di bagian atas halaman (`top: 0px`).
- Menggunakan gradasi linear hijau hutan dengan efek bayangan elegan.
- Saat melakukan *scroll*, seluruh grafik dan data di bawahnya akan meluncur di belakang banner ini secara mulus.

### 2. Navigasi Sidebar Berbentuk Card Buttons
- Menggantikan tombol opsi radio biasa dengan susunan menu card modern.
- Dilengkapi dengan animasi mikro:
  - **Hover**: Mengangkat card (`translateY(-2px) translateX(3px)`) dan mengubah warna teks menjadi hijau moss.
  - **Active**: Card terpilih mendapat gradasi warna hijau hutan gelap penuh dengan teks putih tebal.
- Jarak antar-navigasi telah dikompres secara rapat menggunakan margin negatif CSS.

### 3. Filter Dashboard di Sidebar
- Seluruh kontrol penyaringan data ditempatkan di sidebar sebelah kiri di bawah menu navigasi:
  - **Rentang Tanggal** (Kalender Dinamis)
  - **Kategori Produk** (Multi-select)
  - **Provinsi Pelanggan** (Multi-select)
  - **Metode Pembayaran** (Multi-select)
  - **Brand Tier** (Multi-select)

### 4. Card KPI Modern dengan Sparkline Mingguan
- Menampilkan metrik bisnis utama (Revenue, Pesanan, Rata-rata Rating, Jumlah Retur) dalam bentuk card border bernuansa pasir emas.
- Setiap card dilengkapi dengan **Sparkline Mingguan** (grafik garis mini tanpa sumbu aksis):
  - **Hijau Hutan (`#5D702A`)**: Menandakan performa mingguan naik/positif dibanding minggu sebelumnya.
  - **Merah (`#C05C5C`)**: Menandakan performa mingguan menurun/negatif.

### 5. Layout Grafik Skala Penuh (Full-Width)
- Setiap chart dalam tab performa disajikan secara vertikal dengan lebar **100%** (`use_container_width=True`) dan tinggi **400px** untuk memaksimalkan keterbacaan di layar monitor resolusi tinggi.

### 6. Tabel Interaktif dengan Pagination & Editor Nilai (Tab 3)
- **Pagination Dinamis**: Membatasi tabel "Ringkasan Bulanan" maksimal 10 baris per halaman untuk menghindari scrollbar ganda.
- **Pre-Sorted Pagination**: Proses pengurutan kolom dilakukan terlebih dahulu di Python sebelum data dipotong per halaman, memperbaiki bug pengurutan bawaan Streamlit.
- **In-Place Row Editor**: Panel tersembunyi berikon material `:material/edit:` yang memungkinkan pengguna mengubah nilai sel baris tabel secara langsung.
- **Material Icons**: Seluruh tombol pagination (Chevron kiri/kanan) dan tombol simpan data (`:material/save:`) menggunakan ikon Material Design asli, bebas dari emoticon.

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
