# RAG lokal dengan Ollama

## Setup
1. git clone https://github.com/AllAboutAI-YT/easy-local-rag.git
2. cd dir
3. pip install -r requirements.txt
4. Install Ollama (https://ollama.com/download)
5. ollama pull llama3 (etc)
6. ollama pull mxbai-embed-large
7. run upload.py (pdf, .txt, JSON)
8. run localrag.py (with query re-write)
9. run localrag_no_rewrite.py (no query re-write)

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
https://www.youtube.com/c/AllAboutAI