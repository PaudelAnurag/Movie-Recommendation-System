import streamlit as st
import joblib
import requests
from st_keyup import st_keyup
from dotenv import load_dotenv
import os


load_dotenv()

TMDB_API = os.getenv("TMDB_API")

# =====================
# LOAD ARTIFACTS
# =====================
movies = joblib.load("../artifacts/model/movies.pkl")
vectors = joblib.load("../artifacts/model/vectors.pkl")
model = joblib.load("../artifacts/model/nn_model.pkl")
index_map = joblib.load("../artifacts/model/index_map.pkl")

# =====================
# STREAMLIT CONFIG
# =====================
st.set_page_config(layout="wide")

# =====================
# SESSION STATE
# =====================
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None
if "show_recommendations" not in st.session_state:
    st.session_state.show_recommendations = False
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# =====================
# TMDB POSTER FETCH
# =====================
def fetch_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}"
    params = {"api_key": TMDB_API, "language": "en-US"}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/original{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image"

# =====================
# SEARCH FUNCTION
# =====================
def get_suggestions(query):
    if not query or len(query) < 3:
        return []
    mask = movies['title'].str.lower().str.contains(query.lower(), na=False)
    return movies[mask][['title', 'id']].head(5).values.tolist()

# =====================
# RECOMMENDER
# =====================
def recommend(movie_name):
    idx = index_map[movie_name]
    distances, indices = model.kneighbors(vectors[idx], n_neighbors=10)
    results = []
    for i, dist in zip(indices[0][1:], distances[0][1:]):
        row = movies.iloc[i]
        results.append({
            "title": row['title'],
            "id": row['id'],
            "score": round(1 - dist, 2)
        })
    return results

# =====================
# CSS
# =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0a;
}

/* ── Dark input box ── */
div[data-testid="stTextInput"] input,
input[type="text"] {
    background-color: #1a1a1a !important;
    color: #fff !important;
    border: 1.5px solid #333 !important;
    border-radius: 8px !important;
    padding: 14px 18px !important;
    font-size: 16px !important;
    caret-color: #e50914;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 2px rgba(229,9,20,0.2) !important;
}

