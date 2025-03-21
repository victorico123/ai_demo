import torch # type: ignore
import ollama # type: ignore
import os
from openai import OpenAI # type: ignore
import argparse
import json
import pygame
from gtts import gTTS
import re

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

def clean_text_for_tts(text):
    """Membersihkan teks agar lebih cocok untuk gTTS."""
    text = re.sub(r'\*|\_|\#|\-', '', text)  # Menghapus karakter format Markdown
    text = text.replace("\n", " ")  # Menghapus line breaks agar lebih alami
    return text.strip()

def speak(text, language="id"):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        temp_audio = "temp_audio.mp3"
        tts.save(temp_audio)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
        os.remove(temp_audio)
    except Exception as e:
        print("Error:", e)

# Function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Function to get relevant context from the vault based on user input
def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=5):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the rewritten input
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=rewritten_input)["embedding"]
    # Compute cosine similarity between the input and vault embeddings
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

def rewrite_query(user_input_json, conversation_history, ollama_model):
    user_input = json.loads(user_input_json)["Query"]
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-2:]])
    prompt = f"""Tulis ulang pertanyaan/pertanyaan berikut dengan menggabungkan konteks relevan dari riwayat percakapan.
    Pertanyaan/pertanyaan yang ditulis ulang harus:
    
    - Menjaga makna inti dari pertanyaan/pertanyaan asli
    - Memperluas dan memperjelas pertanyaan/pertanyaan agar lebih spesifik dan informatif dalam mengambil konteks yang relevan
    - Menghindari memperkenalkan topik atau pertanyaan/pertanyaan baru yang menyimpang dari pertanyaan/pertanyaan asli
    - JANGAN PERNAH MENJAWAB pertanyaan/pertanyaan asli, tetapi fokuslah untuk menulis ulang dan memperluasnya menjadi pertanyaan/pertanyaan baru
    
    Kembalikan HANYA teks pertanyaan/pertanyaan yang ditulis ulang, tanpa format atau penjelasan tambahan.
    
    Riwayat Percakapan:
    {context}
    
    Pertanyaan/pertanyaan User: [{user_input}]
    
    Pertanyaan/pertanyaan yang Ditulis Ulang: 
    """
    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        temperature=0.1,
    )
    rewritten_query = response.choices[0].message.content.strip()
    return json.dumps({"Rewritten Query": rewritten_query})
   
def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    conversation_history.append({"role": "user", "content": user_input})
    
    if len(conversation_history) > 1:
        query_json = {
            "Query": user_input,
            "Rewritten Query": ""
        }
        rewritten_query_json = rewrite_query(json.dumps(query_json), conversation_history, ollama_model)
        rewritten_query_data = json.loads(rewritten_query_json)
        rewritten_query = rewritten_query_data["Rewritten Query"]
        print(PINK + "Pernyataan asli: " + user_input + RESET_COLOR)
        print(PINK + "Pernyataan yang ditulis ulang: " + rewritten_query + RESET_COLOR)
    else:
        rewritten_query = user_input
    
    relevant_context = get_relevant_context(rewritten_query, vault_embeddings, vault_content)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        print("Konteks yang diambil dari dalam dokumen: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        print(CYAN + "Tidak ada konteks yang relevan." + RESET_COLOR)
    
    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context = user_input + "\n\nKonteks relevan:\n" + context_str
    
    conversation_history[-1]["content"] = user_input_with_context
    
    messages = [
        {"role": "system", "content": system_message + "\n\nHarap berikan jawaban dalam teks biasa, tanpa Markdown atau format khusus lainnya."},
        *conversation_history
    ]
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    
    return response.choices[0].message.content

# Parse command-line arguments
print(NEON_GREEN + "Mengurai argumen setiap baris perintah..." + RESET_COLOR)
parser = argparse.ArgumentParser(description="Ollama Chat")
parser.add_argument("--model", default="llama3", help="Ollama model to use (default: llama3)")
args = parser.parse_args()

# Configuration for the Ollama API client
print(NEON_GREEN + "Inisialisasi Ollama API client..." + RESET_COLOR)
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='llama3'
)

# Load the vault content
print(NEON_GREEN + "Memuat konten dokumen dari vault..." + RESET_COLOR)
vault_content = []
if os.path.exists("vault.txt"):
    with open("vault.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()

# # Generate embeddings for the vault content using Ollama
# print(NEON_GREEN + "Menghasilkan embeddings untuk konten dari vault..." + RESET_COLOR)
# vault_embeddings = []
# for content in vault_content:
#     response = ollama.embeddings(model='deepseek-r1', prompt=content)
#     vault_embeddings.append(response["embedding"])

# Generate embeddings for the vault content using Ollama
print(NEON_GREEN + "Menghasilkan embeddings untuk konten dari vault..." + RESET_COLOR)
vault_embeddings = []
for content in vault_content:
    if (len(content.strip()) > 0):
        print(NEON_GREEN + ">" + content + RESET_COLOR)
        # response = ollama.embeddings(model='deepseek-r1', prompt='')
        response = ollama.embeddings(model='deepseek-r1:7b', prompt=content)
        vault_embeddings.append(response["embedding"])
    else:
        print(NEON_GREEN + "! skip empty line" + RESET_COLOR)

# Convert to tensor and print embeddings
print("Mengubah embeddings menjadi tensor...")
vault_embeddings_tensor = torch.tensor(vault_embeddings) 
print("Embeddings dari setiap bari dalam vault:")
print(vault_embeddings_tensor)

# Conversation loop
print("Memulai perbincangan...")
conversation_history = []
# system_message = "Anda adalah asisten yang membantu dan ahli dalam mengekstraksi informasi paling berguna dari teks tertentu. Juga berikan informasi tambahan yang relevan ke permintaan pengguna dari luar konteks tertentu. Jawablah pertanyaan sesuai dengan bahasa dari pertanyaan yang diajukan."
# system_message = "Anda adalah asisten cerdas yang ahli dalam mengekstraksi informasi paling relevan dari teks tertentu. Selain itu, Anda juga memberikan informasi tambahan yang berguna sesuai dengan permintaan pengguna, termasuk dari sumber luar konteks utama. Jawablah setiap pertanyaan dalam bahasa yang digunakan oleh pengguna dalam pertanyaannya."
system_message = (
    "Anda adalah asisten AI yang dirancang untuk memahami dan menganalisis teks dari dokumen pengguna. "
    "Gunakan konteks dari dokumen dan percakapan sebelumnya untuk memberikan jawaban yang relevan dan informatif. "
    "Jawablah dalam bahasa yang sama dengan pertanyaan pengguna tanpa menerjemahkan kecuali diminta. "
    "Pastikan respons tetap alami dan mudah dipahami, tanpa karakter tambahan yang tidak diperlukan."
)

while True:
    user_input = input(YELLOW + "berikan pertanyaan mengenai dokumen anda (atau ketik 'keluar' untuk keluar): " + RESET_COLOR)
    if user_input.lower() == 'keluar':
        break
    
    response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, args.model, conversation_history)
    print(NEON_GREEN + "Respon: \n\n" + response + RESET_COLOR)
    speak(clean_text_for_tts(response), "id")

