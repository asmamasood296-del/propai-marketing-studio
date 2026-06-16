import streamlit as st
import openai
import sqlite3
import pandas as pd
import base64

# --- 1. Database & Setup ---
def init_db():
    conn = sqlite3.connect('propai.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS properties 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, prop_type TEXT, beds INTEGER, baths REAL, description TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(prop_type, beds, baths, description):
    conn = sqlite3.connect('propai.db')
    c = conn.cursor()
    c.execute("INSERT INTO properties (prop_type, beds, baths, description) VALUES (?, ?, ?, ?)",
              (prop_type, beds, baths, description))
    conn.commit()
    conn.close()

init_db()

# --- 2. AI Engine (Vision Integration) ---
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

def generate_marketing_copy(prop_type, beds, baths, image_file=None):
    base64_image = encode_image(image_file) if image_file else None
    prompt_text = f"Write a professional real estate description for a {prop_type} with {beds} beds and {baths} baths."
    
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]
    if base64_image:
        messages[0]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
    
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content

# --- 3. UI ---
st.set_page_config(page_title="PropAI Marketing Studio", layout="wide")
st.title("PropAI Marketing Studio")

prop_type = st.sidebar.selectbox("Property Type", ["Single Family", "Luxury Estate", "Apartment"])
beds = st.sidebar.number_input("Bedrooms", min_value=1, value=3)
baths = st.sidebar.number_input("Bathrooms", min_value=1.0, value=2.0, step=0.5)
uploaded_file = st.file_uploader("Upload Property Photos", type=['jpg', 'png', 'jpeg'])

if st.button("Generate Marketing Copy"):
    with st.spinner("AI is analyzing and crafting..."):
        try:
            result = generate_marketing_copy(prop_type, beds, baths, uploaded_file)
            save_to_db(prop_type, beds, baths, result)
            st.success("Result generated!")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

# --- 4. History ---
st.header("History")
data = pd.read_sql_query("SELECT * FROM properties ORDER BY id DESC", sqlite3.connect('propai.db'))
st.table(data)