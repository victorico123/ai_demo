# Menjalankan Mistral Secara Lokal dengan Ollama

Demo **chatbot AI** berbasis CLI (Command Line Interface) menggunakan model **Mistral** yang dijalankan melalui platform **Ollama**. Dalam demo ini, Anda dapat berinteraksi langsung dengan model Mistral untuk mencoba berbagai kemampuan model bahasa besar, seperti percakapan, pemahaman teks, dan pembuatan respons berbasis query yang diberikan.

## 📋 Persyaratan
Sebelum menjalankan demo ini, pastikan Anda sudah menyiapkan beberapa hal berikut:
- **Ollama** harus terinstal di sistem Anda.
- Koneksi internet yang stabil untuk mengunduh model dan menjalankan interaksi.

**Catatan**: Ollama adalah aplikasi yang memungkinkan Anda untuk menggunakan berbagai model bahasa besar (Large Language Models / LLMs) tanpa memerlukan konfigurasi yang rumit. Anda cukup mengunduh dan menjalankannya langsung melalui CLI.

## 🚀 Setup dan Instalasi

Ikuti langkah-langkah berikut untuk menjalankan **Mistral** secara lokal dengan menggunakan **Ollama**:

1. **Install Ollama**:
   - Ollama adalah platform yang memungkinkan interaksi dengan berbagai model LLMs. Untuk menginstalnya, kunjungi [Ollama Download](https://ollama.com/download) dan pilih versi yang sesuai dengan sistem operasi yang Anda gunakan (Windows, macOS, atau Linux).
   - Ikuti petunjuk instalasi yang disediakan di halaman tersebut untuk memastikan Ollama terinstal dengan benar pada sistem Anda.

2. **Tarik model Mistral dengan Ollama**:
   - Setelah Ollama terinstal, buka terminal atau Command Prompt pada sistem Anda, dan jalankan perintah berikut untuk mengunduh model **Mistral**:
     ```bash
     ollama pull mistral
     ```
     Perintah ini akan mengunduh model Mistral yang siap digunakan. Pastikan Anda memiliki koneksi internet yang baik karena model ini memiliki ukuran yang besar dan mungkin memerlukan beberapa menit untuk selesai diunduh.

3. **Jalankan Mistral**:
   - Setelah model berhasil diunduh, jalankan model **Mistral** dengan menggunakan perintah berikut:
     ```bash
     ollama run mistral
     ```
     Perintah ini akan memulai eksekusi model Mistral dan mempersiapkan model untuk menerima input query.

4. **Mulai Interaksi**:
   - Setelah menjalankan perintah `ollama run mistral`, tunggu beberapa saat hingga model siap untuk menerima input.
   - Anda sekarang dapat mulai berinteraksi dengan model **Mistral**. Cukup masukkan **query** atau pertanyaan Anda di CLI, dan model akan memberikan respons berbasis pengetahuan yang ada dalam model tersebut.
   - Misalnya, Anda bisa bertanya tentang topik tertentu atau meminta model untuk menjelaskan konsep tertentu.
   - **Contoh interaksi**:
     ```
     User: Siapa penemu komputer?
     Mistral: Penemu komputer pertama kali adalah Charles Babbage, yang dikenal sebagai "bapak komputer".
     ```

   - **Catatan**: Untuk keluar dari program, tekan `Ctrl+C` di terminal atau Command Prompt Anda.

---

Dengan langkah-langkah di atas, Anda dapat menjalankan **Mistral** secara lokal menggunakan Ollama. Model ini memberikan pengalaman langsung dalam berinteraksi dengan chatbot AI yang dapat membantu menjawab berbagai pertanyaan berbasis pengetahuan yang dimilikinya.


# RAG Lokal dengan Ollama

Demo **Retrieval-Augmented Generation (RAG)** menggunakan **Ollama** untuk menjawab pertanyaan berdasarkan dokumen eksternal yang diunggah. Dalam demo ini, kita menggabungkan teknologi pencarian dan pembangkitan untuk meningkatkan akurasi jawaban.

## 📋 Syarat Menjalankan Demo
- Python versi **3.12.x** atau lebih baru
- Git untuk meng-clone repositori

## 🚀 Setup dan Instalasi

Ikuti langkah-langkah di bawah ini untuk mempersiapkan demo **RAG Lokal**:

1. **Clone repositori ini**:
   ```bash
   git clone https://github.com/victorico123/ai_demo.git
   ```
2. **Masuk ke direktori** untuk model Large Language:
   ```bash
   cd ai_demo
   cd large_language_model
   ```
3. **Install dependencies** menggunakan `pip`:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Ollama**:
   - Kunjungi [Ollama Download](https://ollama.com/download) untuk mengunduh dan menginstal Ollama sesuai dengan sistem operasi Anda.
5. **Tarik model yang diperlukan** dengan Ollama:
   ```bash
   ollama pull llama3
   ollama pull mxbai-embed-large
   ```
6. **Upload file (PDF, TXT, JSON)** dengan menjalankan `upload.py`:
   ```bash
   python upload.py
   ```
7. **Jalankan demo RAG Lokal** dengan menggunakan `localrag.py`:
   ```bash
   python localrag.py
   ```
   **Note**: Anda dapat menulis query untuk menguji sistem dan mendapatkan respons berbasis dokumen yang diunggah.

## 📖 Apa itu RAG?

**Retrieval-Augmented Generation (RAG)** adalah sebuah arsitektur model dalam **pemrosesan bahasa alami (NLP)** yang menggabungkan dua komponen utama:

1. **Retrieval (Pencarian)**:  
   Proses pencarian dan pengambilan informasi yang relevan dari sumber eksternal seperti basis data, dokumen, atau artikel.

2. **Generation (Pembangunan)**:  
   Setelah mendapatkan informasi yang relevan, model kemudian **menghasilkan jawaban atau respons** berdasarkan informasi yang ditemukan tersebut.

### 🔑 Keuntungan Utama dari RAG:
- **Akurasi lebih tinggi**:  
  Dengan menggunakan pencarian informasi eksternal yang relevan, RAG dapat memberikan jawaban yang lebih **akur** dan **berbasis konteks**.
  
- **Penanganan pertanyaan langka**:  
  RAG mampu menjawab pertanyaan yang memerlukan data yang tidak ada dalam model secara langsung, namun dapat diambil dari **sumber eksternal** yang relevan.

---

## 🧑‍💻 Apa itu Ollama?

**Ollama** adalah sebuah platform **AI** yang memungkinkan interaksi dengan berbagai **Large Language Models (LLMs)** secara langsung. Dengan Ollama, pengguna dapat berkomunikasi dengan model bahasa besar seperti GPT untuk berbagai tujuan, termasuk:

- **Percakapan alami**
- **Penulisan teks**
- **Pemrograman dan debugging**
- **Penerjemahan** dan banyak lagi

Ollama menyediakan antarmuka yang **mudah digunakan**, memungkinkan pengguna untuk mengakses model-model besar tanpa memerlukan konfigurasi rumit. Anda dapat mengunduh dan memulai menggunakan Ollama dengan mengikuti instruksi di [Ollama Website](https://www.ollama.com).

## Perbandingan Mistral dan Llama 3.1

| **Fitur**             | **Mistral**                                   | **Llama 3.1**                                    |
|-----------------------|-----------------------------------------------|--------------------------------------------------|
| **Jenis Model**       | Model bahasa besar (LLM) berbasis GPT-style  | Model bahasa besar (LLM) berbasis Meta's Llama  |
| **Ukuran Model**      | 7B parameter (Mistral 7B)                     | 7B, 13B, dan 30B parameter (Llama 3.1)            |
| **Kecepatan dan Efisiensi** | Mistral dirancang untuk efisiensi dalam pemrosesan cepat | Llama 3.1 lebih berat, membutuhkan lebih banyak daya komputasi |
| **Kemampuan Generasi**| Terbaik dalam dialog dan teks berbasis konteks | Sangat baik dalam konteks percakapan alami dan pemahaman teks panjang |
| **Fokus Penggunaan**  | Dikenal untuk percakapan AI interaktif dan aplikasi chatbot | Lebih fokus pada penelitian NLP dan tugas-tugas bahasa besar |
| **Kemampuan Multi-Tugas** | Mendukung berbagai aplikasi, termasuk chatbots dan analisis teks | Ideal untuk penggunaan dalam penerjemahan dan sintesis teks |
| **Sumber Pengembangan** | Dikembangkan oleh tim Mistral.ai             | Dikembangkan oleh Meta (Facebook)                |
| **Akses dan Ketersediaan** | Tersedia melalui Ollama untuk penggunaan lokal | Tersedia melalui Meta dan platform open-source lainnya |
| **Model Pre-trained** | Pre-trained dengan kemampuan bahasa yang canggih | Pre-trained dengan fokus pada penerjemahan dan analisis teks |
| **Kompatibilitas**    | Dapat dijalankan di berbagai platform dengan Ollama | Dapat dijalankan di berbagai platform dan alat open-source |

---

## 📺 Referensi & Tutorial

- **All About AI** - Channel YouTube untuk tutorial dan pembahasan terkait AI serta teknologi terbaru dalam dunia pembelajaran mesin dan pemrosesan bahasa alami:
  - [YouTube - All About AI](https://www.youtube.com/c/AllAboutAI)

---

Terima kasih telah mencoba demo **RAG Lokal dengan Ollama**! Kami harap demo ini dapat membantu Anda memahami konsep **RAG** dalam pemrosesan bahasa alami dan aplikasinya dalam menjawab pertanyaan berbasis dokumen eksternal.
