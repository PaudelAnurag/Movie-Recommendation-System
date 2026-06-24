# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests similar movies based on textual similarity of movie metadata.

---
## 🚀 Live Demo

👉 Try the app here:  
https://movierecommendsystem-mrs.streamlit.app/

## 📌 Project Overview

This project works with a dataset containing **24 columns**. From these, we selected the most relevant features for recommendation:

- `id`
- `title`
- `overview`
- `tagline`
- `genres`
- `keywords`
- `production_companies`

We then combined all selected features (excluding `id` and `title`) into a single text field to create a new processed dataset:

new_df = id + title + combined_text_features


---

## 🧠 Feature Engineering

We merged the following text-based columns:

- overview  
- tagline  
- genres  
- keywords  
- production_companies  

This helps the model understand semantic similarity between movies based on their descriptions and metadata.

---

## ⚙️ Text Vectorization

We used **TF-IDF (Term Frequency - Inverse Document Frequency)** to convert text data into numerical vectors.

- `max_features = 5000`
- Only top 5000 most relevant words are considered
- Reduces noise and improves performance

---

## 🤖 Recommendation Model

We used **K-Nearest Neighbors (KNN)** for similarity search.

- Algorithm: KNN (Cosine Similarity)
- Number of neighbors: **6**
- Output: Top 6 most similar movies for a given input movie

---

## 🚀 How It Works

1. Load dataset (24 columns)
2. Select important features
3. Merge text fields into a single feature
4. Apply TF-IDF vectorization (`max_features=5000`)
5. Compute similarity using KNN
6. Recommend top 6 similar movies

---

## 📊 Example Output

When a movie is selected, the system returns:

- Movie titles
- Similarity-based ranking
- Content-based recommendations (not user ratings)

---

## 🛠️ Tech Stack

- Python 
- Pandas
- Scikit-learn
- TF-IDF Vectorizer
- K-Nearest Neighbors

---

## 📈 Future Improvements

- Add collaborative filtering
- Use deep learning embeddings (Word2Vec / BERT)
- Improve NLP preprocessing (lemmatization, stemming)

---

## 📌 Note

This is a **content-based recommendation system**, which recommends movies based on metadata similarity rather than user preferences or ratings.

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to contribute!
