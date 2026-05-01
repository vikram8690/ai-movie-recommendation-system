"""
ml/train_sentiment.py

Trains a TF-IDF + Logistic Regression sentiment classifier on a sample
movie review dataset and saves the model artefacts to ml/models/.

Run from the project root:
    python ml/train_sentiment.py

After training, the Django app will automatically use the saved model
in utils/sentiment_utils.py to predict review sentiment.
"""

import os
import sys
import re
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ------------------------------------------------------------------
# Sample labelled review dataset (90 examples: 30 per class)
# ------------------------------------------------------------------
REVIEWS = [
    # ---- POSITIVE ----
    ("This movie was absolutely amazing! The acting was superb and the story kept me on the edge of my seat.", "positive"),
    ("A masterpiece of modern cinema. Beautiful cinematography and outstanding performances throughout.", "positive"),
    ("I loved every single moment of this film. Truly one of the most unforgettable experiences.", "positive"),
    ("One of the best movies I have ever seen. Highly recommend to absolutely everyone.", "positive"),
    ("The story was captivating and the characters were wonderfully developed and relatable.", "positive"),
    ("Exceptional filmmaking at its finest. The director's vision is executed perfectly.", "positive"),
    ("I was completely blown away by the performances. This is exactly why cinema exists.", "positive"),
    ("A beautiful and deeply moving film that stayed with me long after the credits rolled.", "positive"),
    ("Perfect in every single way. The script, the acting, the direction — all absolutely top notch.", "positive"),
    ("This film exceeded all of my expectations. Absolutely phenomenal filmmaking.", "positive"),
    ("The best film of the year without a doubt. A true and genuine cinematic masterpiece.", "positive"),
    ("Gripping, emotional, and technically brilliant from start to finish. A total must-watch.", "positive"),
    ("The acting was so authentic it felt real. I was completely and utterly immersed.", "positive"),
    ("Stunning visuals combined with a powerful story make this film completely unmissable.", "positive"),
    ("I laughed, I cried, I was amazed. This movie has absolutely everything you could want.", "positive"),
    ("Incredibly well-crafted film with memorable and deeply engaging characters throughout.", "positive"),
    ("This is what great cinema looks like. Absolutely loved every frame of this film.", "positive"),
    ("A wonderful and magical journey from start to finish. Cannot recommend it highly enough.", "positive"),
    ("The chemistry between the actors is truly electric. A genuinely brilliant movie.", "positive"),
    ("Mind-blowing film that completely challenges your perspective. Absolutely loved it.", "positive"),
    ("Great movie with an amazing and original storyline and fantastic acting all around.", "positive"),
    ("So good I watched it twice in the same week. A real hidden gem of a film.", "positive"),
    ("The plot twists were incredible and completely unexpected. Kept me guessing till the end.", "positive"),
    ("This film is a true work of art. Every single scene is crafted to absolute perfection.", "positive"),
    ("Outstanding movie that deserves every single bit of praise and recognition it receives.", "positive"),
    ("I was completely absorbed from the very first scene all the way through to the last.", "positive"),
    ("Fantastic performances paired with a brilliant script make this a real winner.", "positive"),
    ("This movie made me feel things I have not felt in the cinema for a very long time.", "positive"),
    ("A touching, powerful and visually gorgeous film. Absolutely stunning in every way.", "positive"),
    ("The best cinematic experience I have had this entire year. Cannot stop thinking about it.", "positive"),

    # ---- NEGATIVE ----
    ("Absolutely terrible. The worst movie I have seen in many years of watching films.", "negative"),
    ("A complete and utter waste of both time and money. Please avoid this film at all costs.", "negative"),
    ("The plot made absolutely no sense and the acting was genuinely painful to watch.", "negative"),
    ("Boring, completely predictable, and thoroughly disappointing from beginning to end.", "negative"),
    ("I wanted to leave the cinema after only the first fifteen frustrating minutes.", "negative"),
    ("A total mess from beginning to end. There is no coherent story whatsoever in this film.", "negative"),
    ("The special effects were cheap and the characters were completely unlikable and flat.", "negative"),
    ("This movie is a direct insult to the audience's intelligence. Truly awful filmmaking.", "negative"),
    ("Poorly written, poorly directed, and poorly acted. An absolute disaster of a film.", "negative"),
    ("One of the worst films I have ever had the misfortune of sitting through.", "negative"),
    ("The dialogue was painfully cringe-worthy and the story was laughably bad throughout.", "negative"),
    ("Nothing about this movie works at all. A total failure on every conceivable level.", "negative"),
    ("I genuinely cannot believe this film got made and released. Absolutely dreadful.", "negative"),
    ("The pacing was horrendous and the plot had more holes than Swiss cheese.", "negative"),
    ("Awful movie. I actually fell completely asleep halfway through the second act.", "negative"),
    ("Derivative, dull, and completely forgettable in every possible way. Do not bother.", "negative"),
    ("The actors seemed just as bored as I was throughout. A genuine disappointment.", "negative"),
    ("How on earth did this film get funded? Utterly pointless and boring throughout.", "negative"),
    ("The worst screenplay I have ever seen adapted into a feature film.", "negative"),
    ("A genuinely nauseating experience from the very start to the bitter end.", "negative"),
    ("This movie is pure garbage. The story made absolutely no sense at all.", "negative"),
    ("Painfully slow and monumentally boring. Not a single interesting or engaging scene.", "negative"),
    ("Bad acting, bad writing, terrible direction all around. Please stay far away.", "negative"),
    ("I want my two hours back. Terrible in every single conceivable way possible.", "negative"),
    ("The plot was so predictable I had correctly guessed the ending after just five minutes.", "negative"),
    ("Terrible movie with the most annoying characters and absolutely no plot whatsoever.", "negative"),
    ("This is genuinely the worst thing I have seen all year. Please avoid at all costs.", "negative"),
    ("Complete disaster. The director clearly had absolutely no idea what they were doing.", "negative"),
    ("Awful and stilted dialogue paired with even worse acting. A true waste of time.", "negative"),
    ("One of the most tedious and dull movies ever made. Completely and utterly unwatchable.", "negative"),

    # ---- NEUTRAL ----
    ("The movie was okay I suppose. Nothing particularly special but not terrible either.", "neutral"),
    ("An average film with some genuinely good moments scattered among some very slow parts.", "neutral"),
    ("I have seen far better movies but I have also seen much worse ones. It is what it is.", "neutral"),
    ("Decent enough for a one-time watch at home. Not particularly memorable though.", "neutral"),
    ("The acting was fine and the story was reasonably engaging for the most part.", "neutral"),
    ("A solid but somewhat unremarkable film. It does what it needs to do and nothing more.", "neutral"),
    ("Some truly impressive scenes but the film overall feels a little flat and uneven.", "neutral"),
    ("Not bad but certainly not great either. A thoroughly middle-of-the-road experience.", "neutral"),
    ("It kept me adequately entertained though I probably will not bother watching it again.", "neutral"),
    ("A reasonable enough way to spend two hours. Neither excellent nor truly terrible.", "neutral"),
    ("The film has its moments but really struggles to maintain any consistency throughout.", "neutral"),
    ("Pretty standard stuff all around. Competent but decidedly uninspired filmmaking.", "neutral"),
    ("There are definitely things to like here but there are also significant and obvious flaws.", "neutral"),
    ("An inoffensive and moderately entertaining film that passes the time just fine.", "neutral"),
    ("Better than I was expecting given the reviews but still not quite what I had hoped for.", "neutral"),
    ("The first half was genuinely great but the second half felt very rushed and unfinished.", "neutral"),
    ("Some strong performances let down significantly by a script that does not match them.", "neutral"),
    ("Watchable but ultimately quite forgettable. I would not go out of my way to see it.", "neutral"),
    ("A real mixed bag of a film. Some genuinely good ideas that are only poorly executed.", "neutral"),
    ("Not the best film and definitely not the worst. Just sort of there.", "neutral"),
    ("An average movie experience overall. Entertaining enough without being at all special.", "neutral"),
    ("It passes the time but offers very little that you have not already seen elsewhere.", "neutral"),
    ("The movie had real potential but ultimately failed to fully deliver on its promises.", "neutral"),
    ("Some fun moments scattered throughout an otherwise quite mediocre and forgettable film.", "neutral"),
    ("Fair enough movie I suppose. Worth a watch if you truly have nothing better to do.", "neutral"),
    ("Neither a hit nor a complete miss. Just sitting somewhere there in the middle.", "neutral"),
    ("The concept was genuinely interesting but the execution was sadly only average.", "neutral"),
    ("A perfectly serviceable film that will not stick with you after the credits roll.", "neutral"),
    ("Gets the job done without being particularly impressive or memorable in any way.", "neutral"),
    ("Nothing groundbreaking here whatsoever but a reasonably solid film nonetheless.", "neutral"),
]


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def train():
    print("=" * 60)
    print("  AI Movie System — Sentiment Model Trainer")
    print("=" * 60)

    # Prepare data
    texts  = [preprocess(r[0]) for r in REVIEWS]
    labels = [r[1] for r in REVIEWS]

    print(f"\n  Total samples: {len(texts)}")
    for cls in ['positive', 'negative', 'neutral']:
        print(f"  {cls.capitalize()}: {labels.count(cls)}")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # TF-IDF vectorisation
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
        stop_words='english',
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)

    # Train Logistic Regression
    model = LogisticRegression(
        max_iter=1000,
        C=1.0,
        solver='lbfgs',
        multi_class='multinomial',
        random_state=42,
    )
    model.fit(X_train_vec, y_train)

    # Evaluate
    y_pred = model.predict(X_test_vec)
    acc    = accuracy_score(y_test, y_pred)
    print(f"\n  Test Accuracy : {acc * 100:.1f}%")
    print("\n  Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save artefacts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir  = os.path.join(script_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)

    vec_path   = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
    model_path = os.path.join(model_dir, 'sentiment_model.pkl')

    joblib.dump(vectorizer, vec_path)
    joblib.dump(model,      model_path)

    print(f"\n  Vectorizer saved → {vec_path}")
    print(f"  Model saved      → {model_path}")
    print("\n  Training complete! The Django app will now use this model.")
    print("=" * 60)


if __name__ == '__main__':
    train()
