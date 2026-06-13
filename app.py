import streamlit as st
import openai
from PIL import Image
import os
import base64
import sqlite3
import uuid
from dotenv import load_dotenv

load_dotenv()

# Initialize API Engine
api_key = os.getenv("OPENAI_API_KEY", "sk-proj-YOUR_KEY_HERE")
client = openai.OpenAI(api_key=api_key)

# ==========================================
# DATABASE LAYER (SQLite)
# ==========================================
DB_FILE = "propai_studio.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_tracker (
            device_token TEXT PRIMARY KEY,
            generation_count INTEGER DEFAULT 0,
            is_registered INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS premium_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_token TEXT,
            full_name TEXT,
            agency TEXT,
            email TEXT,
            phone TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_or_create_user(token):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT generation_count, is_registered FROM usage_tracker WHERE device_token = ?", (token,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO usage_tracker (device_token, generation_count, is_registered) VALUES (?, 0, 0)", (token,))
        conn.commit()
        count, registered = 0, 0
    else:
        count, registered = row[0], row[1]
    conn.close()
    return count, bool(registered)

def increment_generation(token):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE usage_tracker SET generation_count = generation_count + 1 WHERE device_token = ?", (token,))
    conn.commit()
    conn.close()

def register_lead_db(token, name, agency, email, phone):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO premium_leads (device_token, full_name, agency, email, phone) 
        VALUES (?, ?, ?, ?, ?)
    """, (token, name, agency, email, phone))
    cursor.execute("UPDATE usage_tracker SET is_registered = 1 WHERE device_token = ?", (token,))
    conn.commit()
    conn.close()

init_db()

# ==========================================
# CORE INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="PropAI Studio | Production Build",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "device_token" not in st.session_state:
    st.session_state.device_token = str(uuid.uuid4())

# Initialize generation result memory state across form submissions
if "last_generated_copy" not in st.session_state:
    st.session_state.last_generated_copy = ""

db_count, db_registered = get_or_create_user(st.session_state.device_token)
st.session_state.usage_counter = db_count
st.session_state.user_is_registered = db_registered

# ==========================================
# AGGRESSIVE THEME REPAIR INJECTOR
# ==========================================
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #ffffff !important;
    }
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, .stWidgetLabel {
        color: #0f172a !important;
    }
    .stMarkdown div p, small, .stCaption, [data-testid="stMarkdownContainer"] p {
        color: #334155 !important;
    }
    div[data-baseweb="select"] * {
        color: #0f172a !important;
    }
    .premium-output-card {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 6px solid #2563eb !important;
        padding: 24px !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
    }
    .api-diagnostic-card {
        background-color: #fff1f2 !important;
        border: 1px solid #fecdd3 !important;
        border-left: 6px solid #f43f5e !important;
        padding: 20px !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏢 PropAI Marketing Studio")
st.markdown("##### Convert visual property assets instantly into high-converting professional listing advertisements.")

remaining_trials = max(0, 3 - st.session_state.usage_counter)
if not st.session_state.user_is_registered:
    st.info(f"⏳ Free Evaluation: {remaining_trials} generations remaining.")
else:
    st.success("💎 Premium Unlimited Tier Active.")

st.divider()

# ==========================================
# SIDEBAR CONTROL CORES
# ==========================================
with st.sidebar:
    st.markdown("### 🏠 Property Profile")
    test_mode = st.toggle("Run Simulation Test Mode", value=True)
    st.divider()
    
    st.markdown("#### 🔑 OpenAI Credentials")
    env_key = os.getenv("OPENAI_API_KEY", "")
    custom_key = st.text_input("Custom API Key Overwrite", value=env_key if env_key.startswith("sk-") else "", type="password", placeholder="sk-proj-...")
    st.divider()
    
    property_type = st.selectbox("Property Category", ["Single Family Residence", "Luxury Estate", "Condominium Apartment", "Executive Townhouse"])
    tone = st.selectbox("Target Writing Voice", ["Luxury & Sophisticated", "Warm & Inviting Family", "Modern & Minimalist"])
    
    # NEW FEATURE: Channel Optimization Selector
    marketing_channel = st.selectbox("Marketing Optimization Channel", ["Zillow/MLS Standard Listing", "Instagram/Facebook Social Copy", "Premium Print Brochure Flyer"])
    
    col_beds, col_baths = st.columns(2)
    with col_beds:
        beds = st.number_input("Bedrooms", min_value=0, max_value=15, value=3, step=1)
    with col_baths:
        baths = st.number_input("Bathrooms", min_value=0.0, max_value=15.0, value=2.5, step=0.5)
        
    key_features = st.text_area("Key Selling Highlights", placeholder="e.g., Prime location, modern kitchen finishes...")
    st.divider()
    
    uploaded_files = st.file_uploader("Upload photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# ==========================================
# PROCESSING PIPELINE LAYOUT
# ==========================================
canvas_left, canvas_right = st.columns([1, 1], gap="large")

with canvas_left:
    st.markdown("### 🖼️ Asset Visual Queue")
    if uploaded_files:
        for file in uploaded_files:
            st.image(Image.open(file), use_container_width=True)
    else:
        st.info("Visual queue empty. Upload photos in the sidebar panel to begin.")

with canvas_right:
    st.markdown("### ✨ Generated Marketing Copy")
    
    if st.session_state.usage_counter >= 3 and not st.session_state.user_is_registered:
        st.warning("🔒 Premium Professional Registration Required")
        with st.form("lead_capture_form", clear_on_submit=False):
            reg_name = st.text_input("Full Professional Name*")
            reg_agency = st.text_input("Real Estate Brokerage / Agency*")
            reg_email = st.text_input("Business Email Address*")
            reg_phone = st.text_input("Mobile Phone Number*")
            submit_registration = st.form_submit_button("Verify Profile & Commit to Database")
            
            if submit_registration:
                if not reg_name or not reg_agency or not reg_email or not reg_phone:
                    st.error("❌ Please complete all fields.")
                else:
                    register_lead_db(st.session_state.device_token, reg_name, reg_agency, reg_email, reg_phone)
                    st.success("🎉 Verified successfully! Reloading...")
                    st.rerun()
    else:
        if st.button("🚀 Process Asset & Generate Premium Listing Copy", use_container_width=True, type="primary"):
            if not uploaded_files:
                st.warning("⚠️ Input asset required: Please upload at least one image in the sidebar panel.")
            else:
                if test_mode:
                    increment_generation(st.session_state.device_token)
                    with st.spinner("Compiling copy simulation..."):
                        import time
                        time.sleep(1.0)
                        
                        simulated_text = f"### 🌟 Simulated {marketing_channel}\n\n" \
                                         f"**Property Profile:** {property_type} — {beds} Beds, {baths} Baths\n\n" \
                                         f"Optimized voice metrics applied: `{tone}` rules executed successfully.\n\n" \
                                         f"This striking residential asset features immaculate attention to architectural details. " \
                                         f"Highlights include: {key_features if key_features else 'Upgraded finishes throughout.'}"
                        
                        st.session_state.last_generated_copy = simulated_text
                else:
                    active_key = custom_key if custom_key else env_key
                    if not active_key.startswith("sk-"):
                        st.markdown("<div class='api-diagnostic-card'><h4>🔑 Missing API Credentials</h4><p>Live generation is active but no valid token was found. Please input an authorized key or run in Simulation Mode.</p></div>", unsafe_allow_html=True)
                    else:
                        with st.spinner("Communicating with Multi-Modal AI Core..."):
                            try:
                                runtime_client = openai.OpenAI(api_key=active_key)
                                
                                def encode_image(f):
                                    return base64.b64encode(f.getvalue()).decode("utf-8")
                                    
                                prompt_structure = f"Write high-end real estate advertising copy tailored specifically for the following channel: {marketing_channel}. " \
                                                   f"Property Details: {property_type} with {beds} bedrooms and {baths} bathrooms. " \
                                                   f"Key Features: {key_features}. The tone should be strictly {tone}. Output the response directly using clean, readable Markdown syntax styling."
                                
                                messages_content = [{"type": "text", "text": prompt_structure}]
                                for file in uploaded_files:
                                    messages_content.append({"type": "image_url", "image_url": {"url": f"data:{file.type};base64,{encode_image(file)}"}})
                                
                                completion = runtime_client.chat.completions.create(
                                    model="gpt-4o", 
                                    messages=[{"role": "user", "content": messages_content}], 
                                    max_tokens=900
                                )
                                
                                increment_generation(st.session_state.device_token)
                                st.session_state.last_generated_copy = completion.choices[0].message.content
                                
                            except openai.RateLimitError:
                                st.markdown("<div class='api-diagnostic-card'><h4>💳 OpenAI Account Balance Notice (Error 429)</h4><p>Your API account has exhausted its active credit balance. Top up your balance or turn Simulation Mode back ON to test for free.</p></div>", unsafe_allow_html=True)
                            except openai.AuthenticationError:
                                st.markdown("<div class='api-diagnostic-card'><h4>❌ Authentication Rejected (Error 401)</h4><p>The provided key was explicitly rejected or revoked by OpenAI.</p></div>", unsafe_allow_html=True)
                            except Exception as general_err:
                                st.error(f"Engine Exception Pipeline: {general_err}")

        # RENDER PERSISTENT MARKETING COPY IF IT EXISTS IN THE SESSION STATE
        if st.session_state.last_generated_copy:
            st.markdown(f"<div class='premium-output-card'>", unsafe_allow_html=True)
            st.markdown(st.session_state.last_generated_copy)
            st.markdown(f"</div>", unsafe_allow_html=True)
            
            st.divider()
            
            # ONE-CLICK EXPORT TO MARKDOWN FILE UTILITY
            st.download_button(
                label="📥 Download Marketing Copy Assets (.md)",
                data=st.session_state.last_generated_copy,
                file_name="PROPAI_LISTING_ASSETS.md",
                mime="text/markdown",
                use_container_width=True
            )