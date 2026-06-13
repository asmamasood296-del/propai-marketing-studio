import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv

# 1. Page Config
st.set_page_config(page_title="PropAI Marketing Studio", layout="wide")
# 2. CSS
st.markdown("""
    <style>
    /* 1. Main Background - Deep Space (#07132D) */
    .stApp, header, [data-testid="stHeader"] {
        background-color: #07132D !important;
    }
    
    /* 2. Sidebar Background - Regel Navy (#002366) */
    [data-testid="stSidebar"] {
        background-color: #002366 !important;
    }

    /* 3. Credentials (Inputs/Select) - Glaucous (#4F80BC) */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    input, 
    textarea, 
    div[data-testid="stFileUploader"],
    div[data-testid="stFileUploader"] > section {
        background-color: #4F80BC !important;
        color: #000000 !
# 2. Database Setup (SQL logic)
def init_db():
    conn = sqlite3.connect('propai_studio.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads 
                 (id INTEGER PRIMARY KEY, property_type TEXT, bedrooms INTEGER, bathrooms REAL)''')
    conn.commit()
    conn.close()

init_db()

# 3. Main UI Layout
st.title("🏢 PropAI Marketing Studio")

# Sidebar
with st.sidebar:
    st.header("Project Configuration")
    prop_type = st.selectbox("Property Type", ["Single Family", "Luxury Estate", "Condo"])
    beds = st.number_input("Bedrooms", min_value=1, value=3)
    baths = st.number_input("Bathrooms", min_value=1.0, value=2.0)
    
    if st.button("Save Property Data"):
        conn = sqlite3.connect('propai_studio.db')
        c = conn.cursor()
        c.execute("INSERT INTO leads (property_type, bedrooms, bathrooms) VALUES (?, ?, ?)", (prop_type, beds, baths))
        conn.commit()
        conn.close()
        st.success("Data saved to database!")

# Main Content Area
col1, col2 = st.columns(2)
with col1:
    st.subheader("Asset Upload")
    st.file_uploader("Upload Property Photos", type=['jpg', 'png'])

with col2:
    st.subheader("Generated Copy")
    if st.button("Generate Marketing Copy"):
        # Yahan aapka AI logic integrate hoga
        st.info("Generating professional copy for " + prop_type + "...")
        st.write("---")
        st.write("Luxurious " + str(beds) + " bedroom home featuring " + str(baths) + " baths. Perfect for modern living.")