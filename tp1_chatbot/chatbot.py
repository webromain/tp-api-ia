import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL = "openai/gpt-oss-120b"
API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

historique = []


def ask(question: str) -> str:
    historique.append({"role": "user", "content": question})

    payload = {
        "model": MODEL,
        "messages": historique,
        "max_tokens": 512,
        "temperature": 0.7,
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    reponse = data["choices"][0]["message"]["content"].strip()
    historique.append({"role": "assistant", "content": reponse})
    return reponse


def lire_question() -> str | None:
    try:
        return input("\nVous : ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAu revoir !")
        return None


def traiter_question(question: str) -> None:
    print("Bot : (en cours...)", end="\r")
    try:
        reponse = ask(question)
        print(f"Bot : {reponse}          ")
    except requests.HTTPError as e:
        print(f"Erreur HTTP {e.response.status_code} : {e.response.text}")
    except requests.ConnectionError:
        print("Erreur : impossible de joindre l'API.")
    except requests.Timeout:
        print("Erreur : délai d'attente dépassé.")
    except (KeyError, IndexError):
        print("Erreur : format de réponse inattendu.")


def main():
    if not API_KEY:
        print("Erreur : HUGGINGFACE_API_KEY absent dans .env")
        return

    print("=" * 50)
    print("       Chatbot IA — Hugging Face")
    print(f"       Modèle : {MODEL}")
    print("  Tapez 'exit' pour quitter le programme.")
    print("=" * 50)

    while True:
        question = lire_question()
        if question is None or question.lower() == "exit":
            print("Au revoir !")
            break
        if question:
            traiter_question(question)


if __name__ == "__main__":
    main()
