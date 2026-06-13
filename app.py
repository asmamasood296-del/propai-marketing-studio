import streamlit as st
import sqlite3

# 1. Page Configuration (Hamesha top par)
st.set_page_config(page_title="PropAI Marketing Studio", layout="wide")

# 2. CSS Styling (Is block ko poora copy karein)
st.markdown("""
    <style>
    /* 1. Dashboard ka poora base background */
    .stApp {
        background-color: #07132D !important;
    }

    /* 2. Sidebar ka background */
    [data-testid="stSidebar"] {
        background-color: #07132D !important;
    }

    /* 3. Sabhi inputs, file uploader, aur buttons ka background - FORCE DEEPSPACE */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    input, 
    textarea, 
    div[data-testid="stFileUploader"],
    div[data-testid="stFileUploader"] > section,
    div.stButton > button {
        background-color: #07132D !important;
        border: 1px solid #4F80BC !important; /* Border halka sa blue rakha hai taake box alag dikhe */
        color: #FFFFFF !important;
    }

    /* 4. Text ka color white */
    label, p, h1, h2, h3, .stMarkdown {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Baaki ka App Logic
st.title("PropAI Marketing Studio")
st.sidebar.header("Project Configuration")

property_type = st.sidebar.selectbox("Property Type", ["Single Family", "Luxury Estate", "Apartment"])
bedrooms = st.sidebar.number_input("Bedrooms", min_value=1, value=3)
bathrooms = st.sidebar.number_input("Bathrooms", min_value=1.0, value=2.0, step=0.5)

if st.sidebar.button("Save Property Data"):
    st.sidebar.success("Data Saved!")

st.header("Asset Upload")
uploaded_file = st.file_uploader("Upload Property Photos", type=['jpg', 'png'])

st.header("Generated Copy")
if st.button("Generate Marketing Copy"):
    st.write("Generating your copy...")