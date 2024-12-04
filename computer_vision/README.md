# 🚀 Demo Computer Vision: Deteksi Objek & Penghitungan Orang

**Computer Vision** adalah cabang dari kecerdasan buatan (AI) yang memungkinkan komputer untuk memahami, menganalisis, dan memproses data visual seperti gambar dan video. Teknologi ini digunakan dalam berbagai aplikasi seperti pengenalan wajah, penghitungan jumlah orang, dan deteksi objek.

Demo ini memiliki dua fitur utama:
1. **Deteksi Objek** - Mengenali dan melokalisasi objek dalam gambar atau video.
2. **Penghitungan Orang** - Menghitung jumlah individu dalam suatu area menggunakan video real-time.

Demo ini menggunakan teknologi dari **Ultralytics** dan didukung oleh referensi dari **Roboflow**. Pastikan Anda memiliki **webcam** untuk menjalankan demo ini.

---

## 🧾 Fitur 1: Deteksi Objek

### Apa itu Deteksi Objek?  
Deteksi objek adalah teknik dalam **Computer Vision** yang digunakan untuk mengenali dan melokalisasi objek tertentu dalam gambar atau video. Teknik ini tidak hanya mendeteksi keberadaan suatu objek tetapi juga menggambar kotak pembatas (**bounding box**) di sekitarnya. Contoh penerapan termasuk:
- Sistem keamanan untuk mendeteksi intrusi.
- Kendaraan otonom untuk mengenali objek di jalan.
- Analisis video untuk pengawasan dan pelacakan.

### ⚙️ Setup untuk Deteksi Objek
Ikuti langkah-langkah berikut untuk menjalankan deteksi objek melalui **Command Line Interface (CLI)**:

1. **Install Ultralytics**:
   ```bash
   pip install ultralytics
   ```
   Catatan: Versi terbaru yang didukung adalah 8.3.39.

2. **Jalankan YOLO untuk Deteksi Objek**:
   ```bash
   yolo detect predict model=yolov5l.pt source=0 show=true
   ```
   - model: Menggunakan model YOLOv5 pre-trained (yolov5l.pt).
   - source=0: Menggunakan webcam sebagai sumber input.
   - show=true: Menampilkan hasil deteksi langsung di layar.

3. **Untuk keluar dari proses deteksi**, tekan `ctrl+c` pada **CLI** untuk menghentikan program.

## 🧾 Fitur 2: Penghitungan Orang

### Apa itu Penghitungan Orang?
Penghitungan orang adalah aplikasi Computer Vision yang digunakan untuk menghitung jumlah individu dalam suatu area berdasarkan data video. Teknik ini berguna dalam:
- Manajemen kerumunan di tempat umum.
- Analisis lalu lintas di pusat perbelanjaan.
- Peningkatan efisiensi di acara atau ruang yang ramai.

## ⚙️ Setup untuk Penghitungan Orang
Ikuti langkah-langkah berikut untuk menjalankan fitur penghitungan orang:

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/victorico123/ai_demo.git
   ```
2. **Arahkan ke Direktori**:
   ```bash
   cd ai_demo
   cd computer_vision
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Jalankan Skrip Penghitungan Orang**:
   ```bash
   python main.py
   ```
   Skrip ini akan memanfaatkan webcam untuk mendeteksi dan menghitung jumlah orang dalam area yang terdeteksi.
5. **Untuk keluar dari proses deteksi**, tekan `ctrl+c` pada **CLI** untuk menghentikan program.

## 🛠️ Teknologi yang Digunakan

- **Ultralytics**: Framework yang mendukung YOLOv5 untuk deteksi objek secara real-time.
- **Roboflow**: Sumber referensi untuk dataset dan inspirasi dalam pengembangan demo ini.

## 📷 Persyaratan
- **Webcam**: Dibutuhkan untuk menjalankan kedua demo (deteksi objek dan penghitungan orang).

---

Selamat mencoba demo Computer Vision ini! 🚀

