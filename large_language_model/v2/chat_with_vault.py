import torch
import ollama
import os
import json
from openai import OpenAI  # type: ignore
import argparse
import pygame
from gtts import gTTS
import re

# === File Paths ===
EMBEDDINGS_FILE = "vault_embeddings.json"

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# === Function to Load Saved Embeddings ===
def load_embeddings():
    """Loads precomputed embeddings from vault_embeddings.json."""
    if not os.path.exists(EMBEDDINGS_FILE):
        print("🚨 Embeddings file not found! Run 'embed_vault.py' first.")
        return [], torch.empty((0,))
    
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        embeddings_data = json.load(f)
    
    vault_content = [entry["text"] for entry in embeddings_data]
    vault_embeddings = [entry["embedding"] for entry in embeddings_data]

    if not vault_embeddings:
        print("🚨 No embeddings found in file!")
        return [], torch.empty((0,))

    vault_embeddings_tensor = torch.tensor(vault_embeddings)
    print(f"✅ Loaded {len(vault_embeddings)} embeddings from {EMBEDDINGS_FILE}")
    
    return vault_content, vault_embeddings_tensor

def remove_think_blocks(text):
    """Removes <think>...</think> blocks from the text."""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

# === Function to Clean Text for gTTS ===
def clean_text_for_tts(text):
    """Removes Markdown formatting and line breaks for gTTS."""
    text = re.sub(r'[*_#-]', '', text)  # Remove special characters
    return text.replace("\n", " ").strip()

# === Function for Text-to-Speech (TTS) ===
def speak(text, language="id"):
    """Speaks only the relevant response, ignoring <think> blocks."""
    text = remove_think_blocks(text)  # Remove unwanted <think> content
    if not text.strip():
        print("⚠️ No valid content to speak.")
        return
    
    """Converts text to speech using gTTS."""
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

# === Function to Get Relevant Context for RAG ===
def get_relevant_context(query, vault_embeddings, vault_content, top_k=5):
    """Retrieves relevant document snippets using cosine similarity."""
    if vault_embeddings.nelement() == 0:
        return []
    
    response = ollama.embeddings(model='deepseek-r1', prompt=query)
    input_embedding = response["embedding"]
    
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    
    return [vault_content[idx].strip() for idx in top_indices]

# === Function for Chat with Ollama ===
def chat_with_ollama(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    """Handles conversation with Ollama AI model."""
    conversation_history.append({"role": "user", "content": user_input})

    # Retrieve relevant context
    relevant_context = get_relevant_context(user_input, vault_embeddings, vault_content)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        print("🔍 Konteks yang diambil dari dokumen: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        print(CYAN + "⚠️ Tidak ada konteks yang relevan." + RESET_COLOR)
    
    # Append context to user input
    user_input_with_context = user_input + ("\n\nKonteks relevan:\n" + context_str if relevant_context else "")
    conversation_history[-1]["content"] = user_input_with_context
    
    # Prepare messages for model
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    # Call Ollama for response
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    # Append assistant response to history
    assistant_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_response})
    
    return assistant_response

# === Load Precomputed Embeddings ===
print(NEON_GREEN + "Loading precomputed embeddings..." + RESET_COLOR)
vault_content, vault_embeddings_tensor = load_embeddings()

# === Initialize Ollama API Client ===
print(NEON_GREEN + "Inisialisasi Ollama API client..." + RESET_COLOR)
parser = argparse.ArgumentParser(description="Ollama Chat")
parser.add_argument("--model", default="deepseek-r1", help="Ollama model to use (default: llama3)")
args = parser.parse_args()

client = OpenAI(base_url='http://localhost:11434/v1', api_key='llama3')

# === Start Conversation Loop ===
print("Memulai perbincangan...")
conversation_history = []

system_message = (
    "Anda adalah asisten AI yang memahami dan menganalisis teks dari dokumen pengguna. "
    "Gunakan konteks dari dokumen dan percakapan sebelumnya untuk memberikan jawaban relevan. "
    "Jawablah dalam bahasa pengguna tanpa menerjemahkan kecuali diminta."
)

while True:
    user_input = input(YELLOW + "Ajukan pertanyaan tentang dokumen Anda (atau ketik 'keluar' untuk keluar): " + RESET_COLOR)
    
    if user_input.lower() == 'keluar':
        break
    
    response = chat_with_ollama(user_input, system_message, vault_embeddings_tensor, vault_content, args.model, conversation_history)
    print(NEON_GREEN + "Respon:\n\n" + response + RESET_COLOR)
    
    speak(clean_text_for_tts(response), "id")