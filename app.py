import streamlit as st
import openai
import sqlite3
import pandas as pd
import base64

# --- 1. Database Setup ---
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

# --- 2. AI Engine ---
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

# --- 3. UI Layout & Compliance ---
st.set_page_config(page_title="PropAI Marketing Studio", layout="wide")
st.markdown("""<style>.stApp { background-color: #07132D !important; } .stSidebar { background-color: #07132D !important; }</style>""", unsafe_allow_html=True)

st.title("PropAI Marketing Studio")

# Contact Info in Sidebar
st.sidebar.subheader("Contact Information")
st.sidebar.write("📍 Office: Rawalpindi, Punjab, Pakistan")
st.sidebar.write("📞 Contact: 0302-5604239")
st.sidebar.write("✉️ Email: asmamasood296@gmail.com")

tab1, tab2, tab3 = st.tabs(["Marketing Studio", "Terms & Conditions", "Refund Policy"])

with tab1:
    prop_type = st.selectbox("Property Type", ["Single Family", "Luxury Estate", "Apartment"])
    beds = st.number_input("Bedrooms", min_value=1, value=3)
    baths = st.number_input("Bathrooms", min_value=1.0, value=2.0, step=0.5)
    uploaded_file = st.file_uploader("Upload Property Photos", type=['jpg', 'png', 'jpeg'])

    if st.button("Generate Marketing Copy"):
        with st.spinner("AI is crafting your description..."):
            try:
                result = generate_marketing_copy(prop_type, beds, baths, uploaded_file)
                save_to_db(prop_type, beds, baths, result)
                st.success("Result generated and saved!")
                st.write(result)
            except Exception as e:
                if "insufficient_quota" in str(e):
                    st.warning("⚠️ **Credit Limit Reached!**")
                    st.error("Please upgrade to premium to keep generating.")
                    st.link_button("Upgrade to Premium", "https://your-payment-link-here")
                else:
                    st.error(f"Something went wrong: {e}")
    
    st.header("History")
    data = pd.read_sql_query("SELECT * FROM properties ORDER BY id DESC", sqlite3.connect('propai.db'))
    st.table(data)

    st.subheader("Our Services")
    st.write("1. Real Estate Basic | 2. Luxury Estate Pro | 3. Apartment Special | 4. Commercial Space | 5. Bulk Property Upload | 6. AI Image Enhancement | 7. Multi-Language Support | 8. Enterprise Solutions")

with tab2:
    st.header("Terms & Conditions")
    st.write("By using PropAI, you agree to these terms. AI-generated content is for professional use only. We are not liable for description inaccuracies.")

with tab3:
    st.header("Refund & Privacy Policy")
    st.write("Privacy: We do not store your personal images. Refund: Processed within 7 days if the service is unavailable.")