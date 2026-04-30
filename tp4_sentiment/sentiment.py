import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL = "tabularisai/multilingual-sentiment-analysis"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

SYMBOLES = {
    "Very Positive": "[++]",
    "Positive":      "[+] ",
    "Neutral":       "[~] ",
    "Negative":      "[-] ",
    "Very Negative": "[--]",
}


def analyser(phrase: str) -> dict:
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": phrase},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"Erreur modèle : {data['error']}")

    resultats = data[0] if isinstance(data, list) and isinstance(data[0], list) else data
    return max(resultats, key=lambda x: x["score"])


def afficher_resultat(phrase: str, resultat: dict) -> None:
    label = resultat["label"]
    score = resultat["score"]
    symbole = SYMBOLES.get(label, "[?] ")
    barre = int(score * 20)
    print(f"\nPhrase    : {phrase}")
    print(f"Sentiment : {symbole} {label}")
    print(f"Confiance : {'█' * barre}{'░' * (20 - barre)} {score:.1%}\n")


def lire_phrase() -> str | None:
    try:
        return input("\nPhrase : ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAu revoir !")
        return None


def traiter_phrase(phrase: str) -> None:
    print("Analyse en cours...", end="\r")
    try:
        resultat = analyser(phrase)
        afficher_resultat(phrase, resultat)
    except requests.HTTPError as e:
        print(f"Erreur HTTP {e.response.status_code} : {e.response.text}")
    except requests.ConnectionError:
        print("Erreur : impossible de joindre l'API.")
    except requests.Timeout:
        print("Erreur : délai d'attente dépassé.")
    except (RuntimeError, ValueError) as e:
        print(f"Erreur : {e}")


def main():
    if not API_KEY:
        print("Erreur : HUGGINGFACE_API_KEY absent dans .env")
        return

    print("=" * 50)
    print("  Analyse de sentiment — Hugging Face")
    print(f"  Modèle : {MODEL}")
    print("  Tapez 'exit' pour quitter le programme.")
    print("=" * 50)

    while True:
        phrase = lire_phrase()
        if phrase is None or phrase.lower() == "exit":
            print("Au revoir !")
            break
        if phrase:
            traiter_phrase(phrase)


if __name__ == "__main__":
    main()
