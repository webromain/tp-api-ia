# TP API IA — Python Terminal

4 programmes Python en terminal qui consomment des API d'intelligence artificielle.

## Prérequis

- Python 3.10+
- Un compte [Hugging Face](https://huggingface.co) (gratuit)

## Installation

```bash
pip install requests python-dotenv
```

Copier `.env.example` en `.env` et remplir les clés :

```bash
cp .env.example .env
```

```
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxx
OCR_SPACE_API_KEY=helloworld
```

> Clé Hugging Face : https://huggingface.co/settings/tokens (permission **Make calls to Inference Providers**)

---

## TP 1 — Chatbot IA

Pose une question, obtiens une réponse générée par un LLM.

```bash
python tp1_chatbot/chatbot.py
```

**Modèle :** `openai/gpt-oss-120b` via Hugging Face  
**Commande pour quitter :** `exit`

---

## TP 2 — Traducteur automatique

Traduit un texte d'une langue vers une autre.

```bash
python tp2_traducteur/traducteur.py
```

**API :** MyMemory (gratuite, sans clé)  
**Langues supportées :** `fr`, `en`, `es`, `de`, `it`, `pt`, `ar`, `zh`, `ja`, `ru`  
**Commande pour quitter :** `exit`

---

## TP 3 — OCR : extraction de texte

Extrait le texte présent dans une image.

```bash
python tp3_ocr/ocr.py
```

**API :** OCR.space (clé de test `helloworld` incluse)  
**Formats acceptés :** `.jpg`, `.jpeg`, `.png`, `.gif`, `.pdf`, `.bmp`, `.tiff`  
**Commande pour quitter :** `exit`

---

## TP 4 — Analyse de sentiment

Analyse si une phrase est positive, neutre ou négative.

```bash
python tp4_sentiment/sentiment.py
```

**Modèle :** `tabularisai/multilingual-sentiment-analysis` via Hugging Face  
**Niveaux :** Very Positive · Positive · Neutral · Negative · Very Negative  
**Langues :** français et anglais  
**Commande pour quitter :** `exit`

---

## Sécurité

- Ne jamais committer le fichier `.env`
- Ne jamais faire apparaître une clé API dans le code ou les captures d'écran
- En cas de fuite : révoquer immédiatement sur https://huggingface.co/settings/tokens
