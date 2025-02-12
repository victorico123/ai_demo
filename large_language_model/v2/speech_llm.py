import ollama
import os
import argparse
import pygame
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI

# ANSI escape codes for colors
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Initialize Recognizer
recognizer = sr.Recognizer()

def clean_text_for_tts(text):
    """Removes Markdown formatting (like asterisks) and line breaks for gTTS."""
    text = text.replace('*', '')  # Remove asterisks used for bold/italic
    return text.replace("\n", ". ").strip()

def speak(text, language="id"):
    """Converts text to speech using gTTS with better intonation."""
    text = text.replace(',', ', ').replace('.', '. ')  # Add spacing for better pauses
    text = text.replace(':', ': ').replace('?', '? ')  # Improve phrasing
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

def chat_with_ollama(user_input, system_message, llm_model, conversation_history):
    """Handles conversation with Ollama AI model."""
    conversation_history.append({"role": "user", "content": user_input})
    
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    response = client.chat.completions.create(
        model=llm_model,
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
                
                response = chat_with_ollama(text, system_message, args.model, conversation_history)
                print(NEON_GREEN + "Respon:\n\n" + response + RESET_COLOR)
                speak(clean_text_for_tts(response), "id")
            except sr.UnknownValueError:
                print("❌ Sorry, I couldn't understand that.")
            except sr.RequestError:
                print("❌ Could not request results from Google STT.")

# Initialize Ollama Client
print(NEON_GREEN + "Inisialisasi Ollama API client..." + RESET_COLOR)
parser = argparse.ArgumentParser(description="Ollama Chat")
parser.add_argument("--model", default="llama3.2:3b", help="Ollama model to use")
args = parser.parse_args()
client = OpenAI(base_url='http://localhost:11434/v1', api_key='llama3')

# Start Speech Recognition Mode
conversation_history = []
system_message = "Anda adalah asisten AI yang memberikan jawaban sangat singkat, jelas, dan informatif tanpa tambahan detail yang tidak perlu"
recognize_speech()
