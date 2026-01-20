# model.py


import os
import re
import requests
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY", "").strip()
API_URL = "https://router.huggingface.co/hf-inference/models/sshleifer/distilbart-cnn-12-6"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

# small stopword set
_STOPWORDS = {
    "the","and","is","in","to","of","a","that","it","for","on","as","with","are","was","by","be","this",
    "an","or","from","at","which","but","have","has","not","they","their","its","we","you","i","can",
    "will","these","more","such","also","other","one","all","may","into","however"
}

_sentence_split_re = re.compile(r'(?<=[.!?])\s+')

def _split_sentences(text):
    sents = [s.strip() for s in _sentence_split_re.split(text) if s.strip()]
    if not sents:
        sents = [s.strip() for s in text.splitlines() if s.strip()]

    merged = []
    for s in sents:
        if merged and len(s.split()) < 4:
            merged[-1] += " " + s
        else:
            merged.append(s)
    return merged

def _clean(text):
    text = text.strip()
    if not re.search(r'[.!?]$', text):
        text += '.'
    return text

def _extractive_summary(text, num_sentences=2):
    sents = _split_sentences(text)
    if len(sents) <= num_sentences:
        return _clean(" ".join(sents))

    freq = Counter()
    for s in sents:
        for w in re.findall(r"[A-Za-z']+", s.lower()):
            if w not in _STOPWORDS:
                freq[w] += 1

    scores = []
    for i, s in enumerate(sents):
        score = sum(freq.get(w.lower(), 0) for w in re.findall(r"[A-Za-z']+", s))
        scores.append((score, i))

    top = sorted(scores, reverse=True)[:num_sentences]
    idx = sorted(i for _, i in top)
    return _clean(" ".join(sents[i] for i in idx))

def _call_hf(text):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": 40,
            "max_length": 90
        }
    }
    try:
        r = requests.post(
            API_URL,
            headers={**HEADERS, "Content-Type": "application/json"},
            json=payload,
            timeout=40
        )
        return r.status_code, r.json()
    except Exception:
        return None, None

def summarize_text(text):
    if not text or not text.strip():
        return "Input text is empty."

    # Try Hugging Face first
    if HF_API_KEY:
        status, data = _call_hf(text)
        if status and status < 400 and isinstance(data, list):
            summary = data[0].get("summary_text")
            if summary:
                return _clean(summary)

    # Fallback extractive summary
    return _extractive_summary(text, num_sentences=2)
