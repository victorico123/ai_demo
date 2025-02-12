import torch
import ollama
import os
import json
import argparse
import pygame
import speech_recognition as sr
from gtts import gTTS
import re
from openai import OpenAI

# === File Paths ===
EMBEDDINGS_FILE = "vault_embeddings.json"

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Initialize Recognizer
recognizer = sr.Recognizer()

def load_embeddings():
    """Loads precomputed embeddings."""
    if not os.path.exists(EMBEDDINGS_FILE):
        print("🚨 Embeddings file not found! Run 'embed_vault.py' first.")
        return [], torch.empty((0,))
    
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        embeddings_data = json.load(f)
    
    vault_content = [entry["text"] for entry in embeddings_data]
    vault_embeddings = [entry["embedding"] for entry in embeddings_data]
    
    return vault_content, torch.tensor(vault_embeddings) if vault_embeddings else torch.empty((0,))

def clean_text_for_tts(text):
    """Removes Markdown formatting and line breaks for gTTS."""
    text = re.sub(r'[*_#-]', '', text)
    return text.replace("\n", " ").strip()

def speak(text, language="id"):
    """Converts text to speech using gTTS."""
    if not text.strip():
        print("⚠️ No valid content to speak.")
        return
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

def get_relevant_context(query, vault_embeddings, vault_content, top_k=5):
    """Retrieves relevant document snippets using cosine similarity."""
    if vault_embeddings.nelement() == 0:
        return []
    
    response = ollama.embeddings(model='deepseek-r1:7b', prompt=query)
    input_embedding = response["embedding"]
    
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_indices = torch.topk(cos_scores, k=min(top_k, len(cos_scores)))[1].tolist()
    
    return [vault_content[idx].strip() for idx in top_indices]

def chat_with_ollama(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    """Handles conversation with Ollama AI model."""
    conversation_history.append({"role": "user", "content": user_input})

    relevant_context = get_relevant_context(user_input, vault_embeddings, vault_content)
    user_input_with_context = user_input + ("\n\nKonteks relevan:\n" + "\n".join(relevant_context) if relevant_context else "")
    conversation_history[-1]["content"] = user_input_with_context
    
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    assistant_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_response})
    
    return assistant_response

def recognize_speech():
    """Continuously listens for speech and processes it."""
    print("🎤 Say something (say 'hentikan program' to exit)...")
    while True:
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source)
                print("🔴 Listening...")
                audio = recognizer.listen(source)
                print("⏳ Recognizing...")
                text = recognizer.recognize_google(audio, language='id-ID').lower()
                print(f"✅ You said: {text}")
                
                if "hentikan program" in text:
                    print("🛑 Stopping the program...")
                    break
                
                response = chat_with_ollama(text, system_message, vault_embeddings_tensor, vault_content, args.model, conversation_history)
                print(NEON_GREEN + "Respon:\n\n" + response + RESET_COLOR)
                speak(clean_text_for_tts(response), "id")
            except sr.UnknownValueError:
                print("❌ Sorry, I couldn't understand that.")
            except sr.RequestError:
                print("❌ Could not request results from Google STT.")

# Load Embeddings
print(NEON_GREEN + "Loading precomputed embeddings..." + RESET_COLOR)
vault_content, vault_embeddings_tensor = load_embeddings()

# Initialize Ollama Client
print(NEON_GREEN + "Inisialisasi Ollama API client..." + RESET_COLOR)
parser = argparse.ArgumentParser(description="Ollama Chat")
parser.add_argument("--model", default="deepseek-r1:7b", help="Ollama model to use")
args = parser.parse_args()
client = OpenAI(base_url='http://localhost:11434/v1', api_key='llama3')

# Start Speech Recognition Mode
conversation_history = []
system_message = (
    "Anda adalah asisten AI yang memahami dan menganalisis teks dari dokumen pengguna. "
    "Gunakan konteks dari dokumen dan percakapan sebelumnya untuk memberikan jawaban relevan. "
    "Jawablah dalam bahasa pengguna tanpa menerjemahkan kecuali diminta."
)
recognize_speech()
