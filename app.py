# --- Page Config ---
import streamlit as st
st.set_page_config(page_title="E-commerce AI Agent", layout="wide")

# --- Imports ---
import requests
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
# Assuming user_store.py and users.json are correctly set up for authentication
from user_store import add_user, validate_user
import os

# --- Inject CSS ---
def local_css(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠ CSS file not found: {file_path}")

local_css("style.css")

# --- Load Lottie Animation ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_lottie():
    lottie = load_lottieurl("https://lottie.host/1a9342fa-35e1-4720-b66c-2ef8c6805ae0/2X4XZnDGBg.json")
    if lottie:
        st_lottie(lottie, height=200)

# --- Backend API ---
BACKEND_URL = "http://127.0.0.1:5000/ask"

# --- Signup ---
def signup():
    st.subheader("🔐 Create Account")
    username = st.text_input("Choose a Username", key="signup_username")
    password = st.text_input("Choose a Password", type="password", key="signup_password")
    if st.button("Sign Up", key="signup_button"):
        if add_user(username, password):
            st.success("✅ Account created! Please log in.")
        else:
            st.error("❌ Username already exists.")

# --- Login ---
def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if validate_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("❌ Invalid credentials.")

# --- Theme ---
def apply_theme(theme_choice):
    if theme_choice == "Dark":
        dark_style = """
        <style>
        body, .stApp { background-color: #1e1e1e; color: white; }
        .stTextInput > div > div > input, .stDataFrame { background-color: #2b2b2b; color: white; border: 1px solid #444; }
        .stSelectbox > div > div, .stButton > button { background-color: #3a3a3a; color: white; border: 1px solid #555; }
        h1, h2, h3, h4, h5, h6 { color: #f0f0f0; }
        .stMarkdown { color: #d0d0d0; }
        .stSidebar { background-color: #2a2a2a; }
        .css-1cpxqw2.e1tzin5v2 { background-color: #007bff; color: white; }
        </style>
        """
        st.markdown(dark_style, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        body, .stApp { background-color: white; color: black; }
        .stTextInput > div > div > input, .stDataFrame { background-color: white; color: black; border: 1px solid #ccc; }
        .stSelectbox > div > div, .stButton > button { background-color: #f0f0f0; color: black; border: 1px solid #ccc; }
        .stSidebar { background-color: #f8f8f8; }
        </style>
        """, unsafe_allow_html=True)

# --- Main App Logic ---
def main_app():
    st.title("🛒 E-commerce Data Agent")
    show_lottie()

    st.markdown("### 📌 Suggested Questions")
    for q in [
        "🔹 Show total sales trend over time",
        "🔹 Compare ad sales vs ad spend by date",
        "🔹 Plot top 5 items by impressions",
        "🔹 What are the trends of clicks over time?",
        "🔹 Which items have the highest click-through rate (CTR)?",
        "🔹 How does conversion rate vary by weekday?",
        "🔹 Show return rate by product category",
        "🔹 Compare cost per click (CPC) across campaigns",
        "🔹 What are the top 5 products by revenue last month?",
        "🔹 How has customer acquisition changed over time?",
        "🔹 Which regions have the best performing ads?"
    ]:
        st.markdown(q)

    st.sidebar.title("🌃 Theme & Filters")
    theme = st.sidebar.radio("🌃 Select Theme", ["Light", "Dark"])
    apply_theme(theme)

    item_id_filter = st.sidebar.text_input("🔍 Filter by Item ID (e.g., 29)")
    eligibility_filter = st.sidebar.text_input("🔍 Eligibility Message Contains (e.g., cost)")
    chart_type = st.sidebar.selectbox("📊 Chart Type", ["Line", "Bar", "Area"])

    query = st.text_input("### 💬 Enter your question")

    if st.button("Ask"):
        if not query:
            st.warning("Please enter a question.")
            return

        with st.spinner("Thinking..."):
            try:
                res = requests.post(BACKEND_URL, json={"question": query})
                res.raise_for_status()
                data = res.json()

                sql = data.get("sql_query", "")
                results = data.get("results", [])

                if sql:
                    st.markdown("### 🧮 Generated SQL")
                    st.code(sql, language="sql")

                if results:
                    df = pd.DataFrame(results)

                    if "item_id" in df.columns:
                        df["item_id"] = df["item_id"].astype(str).replace('nan', '')
                    if "message" in df.columns:
                        df["message"] = df["message"].astype(str).replace('nan', '')

                    filtered_df = df.copy()
                    try:
                        if item_id_filter and "item_id" in filtered_df.columns:
                            st.write("🛠 Applying Item ID filter...")
                            filtered_df = filtered_df[filtered_df["item_id"].str.contains(item_id_filter.lower(), case=False, na=False)]
                    except Exception as e:
                        st.error(f"❌ Error applying Item ID filter: {e}")

                    try:
                        if eligibility_filter and "message" in filtered_df.columns:
                            st.write("🛠 Applying Eligibility Message filter...")
                            filtered_df = filtered_df[filtered_df["message"].str.contains(eligibility_filter.lower(), case=False, na=False)]
                    except Exception as e:
                        st.error(f"❌ Error applying Message filter: {e}")

                    st.markdown("### 📋 Results Table")
                    if not filtered_df.empty:
                        st.dataframe(filtered_df, use_container_width=True)
                    else:
                        st.info("No results found after applying filters.")

                    df_for_charting = filtered_df.copy()

                    # --- FIXED CODE ---
                    time_cols = [
                        col for col in df_for_charting.columns
                        if isinstance(col, str) and ('date' in col.lower() or 'time' in col.lower())
                    ]
                    # ------------------

                    numeric_cols = df_for_charting.select_dtypes(include='number').columns.tolist()

                    if time_cols and numeric_cols and not df_for_charting.empty:
                        st.markdown("### 📈 Auto Chart")
                        default_x = time_cols[0] if time_cols else None
                        default_y = numeric_cols[0] if numeric_cols else None

                        x_axis_index = time_cols.index(default_x) if default_x in time_cols else 0
                        y_axis_index = numeric_cols.index(default_y) if default_y in numeric_cols else 0

                        x_axis = st.selectbox("🗂 Select X-axis", time_cols, index=x_axis_index)
                        y_axis = st.selectbox("📐 Select Y-axis", numeric_cols, index=y_axis_index)

                        df_for_charting[x_axis] = pd.to_datetime(df_for_charting[x_axis], errors='coerce')
                        df_chart_final = df_for_charting.dropna(subset=[x_axis])

                        if not df_chart_final.empty:
                            df_chart_final = df_chart_final.sort_values(by=x_axis)

                            if chart_type == "Line":
                                fig = px.line(df_chart_final, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                            elif chart_type == "Bar":
                                fig = px.bar(df_chart_final, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                            elif chart_type == "Area":
                                fig = px.area(df_chart_final, x=x_axis, y=y_axis, title=f"{y_axis} Area Chart over {x_axis}")

                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("ℹ No valid data points for charting after date conversion or filtering.")
                    else:
                        st.info("ℹ Not enough valid time and numeric columns or data to plot a chart.")
                else:
                    st.warning("No results found for your query.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Could not connect to the backend API. Please ensure it's running.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API Request Error: {e}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
                import traceback
                st.exception(e)
                traceback.print_exc()

# --- Routing ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

with st.sidebar:
    page = option_menu("Navigation", ["Login", "Sign Up"],
                       icons=['box-arrow-in-right', 'person-plus'], default_index=0, key="auth_navigation")

if st.session_state["authenticated"]:
    main_app()
else:
    if page == "Login":
        login()
    elif page == "Sign Up":
        signup()