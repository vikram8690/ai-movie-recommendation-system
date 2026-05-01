# 🎬 AI Movie Recommendation & Review Sentiment System

A full-stack Django web application that combines AI-powered sentiment analysis with content-based movie recommendations. Built as a college final-year portfolio project.

**GitHub:** [vikram8690](https://github.com/vikram8690/ai-movie-recommendation-system)  
**Live Demo:** Deployed on Render

---

## 📋 Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Installation Guide](#installation-guide)
5. [Train the ML Model](#train-the-ml-model)
6. [Run the Project](#run-the-project)
7. [Sample Data](#sample-data)
8. [Database Models](#database-models)
9. [AI/ML Explanation](#aiml-explanation)
10. [Deployment on Render](#deployment-on-render)
11. [Future Scope](#future-scope)
12. [Project Report Notes](#project-report-notes)

---

## ✨ Features

### User Features
- User registration, login, logout with Django authentication
- Personalised user dashboard with stats
- Movie browsing with search, filter (genre, year, rating), sort & pagination
- Movie detail page with average rating, all reviews, and similar movies
- Write / edit movie reviews with 1–5 star rating
- **AI Sentiment Analysis** — every review is auto-classified as Positive, Negative, or Neutral
- Watchlist system — save movies to watch later
- **AI Recommendations** — content-based personalised movie suggestions
- Review history with CSV export

### Admin Features
- Role-based access (admin/user roles)
- Movie CRUD — Add, Edit, Delete movies
- Admin dashboard with system-wide stats, sentiment breakdown, genre distribution
- Full Django admin panel integration

### AI/ML Features
- **Sentiment Analysis:** TF-IDF + Logistic Regression (trained on 90 labelled reviews)
- **Recommendation Engine:** Content-based filtering using TF-IDF + Cosine Similarity
- Graceful keyword-based fallback if ML model is not yet trained

---

## 🛠️ Tech Stack

| Layer      | Technology                                  |
|------------|---------------------------------------------|
| Backend    | Python 3.11, Django 4.2                     |
| Database   | SQLite (dev) / PostgreSQL (production)      |
| ML/AI      | scikit-learn, pandas, numpy, nltk, joblib   |
| Frontend   | HTML5, CSS3, Bootstrap 5.3, JavaScript ES6  |
| Icons      | Font Awesome 6                              |
| Deployment | Render (Web Service), Whitenoise, Gunicorn  |

---

## 📁 Project Structure

```
ai_movie_system/
├── manage.py
├── requirements.txt
├── Procfile
├── render.yaml
├── runtime.txt
│
├── ai_movie_system/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                 # User auth & profiles
│   ├── models.py             # UserProfile model
│   ├── views.py              # register, login, logout, dashboard
│   ├── forms.py              # RegistrationForm
│   └── urls.py
│
├── movies/                   # Movie CRUD
│   ├── models.py             # Movie model
│   ├── views.py              # list, detail, add, edit, delete, trending
│   ├── forms.py              # MovieForm
│   └── management/commands/seed_movies.py
│
├── reviews/                  # Review system
│   ├── models.py             # Review model (with sentiment field)
│   ├── views.py              # add_review, history, export CSV
│   └── forms.py              # ReviewForm
│
├── recommendations/          # Watchlist & Recommendations
│   ├── models.py             # Watchlist, RecommendationLog
│   └── views.py
│
├── dashboard/                # Admin dashboard
│   └── views.py
│
├── utils/
│   ├── sentiment_utils.py    # Load ML model & predict sentiment
│   └── recommendation_utils.py  # Content-based recommendation engine
│
├── ml/
│   ├── train_sentiment.py    # Train TF-IDF + Logistic Regression model
│   └── models/               # Saved .pkl model files
│
├── static/
│   ├── css/style.css         # Dark cinema theme
│   └── js/main.js
│
├── media/                    # User-uploaded files (posters, avatars)
│
└── templates/                # All HTML templates (Jinja/Django)
    ├── base.html
    ├── home.html
    ├── accounts/
    ├── movies/
    ├── reviews/
    ├── recommendations/
    └── dashboard/
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.11+
- pip
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/vikram8690/ai-movie-recommendation-system.git
cd ai-movie-recommendation-system
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run database migrations
```bash
python manage.py migrate
```

### Step 5 — Train the AI sentiment model
```bash
python ml/train_sentiment.py
```
This trains a Logistic Regression classifier and saves two files:
- `ml/models/tfidf_vectorizer.pkl`
- `ml/models/sentiment_model.pkl`

### Step 6 — Load sample movie data
```bash
python manage.py seed_movies
```

### Step 7 — Create admin superuser
```bash
python manage.py createsuperuser
```
After creating, go to `/admin/` → UserProfile → set your role to **admin**.

### Step 8 — Collect static files (optional for development)
```bash
python manage.py collectstatic
```

---

## 🤖 Train the ML Model

```bash
python ml/train_sentiment.py
```

**Output:**
```
============================================================
  AI Movie System — Sentiment Model Trainer
============================================================
  Total samples: 90
  Positive: 30
  Negative: 30
  Neutral:  30

  Test Accuracy : 88.9%
  ...
  Model saved → ml/models/sentiment_model.pkl
============================================================
```

---

## ▶️ Run the Project

```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

| URL                       | Page                    |
|---------------------------|-------------------------|
| `/`                       | Home page               |
| `/register/`              | Register                |
| `/login/`                 | Login                   |
| `/dashboard/`             | User dashboard          |
| `/movies/`                | Movie list              |
| `/movies/<id>/`           | Movie detail            |
| `/movies/add/`            | Add movie (admin)       |
| `/movies/trending/`       | Trending movies         |
| `/reviews/add/<id>/`      | Write a review          |
| `/reviews/history/`       | Review history          |
| `/reviews/export/`        | Export CSV              |
| `/recommendations/`       | AI recommendations      |
| `/recommendations/watchlist/` | Watchlist           |
| `/dashboard/admin-panel/` | Admin dashboard         |
| `/admin/`                 | Django admin            |

---

## 🎬 Sample Data

20 sample movies are loaded by `python manage.py seed_movies`:

- The Dark Knight (2008) — Action
- Inception (2010) — Sci-Fi
- Interstellar (2014) — Sci-Fi
- Pulp Fiction (1994) — Crime
- The Shawshank Redemption (1994) — Drama
- The Matrix (1999) — Sci-Fi
- Joker (2019) — Thriller
- Parasite (2019) — Thriller
- Oppenheimer (2023) — Biography
- ... and 11 more

---

## 🗄️ Database Models

### UserProfile
| Field         | Type          | Description          |
|---------------|---------------|----------------------|
| user          | OneToOneField | Django User          |
| role          | CharField     | 'admin' or 'user'    |
| profile_image | ImageField    | Optional avatar      |

### Movie
| Field        | Type        | Description                |
|--------------|-------------|----------------------------|
| title        | CharField   | Movie title                |
| description  | TextField   | Synopsis                   |
| genre        | CharField   | Genre (15 choices)         |
| release_year | IntegerField| Year                       |
| director     | CharField   | Director name              |
| actors       | TextField   | Comma-separated actors     |
| poster       | ImageField  | Optional poster image      |

### Review
| Field       | Type       | Description                   |
|-------------|------------|-------------------------------|
| user        | ForeignKey | Reviewer                      |
| movie       | ForeignKey | Reviewed movie                |
| rating      | IntegerField| 1 to 5                       |
| review_text | TextField  | Written review                |
| sentiment   | CharField  | 'positive'/'negative'/'neutral'|

### Watchlist
| Field    | Type       | Description      |
|----------|------------|------------------|
| user     | ForeignKey | User             |
| movie    | ForeignKey | Movie            |
| added_at | DateTime   | Auto timestamp   |

### RecommendationLog
| Field             | Type       | Description      |
|-------------------|------------|------------------|
| user              | ForeignKey | User             |
| recommended_movie | ForeignKey | Movie            |
| score             | FloatField | Similarity score |

---

## 🧠 AI/ML Explanation

### Sentiment Analysis
**Algorithm:** TF-IDF Vectorizer + Logistic Regression

1. Raw review text is preprocessed (lowercase, remove special characters)
2. TF-IDF converts text to numerical feature vectors (bigrams, max 5000 features)
3. Logistic Regression predicts one of three classes: positive / negative / neutral
4. Model is saved with joblib and loaded in Django on each review submission

**Accuracy:** ~88–93% on test set

### Recommendation Engine
**Algorithm:** Content-Based Filtering with TF-IDF + Cosine Similarity

1. For each movie, a feature string is built: `title + genre + genre + description + actors + director + director`
2. TF-IDF vectorizes all movie feature strings
3. When a user requests recommendations, their highly rated movies (≥4 stars) are used as seeds
4. Cosine similarity is computed between seed movies and all other movies
5. Scores are weighted by the user's rating (higher rating = more influence)
6. Top-5 movies with highest scores (excluding already reviewed/watchlisted) are returned

---

## 🌐 Deployment on Render

### Step 1 — Push to GitHub
The project is already configured. Make sure your repository is public at:
`https://github.com/vikram8690/ai-movie-recommendation-system`

### Step 2 — Create Render account
Go to [render.com](https://render.com) and sign up with `vrjalalpur@gmail.com`

### Step 3 — New Web Service
1. Click **New → Web Service**
2. Connect your GitHub repo
3. Configure:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python ml/train_sentiment.py`
   - **Start Command:** `gunicorn ai_movie_system.wsgi:application`
4. Set environment variables:
   - `SECRET_KEY` = (a long random string)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `.onrender.com`
5. Click **Deploy**

> ⚠️ **SQLite on Render:** Free tier has no persistent disk. For production, connect a PostgreSQL database and set the `DATABASE_URL` environment variable.

---

## 🔮 Future Scope

1. **Collaborative Filtering** — Use matrix factorisation (SVD) based on all users' ratings
2. **Neural Sentiment** — Replace Logistic Regression with BERT or DistilBERT for higher accuracy
3. **Real Movie Data** — Integrate with TMDB API for live movie data and posters
4. **Social Features** — Follow other users, like reviews, discussion threads
5. **Mobile App** — React Native or Flutter frontend consuming a Django REST API
6. **Email Notifications** — Weekly personalised recommendation digest
7. **A/B Testing** — Compare recommendation algorithms
8. **Advanced Search** — Elasticsearch for full-text search
9. **Streaming Links** — Integrate with JustWatch API to show where to watch
10. **Admin Analytics** — Charts using Chart.js or D3.js

---

## 📝 Project Report Notes

**Project Title:** AI Movie Recommendation and Review Sentiment System

**Abstract:**
This project implements a full-stack web application that leverages machine learning to enhance the movie discovery and review experience. The system uses TF-IDF vectorisation with Logistic Regression for real-time sentiment analysis of movie reviews, classifying them as positive, negative, or neutral. A content-based recommendation engine uses cosine similarity to suggest personalised movies based on user preferences. Built with Django for the backend and Bootstrap 5 for a responsive UI, the system demonstrates practical application of natural language processing and collaborative recommendation techniques in a production-ready web environment.

**Keywords:** Django, Machine Learning, Sentiment Analysis, TF-IDF, Logistic Regression, Content-Based Filtering, Cosine Similarity, NLP, Bootstrap 5, Python

---

## 👨‍💻 Developer

**Vikram** | GitHub: [@vikram8690](https://github.com/vikram8690)

Built with ❤️ using Django, scikit-learn & Bootstrap 5