/* ── Hide the ugly Streamlit buttons completely ── */
.card-btn-wrapper > div[data-testid="stButton"] {
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    z-index: 10;
}
.card-btn-wrapper > div[data-testid="stButton"] button {
    width: 100%;
    height: 100%;
    cursor: pointer;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ── Card wrapper ── */
.card-outer {
    position: relative;
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
    border: 1.5px solid #2a2a2a;
    background: #141414;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}
.card-outer:hover {
    transform: translateY(-6px) scale(1.03);
    border-color: #e50914;
    box-shadow: 0 8px 28px rgba(229,9,20,0.4);
}
.card-outer img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}
.card-title {
    padding: 8px 8px 10px;
    font-size: 12px;
    font-weight: 600;
    color: #ccc;
    text-align: center;
    line-height: 1.4;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ── Selected banner ── */
.selected-banner {
    display: flex;
    align-items: center;
    gap: 20px;
    background: #141414;
    border: 1.5px solid #e50914;
    border-radius: 12px;
    padding: 16px 22px;
    margin: 20px 0 4px;
}
.selected-banner img {
    width: 64px;
    height: 90px;
    object-fit: cover;
    border-radius: 6px;
    flex-shrink: 0;
}
.selected-label {
    font-size: 10px;
    color: #e50914;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}
.selected-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #fff;
}

/* ── Recommend button ── */
div[data-testid="stButton"].rec-btn > div > button {
    background: #e50914 !important;
    color: white !important;
    border: none !important;
    padding: 10px 28px !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    margin-top: 10px;
    transition: background 0.2s;
}
div[data-testid="stButton"].rec-btn > div > button:hover {
    background: #b0060f !important;
}

/* ── Rec cards ── */
.rec-card {
    background: #141414;
    border: 1.5px solid #2a2a2a;
    border-radius: 10px;
    overflow: hidden;
    text-align: center;
    transition: transform 0.18s, border-color 0.18s;
}
.rec-card:hover {
    transform: translateY(-4px);
    border-color: #444;
}
.rec-card img {
    width: 100%;
    height: 220px;
    object-fit: cover;
}
.rec-card-body { padding: 10px 8px 12px; }
.rec-card-title {
    font-size: 12.5px;
    font-weight: 600;
    color: #ddd;
    margin-bottom: 5px;
    line-height: 1.3;
}
.rec-score {
    font-size: 12px;
    color: #e50914;
    font-weight: 700;
}

.section-divider {
    border: none;
    border-top: 1px solid #222;
    margin: 24px 0;
}

.page-title { font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 2px; }
.page-sub   { color: #666; font-size: 0.9rem; margin-bottom: 24px; }
</style>
""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown('<div class="page-title"> Netflix Style Movie Search</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Search any movie and discover similar titles</div>', unsafe_allow_html=True)

# =====================
# LIVE INPUT
# =====================
query = st_keyup(
    "Search",
    placeholder="e.g. Dark Knight...",
    debounce=200,
    key="search_query",
    label_visibility="collapsed"
)

# Reset on new query
if query != st.session_state.last_query:
    st.session_state.selected_movie = None
    st.session_state.selected_id = None
    st.session_state.show_recommendations = False
    st.session_state.last_query = query

# =====================
# SUGGESTION CARDS
# =====================
suggestions = get_suggestions(query) if not st.session_state.selected_movie else []

if suggestions:
    cols = st.columns(len(suggestions))
    for col, (title, id) in zip(cols, suggestions):
        poster = fetch_poster(id)
        with col:
            # Render card HTML
            st.markdown(f"""
                <div class="card-outer">
                    <img src="{poster}" alt="{title}"/>
                    <div class="card-title">{title}</div>
                </div>
            """, unsafe_allow_html=True)

            # Invisible button on top via wrapper class
            st.markdown('<div class="card-btn-wrapper">', unsafe_allow_html=True)
            if st.button("select", key=f"pick_{id}", use_container_width=True):
                st.session_state.selected_movie = title
                st.session_state.selected_id = id
                st.session_state.show_recommendations = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif query and len(query) >= 3 and not st.session_state.selected_movie:
    st.warning("No movies found. Try a different search.")

# =====================
# SELECTED BANNER
# =====================
if st.session_state.selected_movie:
    poster = fetch_poster(st.session_state.selected_id)
    st.markdown(f"""
        <div class="selected-banner">
            <img src="{poster}" alt="{st.session_state.selected_movie}"/>
            <div>
                <div class="selected-label">Selected Movie</div>
                <div class="selected-title">{st.session_state.selected_movie}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rec-btn">', unsafe_allow_html=True)
    if st.button(" Get Recommendations"):
        st.session_state.show_recommendations = True
    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# RECOMMENDATION CARDS
# =====================
# =====================
# RECOMMENDATION CARDS
# =====================
if st.session_state.show_recommendations and st.session_state.selected_movie:
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    st.markdown(f"### Recommendations for **{st.session_state.selected_movie}**")

    results = recommend(st.session_state.selected_movie)

    # 🔥 FILTER OUT INVALID POSTERS
    filtered_results = []
    for rec in results:
        poster_url = fetch_poster(rec["id"])
        
        # skip placeholder posters
        if "via.placeholder.com" not in poster_url:
            filtered_results.append((rec, poster_url))

        if len(filtered_results) == 5:
            break

    cols = st.columns(len(filtered_results))

    for col, (rec, poster) in zip(cols, filtered_results):
        with col:
            st.markdown(f"""
                <div class="rec-card">
                    <img src="{poster}" alt="{rec['title']}"/>
                    <div class="rec-card-body">
                        <div class="rec-card-title">{rec['title']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)