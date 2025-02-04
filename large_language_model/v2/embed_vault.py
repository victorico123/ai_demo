import torch
import ollama
import os
import json

# === File Paths ===
VAULT_FILE = "vault.txt"
EMBEDDINGS_FILE = "vault_embeddings.json"

# === Function to Load Existing Embeddings ===
def load_existing_embeddings():
    """Loads previously saved embeddings from vault_embeddings.json."""
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# === Function to Generate & Save Only New Embeddings ===
def update_embeddings():
    """Checks for new lines in vault.txt and only embeds new content."""
    
    # Load vault content
    if not os.path.exists(VAULT_FILE):
        print("🚨 Vault file not found! Please create 'vault.txt'.")
        return

    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        vault_content = [line.strip() for line in f.readlines() if line.strip()]

    if not vault_content:
        print("🚨 Vault file is empty!")
        return

    # Load existing embeddings
    existing_data = load_existing_embeddings()
    existing_texts = {entry["text"] for entry in existing_data}  # Convert to set for fast lookup

    new_data = []
    for content in vault_content:
        if content not in existing_texts:  # Only process new entries
            try:
                print(f"📄 Generating embedding for: {content[:50]}...")
                response = ollama.embeddings(model='deepseek-r1', prompt=content)
                embedding = response.get("embedding")

                if embedding:
                    new_data.append({"text": content, "embedding": embedding})
                else:
                    print(f"⚠️ Failed to generate embedding for: {content[:50]}")
            except Exception as e:
                print(f"❌ Error generating embedding: {e}")

    if new_data:
        # Append new embeddings to the existing data
        updated_data = existing_data + new_data
        with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_data, f)

        print(f"✅ Added {len(new_data)} new embeddings to {EMBEDDINGS_FILE}")
    else:
        print("✅ No new data to embed. Vault is up-to-date.")

if __name__ == "__main__":
    update_embeddings()
