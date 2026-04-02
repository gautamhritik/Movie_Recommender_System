# 🎬 Movie Recommender System

A content-based movie recommendation system built using machine learning and deployed with Streamlit. The app suggests similar movies based on user selection and displays posters using the TMDB API.

---

## 🚀 Live Demo

🔗 https://movie-recommender-system-ahg.streamlit.app

---

## 🧠 Features

* Content-based movie recommendation
* Fast similarity computation using a precomputed matrix
* Movie poster fetching via TMDB API
* Clean and interactive UI with Streamlit
* Cloud deployment with remote model loading

---

## 🛠️ Tech Stack

* **Python**
* **Pandas, NumPy**
* **Scikit-learn**
* **Streamlit**
* **TMDB API**
* **Google Drive (for large file hosting)**

---

## 📂 Project Structure

```
movie_recommender_system/
│
├── app.py                  # Main Streamlit app
├── movies.pkl              # Movie dataset
├── movies_dict.pkl         # Processed movie dictionary
├── similarity.pkl          # Similarity matrix (hosted externally)
├── requirements.txt        # Dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/movie_recommender_system.git
cd movie_recommender_system
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Run the app locally

```
streamlit run app.py
```

---

## 🔑 Environment Variables

Create a `.streamlit/secrets.toml` file and add:

```
TMDB_API_KEY = "your_tmdb_api_key"
```

---

## 📦 Model Handling

Due to GitHub file size limitations, the similarity matrix is hosted externally and downloaded at runtime using Google Drive.

---

## ⚠️ Notes

* First run may take time due to model download
* Ensure the API key is valid for poster fetching
* App may go to sleep after inactivity (Streamlit free tier)

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Hritik Gautam**

---
