import streamlit as st
import sqlite3

# 1. Page Configuration (Hamesha top par)
st.set_page_config(page_title="PropAI Marketing Studio", layout="wide")

# 2. CSS Styling (Is block ko poora copy karein)
st.markdown("""
    <style>
    /* Main Background - Deep Space (#07132D) */
    .stApp, header, [data-testid="stHeader"] {
        background-color: #07132D !important;
    }
    
    /* Sidebar Background - Regel Navy (#002366) */
    [data-testid="stSidebar"] {
        background-color: #002366 !important;
    }

    /* Inputs/Credentials - Glaucous (#4F80BC) */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    input, 
    textarea, 
    div[data-testid="stFileUploader"],
    div[data-testid="stFileUploader"] > section {
        background-color: #4F80BC !important;
        color: #000000 !important;
    }

    /* Buttons - Glaucous (#4F80BC) */
    div.stButton > button, 
    button[kind="secondary"] {
        background-color: #4F80BC !important;
        color: #000000 !important;
        border: none !important;
    }

    /* Number Input fix for plus/minus area */
    div[data-testid="stNumberInput"] > div > div {
        background-color: #4F80BC !important;
    }

    /* White Text for all elements */
    label, p, h1, h2, h3, .stMarkdown, .stFileUploader, .stNumberInput {
        color: #FFFFFF !important;
    }
    
    /* Input field text force black */
    input, textarea, div[data-baseweb="select"] > div {
        color: #000000 !important;
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