# 🛒 AI E-commerce Data Agent

An intelligent, interactive agent powered by LLMs that enables users to ask natural language questions about e-commerce data — and get back insights via charts, tables, and textual summaries. Built using **Gemini Pro**, **Flask**, **SQLite**, and a modern **Streamlit UI** with user login.
---
## 🎥 Demo Video

[Click here to watch the demo video](https://drive.google.com/drive/folders/1jgusrHDn2iyPf9SViGW5PA43Ti4wAagD)


## 📁 Project Structure

```
ai-ecommerce-agent/
├── app/                    ← Core logic & backend
│   ├── gemini_connector.py        # LLM connection (Gemini API)
│   ├── api.py                     # Flask API to serve queries
│   ├── db_loader.py               # Loads CSV into SQLite
│   ├── list_models.py             # (Optional) Model registry
│   ├── main.py                    # Startup script
│   ├── query_engine.py            # Converts question → SQL → Answer
│   └── visualizer.py              # Generates charts from results
│
├── charts/                 ← Saved/generated charts
├── data/                   ← 3 cleaned CSV datasets
├── database/
│   ├── ecommerce.db               # SQLite database
│   └── inspect_db.py             # Explore schema
│
├── streamlit_ui/           ← Frontend UI (Streamlit)
│   ├── animations/
│   │   └── lottie_animation.json  # Optional animation
│   ├── app.py                     # Streamlit main UI
│   ├── auth.utils.py              # Login logic
│   ├── user_store.py              # User storage backend
│   └── users.json                 # User credentials (JSON)
│
├── .env                    ← API keys (Gemini)
├── main.py                 ← Entry point for backend
├── readme.md
└── requirements.txt        ← Python dependencies
```

---

## 🚀 Features

- 🌐 **Ask questions in natural language** (e.g., “What are the top 5 products by revenue?”)
- 📊 **Visualize answers** using Plotly charts
- 🧠 **LLM-powered SQL generation** via Gemini Pro
- 🔒 **User authentication system** (login, register)
- 🧩 **Modular Flask backend + Streamlit frontend**
- 💾 Local database with real-time querying

---

## 🛣️ Project Roadmap

| Stage | Description |
|-------|-------------|
| ✅ Stage 1 | Preprocess CSV datasets and create a clean SQLite schema |
| ✅ Stage 2 | Develop `query_engine.py` to convert questions → SQL → result |
| ✅ Stage 3 | Integrate Gemini via `gemini_connector.py` |
| ✅ Stage 4 | Build Flask backend with `/ask` endpoint |
| ✅ Stage 5 | Enable visualizations with `visualizer.py` |
| ✅ Stage 6 | Create secure user login (JSON-based) |
| ✅ Stage 7 | Build Streamlit UI (`app.py`) with animations |
| ✅ Stage 8 | Blend visualizations and tabular output in UI |

---

## 🧪 Example Questions

Try these in the UI:

- **“Show total sales trend over time”**
- **“Compare ad sales vs ad spend by date”**
- **“Plot top 5 items by impressions”**
- **“What are the trends of clicks over time?”**
- **“Which items have the highest click-through rate (CTR)?”**
- **“Plot total sales, clicks, and CTR trends by date”**
- **“Show return rate by product category”**
- **“Compare cost per click (CPC) across campaigns”**

---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/Sanjuu2004/Ecommerce_AI_Agent
cd Ecommerce_AI_Agent
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add `.env`
Create a `.env` file with your [Gemini API key](https://aistudio.google.com/app/apikey):

```
GEMINI_API_KEY=your-gemini-api-key
```

### 4️⃣ Load CSVs into SQLite
```bash
cd app
python db_loader.py
```

### 5️⃣ Start Backend (Flask API)
```bash
cd app
python main.py
```
Runs at `http://127.0.0.1:5000`

### 6️⃣ Run Frontend (Streamlit UI)
In another terminal:
```bash
cd streamlit_ui
streamlit run app.py
```

---

## 🖼️ Sample UI

- Animated Lottie welcome
- Login screen
- Natural language input box
- Response section: ✨ Answer + 📊 Chart (if any)

---

## 📤 Deployment Guide

1. **Streamlit Cloud**: Deploy `streamlit_ui/app.py`
2. **Flask API**:
   - Use [Ngrok](https://ngrok.com/) to expose local backend:
     ```bash
     ngrok http 5000
     ```
   - Update the API URL in `app.py` to the Ngrok public endpoint.

---

## 🔐 Authentication

- User credentials stored in `users.json`
- Functions in `auth.utils.py` and `user_store.py` handle login, validation, and storage.

---

## 📊 Visualization Support

- Uses **Plotly** to render:
  - Line charts (sales over time)
  - Bar plots (top products)
  - Pie charts (distribution-based)

---

## ✅ Requirements

- Python 3.8+
- Packages listed in `requirements.txt`:
  ```
  flask
  requests
  openai
  streamlit
  streamlit-option-menu
  streamlit-lottie
  plotly
  pandas
  sqlite3
  python-dotenv
  ```

