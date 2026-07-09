# Panduan Pengguna — Shopnesia Executive Dashboard 📊🌲

Selamat datang di **Shopnesia Executive Dashboard**! Aplikasi ini dirancang khusus bagi jajaran manajemen dan eksekutif untuk memantau performa bisnis, menganalisis pasar, serta mendapatkan wawasan operasional e-commerce secara cepat, interaktif, dan mudah dipahami.

---

## 💡 Apa yang Bisa Anda Lakukan di Dashboard Ini?

Dashboard ini dibagi menjadi tiga halaman utama yang dapat Anda akses melalui menu navigasi di sebelah kiri:

### 1. 📊 Ringkasan Performa
*   **Pantau Metrik Bisnis Utama**: Temukan ringkasan total pendapatan (*Revenue*), jumlah pesanan, rata-rata rating kepuasan pelanggan, serta tingkat retur barang secara instan.
*   **Tren Grafik**: Visualisasikan pertumbuhan pendapatan bulanan dan performa penjualan per kategori produk.

### 2. 🔍 Analisis Pasar & Operasional
*   **Distribusi Geografis**: Ketahui provinsi dengan kontribusi penjualan tertinggi.
*   **Analisis Pengiriman**: Analisis efisiensi logistik (rata-rata hari pengiriman) dan hubungannya dengan rating kepuasan pelanggan.
*   **Preferensi Pembayaran**: Identifikasi metode pembayaran terpopuler yang paling sering digunakan oleh pelanggan Anda.

### 3. 💡 Insight Eksekutif
*   **Ringkasan Otomatis**: Dapatkan ringkasan performa penjualan secara instan.
*   **Tabel Ringkasan Bulanan**: Telusuri data kinerja bulanan secara detail lengkap dengan fitur pengurutan kolom dan pembagian halaman (*pagination*).
*   **Ubah Data Langsung**: Anda dapat menyesuaikan atau mengubah nilai data bulanan secara langsung pada tabel menggunakan panel edit yang disediakan.

---

## 🎛️ Cara Menggunakan Fitur Interaktif

*   **Penyaringan Data (Filter)**: Gunakan panel filter di sidebar kiri untuk menyaring data berdasarkan rentang tanggal, kategori produk, wilayah provinsi, metode pembayaran, atau tier merek (*brand tier*). Semua grafik dan kartu metrik akan terupdate secara otomatis.
*   **Melihat Detail Grafik**: Arahkan kursor (*hover*) ke area grafik Plotly untuk melihat angka detail di setiap titik data atau batang diagram.
*   **Mengubah Data Tabel**: Buka panel ekspansi *"Edit Nilai Baris"* di Tab Insight Eksekutif, masukkan angka baru yang Anda inginkan, lalu tekan tombol simpan untuk memperbarui tampilan tabel secara instan.

---

## 🚀 Cara Menjalankan Aplikasi

Aplikasi ini dapat dijalankan dengan mudah melalui langkah-langkah berikut:

1. **Unduh kode sumber (Clone):**
   ```bash
   git clone <repository-url>
   cd dashboard_shopnesia
   ```

2. **Pasang paket pendukung (Dependencies):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi:**
   ```bash
   streamlit run tugas_dashboard.py
   ```
---

##📦 dashboard_shopnesia
* 📜 tugas_dashboard.py    # Skrip utama aplikasi Streamlit (UI & Logic)
* 📜 Dataset_bersih.csv    # Dataset e-commerce yang telah dibersihkan
* 📜 Dataset_bersih.xlsx   # Backup dataset format Excel
* 📜 requirements.txt      # Daftar pustaka/library Python yang dibutuhkan
* 📜 README.md             # Dokumentasi proyek

---

## 👥 Tim Pengembang
Proyek ini dikembangkan sebagai tugas Data Analytics dan Visualisasi (DAV) oleh kelompok kami:
* Adinata (Data Preparation & Initial Setup)
* Danendra (Data Processing & Repository Management)
* Dzikri (UI/UX Layout Optimization)
* Yama Dewa / 12paradewa (UX Enhancement, Interactivity & Documentation)
Dashboard ini di-deploy menggunakan Streamlit Community Cloud.

---
