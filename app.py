import streamlit as st
import pandas as pd
import openai
import sqlite3  # SQLite import zaroori hai

# 1. Database Setup
def init_db():
    conn = sqlite3.connect('propai.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS properties 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  prop_type TEXT, beds INTEGER, baths REAL, 
                  description TEXT)''')
    conn.commit()
    conn.close()

init_db()

def save_to_db(prop_type, beds, baths, description):
    conn = sqlite3.connect('propai.db')
    c = conn.cursor()
    c.execute("INSERT INTO properties (prop_type, beds, baths, description) VALUES (?, ?, ?, ?)",
              (prop_type, beds, baths, description))
    conn.commit()
    conn.close()

# 2. Page Configuration
st.set_page_config(page_title="PropAI Marketing Studio", layout="wide")

# 3. CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #07132D !important; }
    [data-testid="stSidebar"] { background-color: #07132D !important; }
    div[data-testid="stButton"] > button { background-color: #4F80BC !important; color: white !important; }
    label, p, h1, h2, h3 { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# 4. OpenAI Client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_marketing_copy(prop_type, beds, baths):
    prompt = f"Write a professional, attractive real estate marketing description for a {prop_type} with {beds} bedrooms and {baths} bathrooms."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ... (Baaki code upar waise hi rahega) ...

# 5. UI Layout
st.title("PropAI Marketing Studio")
# ... (Sidebar inputs waise hi) ...

st.header("Generated Copy")
if st.button("Generate Marketing Copy"):
    with st.spinner("AI is crafting your description..."):
        try:
            result = generate_marketing_copy(prop_type, beds, baths)
            save_to_db(prop_type, beds, baths, result)
            st.success("Result generated and saved to database!")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

# --- HISTORY SECTION (Ise if-block se bahar aur alag rakhein) ---
def get_history():
    conn = sqlite3.connect('propai.db')
    c = conn.cursor()
    c.execute("SELECT * FROM properties ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

st.header("History of Generated Copies")
history = get_history()

if history:
    import pandas as pd
    df = pd.DataFrame(history, columns=["ID", "Type", "Beds", "Baths", "Description"])
    st.table(df)
else:
    st.write("No history found yet.")