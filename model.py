import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- AI DETECTOR ----------------

def detect_ai_text(text):

    if not text.strip():
        return {"ai": 0, "human": 0, "explanation": "No text provided"}

    words = text.split()
    sentences = re.split(r'[.!?]+', text)

    avg_word_len = np.mean([len(w) for w in words]) if words else 0
    sentence_var = np.std([len(s.split()) for s in sentences if s.strip()]) if sentences else 0

    ai_score = min(100, int(avg_word_len * 5 + sentence_var * 2))
    human_score = 100 - ai_score

    explanation = f"Avg word length: {avg_word_len:.2f}, Sentence variation: {sentence_var:.2f}"

    return {
        "ai": ai_score,
        "human": human_score,
        "explanation": explanation
    }

# ---------------- PLAGIARISM ----------------

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

def plagiarism_score(text1, text2):

    text1 = preprocess(text1)
    text2 = preprocess(text2)

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([text1, text2])

        score = cosine_similarity(vectors[0], vectors[1])[0][0]
        return round(score * 100, 2)

    except:
        return 0

# ---------------- MATCHES ----------------

def get_matches(text1, text2):

    s1_list = [s.strip() for s in re.split(r'[.!?]', text1) if s.strip()]
    s2_list = [s.strip() for s in re.split(r'[.!?]', text2) if s.strip()]

    matches = []

    for s1 in s1_list:
        for s2 in s2_list:
            score = sentence_similarity(s1, s2)
            if score > 0.5:
                matches.append([s1, s2, round(score * 100, 2)])

    return matches

def sentence_similarity(s1, s2):
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([s1, s2])
        return cosine_similarity(vectors[0], vectors[1])[0][0]
    except:
        return 0