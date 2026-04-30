import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OCR_SPACE_API_KEY", "ocr_key")
API_URL = "https://api.ocr.space/parse/image"

EXTENSIONS_AUTORISEES = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".bmp", ".tiff"}


def valider_fichier(chemin: str) -> None:
    if not os.path.isfile(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    _, ext = os.path.splitext(chemin)
    if ext.lower() not in EXTENSIONS_AUTORISEES:
        raise ValueError(f"Extension non supportée : {ext}. Acceptées : {', '.join(EXTENSIONS_AUTORISEES)}")


def extraire_texte(chemin: str) -> str:
    valider_fichier(chemin)

    with open(chemin, "rb") as f:
        response = requests.post(
            API_URL,
            files={"file": (os.path.basename(chemin), f)},
            data={
                "apikey": API_KEY,
                "language": "fre",
                "isOverlayRequired": "false",
                "detectOrientation": "true",
                "scale": "true",
            },
            timeout=30,
        )

    response.raise_for_status()
    data = response.json()

    if data.get("IsErroredOnProcessing"):
        messages = data.get("ErrorMessage", ["Erreur inconnue"])
        raise RuntimeError(f"Erreur OCR : {'; '.join(messages)}")

    resultats = data.get("ParsedResults", [])
    if not resultats:
        return "(Aucun texte détecté)"

    texte = resultats[0].get("ParsedText", "").strip()
    return texte if texte else "(Aucun texte détecté)"


def main():
    print("=" * 50)
    print("      OCR — Extraction de texte (OCR.space)")
    print("  Tapez 'exit' pour quitter le programme.")
    print("=" * 50)
    print(f"\nFormats acceptés : {', '.join(EXTENSIONS_AUTORISEES)}")

    while True:
        try:
            chemin = input("\nChemin de l'image : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            break

        if chemin.lower() == "exit":
            print("Au revoir !")
            break

        if not chemin:
            continue

        chemin = chemin.strip('"').strip("'")

        print("Envoi en cours...", end="\r")
        try:
            texte = extraire_texte(chemin)
            print(f"\nTexte extrait :\n{'-' * 40}\n{texte}\n{'-' * 40}")
        except FileNotFoundError as e:
            print(f"Erreur : {e}")
        except ValueError as e:
            print(f"Erreur : {e}")
        except RuntimeError as e:
            print(f"{e}")
        except requests.HTTPError as e:
            print(f"Erreur HTTP {e.response.status_code} : {e.response.text}")
        except requests.ConnectionError:
            print("Erreur : impossible de joindre l'API.")
        except requests.Timeout:
            print("Erreur : délai d'attente dépassé.")


if __name__ == "__main__":
    main()
