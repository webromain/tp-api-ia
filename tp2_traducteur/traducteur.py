import requests

API_URL = "https://api.mymemory.translated.net/get"

LANGUES = {
    "fr": "Français",
    "en": "Anglais",
    "es": "Espagnol",
    "de": "Allemand",
    "it": "Italien",
    "pt": "Portugais",
    "ar": "Arabe",
    "zh": "Chinois",
    "ja": "Japonais",
    "ru": "Russe",
}


def traduire(texte: str, lang_source: str, lang_cible: str) -> str:
    params = {
        "q": texte,
        "langpair": f"{lang_source}|{lang_cible}",
    }
    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data.get("responseStatus") != 200:
        message = data.get("responseDetails", "Erreur inconnue")
        raise ValueError(f"Erreur API : {message}")

    traduction = data["responseData"]["translatedText"]

    if traduction.upper() == texte.upper():
        raise ValueError("Paire de langues non reconnue ou texte identique.")

    return traduction


def afficher_langues():
    print("\nCodes de langue disponibles :")
    for code, nom in LANGUES.items():
        print(f"  {code} → {nom}")
    print()


def main():
    print("=" * 50)
    print("    Traducteur automatique — MyMemory API")
    print("  Tapez 'exit' pour quitter le programme.")
    print("=" * 50)
    afficher_langues()

    while True:
        try:
            texte = input("Texte à traduire : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            break

        if texte.lower() == "exit":
            print("Au revoir !")
            break

        if not texte:
            continue

        source = input("Langue source (ex: fr) : ").strip().lower()
        if source == "exit":
            print("Au revoir !")
            break

        cible = input("Langue cible  (ex: en) : ").strip().lower()
        if cible == "exit":
            print("Au revoir !")
            break

        try:
            traduction = traduire(texte, source, cible)
            print(f"\nTraduction ({source} → {cible}) : {traduction}\n")
        except requests.HTTPError as e:
            print(f"Erreur HTTP {e.response.status_code} : {e.response.text}\n")
        except requests.ConnectionError:
            print("Erreur : impossible de joindre l'API.\n")
        except requests.Timeout:
            print("Erreur : délai d'attente dépassé.\n")
        except ValueError as e:
            print(f"{e}\n")


if __name__ == "__main__":
    main()
