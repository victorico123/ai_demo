<!-- # RAG lokal dengan Ollama

## Syarat menjalankan demo
- Python versi 3.12.x
- Git

## Setup
1. git clone https://github.com/victorico123/ai_demo.git
2. cd path/to/dir/large_language_model
3. pip install -r requirements.txt
4. Install [Ollama](https://ollama.com/download) <https://ollama.com/download>
5. ollama pull llama3
6. ollama pull mxbai-embed-large
7. run upload.py (.pdf, .txt, JSON)
8. run localrag.py (with query re-write)

## Apa itu RAG?
RAG (Retrieval-Augmented Generation) adalah arsitektur model dalam pemrosesan bahasa alami (NLP) yang menggabungkan dua komponen utama: retrieval (pencarian) dan generation (pembangunan).

### Cara Kerja RAG:
Retrieval (Pencarian): Model pertama-tama mencari dan mengambil informasi atau dokumen yang relevan dari basis data pengetahuan besar (misalnya, basis data atau dokumen teks).
Generation (Pembangunan): Setelah mendapatkan dokumen relevan, model kemudian menghasilkan jawaban atau respons berdasarkan kombinasi antara query input dan informasi yang diambil, seringkali menggunakan model bahasa seperti GPT.
Keuntungan Utama:
Akurasi lebih tinggi: Dengan mengambil informasi yang relevan dari sumber eksternal, model RAG memberikan jawaban yang lebih akurat dan berbasis konteks.
Penanganan pertanyaan langka: Dapat menjawab pertanyaan atau menghasilkan teks berdasarkan informasi yang tidak langsung disimpan dalam model, tetapi dapat diambil dari sumber eksternal.

## Apa itu olama?
Ollama adalah sebuah platform atau aplikasi yang mengintegrasikan teknologi Large Language Models (LLM) untuk memungkinkan interaksi dengan model-model AI secara langsung. Ollama memungkinkan pengguna untuk berbicara atau berkomunikasi dengan berbagai model bahasa besar untuk berbagai keperluan, seperti percakapan, penulisan teks, pemrograman, dan banyak lagi. https://www.ollama.com.

### Referensi
https://www.youtube.com/c/AllAboutAI -->




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
   cd path/to/dir/large_language_model
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

---

## 📺 Referensi & Tutorial

- **All About AI** - Channel YouTube untuk tutorial dan pembahasan terkait AI serta teknologi terbaru dalam dunia pembelajaran mesin dan pemrosesan bahasa alami:
  - [YouTube - All About AI](https://www.youtube.com/c/AllAboutAI)

---

## 🔧 Kontribusi

Kami menyambut baik kontribusi dari Anda! Jika Anda tertarik untuk berkontribusi dalam proyek ini, Anda dapat melakukan **fork** dan **pull request**. Pastikan untuk menyertakan dokumentasi dan pengujian yang diperlukan jika ada perubahan besar yang dilakukan.

---

Terima kasih telah mencoba demo **RAG Lokal dengan Ollama**! Kami harap demo ini dapat membantu Anda memahami konsep **RAG** dalam pemrosesan bahasa alami dan aplikasinya dalam menjawab pertanyaan berbasis dokumen eksternal.
