"""
utils/sentiment_utils.py

Sentiment prediction utility.
Loads the trained TF-IDF + Logistic Regression model from disk.
Falls back to a simple keyword-based classifier if the model file is missing
(e.g., before `python ml/train_sentiment.py` has been run).
"""

import os
import re

# Path to saved model files
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR    = os.path.join(BASE_DIR, 'ml', 'models')
VECTORIZER_F = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
MODEL_F      = os.path.join(MODEL_DIR, 'sentiment_model.pkl')


def _preprocess(text: str) -> str:
    """Lowercase and strip non-alphabetic characters."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _keyword_fallback(text: str) -> str:
    """
    Very simple rule-based sentiment.
    Used when the ML model has not been trained yet.
    """
    positive_words = {
        'great', 'amazing', 'excellent', 'wonderful', 'fantastic', 'love', 'best',
        'awesome', 'brilliant', 'superb', 'outstanding', 'perfect', 'beautiful',
        'incredible', 'stunning', 'masterpiece', 'enjoyed', 'thrilling', 'impressive',
        'magnificent', 'exceptional', 'loved', 'favorite', 'heartwarming', 'inspiring',
    }
    negative_words = {
        'terrible', 'awful', 'bad', 'horrible', 'hate', 'worst', 'boring',
        'disappointing', 'poor', 'waste', 'dreadful', 'pathetic', 'garbage',
        'unwatchable', 'painful', 'atrocious', 'mediocre', 'overrated', 'confusing',
        'frustrating', 'annoying', 'dull', 'slow', 'predictable', 'pointless',
    }
    words  = set(_preprocess(text).split())
    pos_ct = len(words & positive_words)
    neg_ct = len(words & negative_words)

    if pos_ct > neg_ct:
        return 'positive'
    if neg_ct > pos_ct:
        return 'negative'
    return 'neutral'


def predict_sentiment(text: str) -> str:
    """
    Predict the sentiment of a review text.
    Returns 'positive', 'negative', or 'neutral'.
    """
    if not text or not text.strip():
        return 'neutral'

    # Try ML model first
    if os.path.exists(VECTORIZER_F) and os.path.exists(MODEL_F):
        try:
            import joblib
            vectorizer = joblib.load(VECTORIZER_F)
            model      = joblib.load(MODEL_F)
            processed  = _preprocess(text)
            features   = vectorizer.transform([processed])
            prediction = model.predict(features)[0]
            return str(prediction)
        except Exception:
            pass  # Fall through to keyword fallback

    return _keyword_fallback(text)
