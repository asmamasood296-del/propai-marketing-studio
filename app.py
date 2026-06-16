import streamlit as st
import openai

# 1. Page Configuration
st.set_page_config(page_title="PropAI Marketing Studio", layout="wide")

# 2. CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #07132D !important; }
    [data-testid="stSidebar"] { background-color: #07132D !important; }
    div[data-testid="stButton"] > button { background-color: #4F80BC !important; color: white !important; }
    label, p, h1, h2, h3 { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# 3. OpenAI Client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 4. Logic Function
def generate_marketing_copy(prop_type, beds, baths):
    prompt = f"Write a professional, attractive real estate marketing description for a {prop_type} with {beds} bedrooms and {baths} bathrooms."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 5. UI Layout
st.title("PropAI Marketing Studio")
st.sidebar.header("Project Configuration")

prop_type = st.sidebar.selectbox("Property Type", ["Single Family", "Luxury Estate", "Apartment"])
beds = st.sidebar.number_input("Bedrooms", min_value=1, value=3)
baths = st.sidebar.number_input("Bathrooms", min_value=1.0, value=2.0, step=0.5)

if st.sidebar.button("Save Property Data"):
    st.sidebar.success("Data Saved!")

st.header("Asset Upload")
uploaded_file = st.file_uploader("Upload Property Photos", type=['jpg', 'png'])

st.header("Generated Copy")
if st.button("Generate Marketing Copy"):
    with st.spinner("AI is crafting your description..."):
        try:
            result = generate_marketing_copy(prop_type, beds, baths)
            st.success("Here is your property description:")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")