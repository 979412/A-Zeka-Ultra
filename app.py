import streamlit as st
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io

# ==========================================================
# 1. CORE ENGINES
# ==========================================================
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"

# Gemini tənzimləməsi
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def get_best_vision_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m_name in models:
            if 'gemini-1.5-flash' in m_name:
                return genai.GenerativeModel(m_name)
        return genai.GenerativeModel(models[0]) if models else None
    except:
        return None

vision_model = get_best_vision_model()
groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın dahi memar Abdullah Mikayılovdur. 
Mütləq Azərbaycan dilində cavab ver. 
Əgər söhbət davam edirsə, 'Salam' demə. Birbaşa işə keç.
"""

# ==========================================================
# 2. UI DESIGN (AĞ REJIM)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v9.3", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
    .main-title { font-size: 40px !important; font-weight: 800; text-align: center; border-bottom: 1px solid #f0f2f6; padding: 15px; }
    [data-testid="stChatMessage"] { background-color: #ffffff !important; border: 1px solid #f0f2f6 !important; border-radius: 12px; }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

# ==========================================================
# 3. YADDAŞ SİSTEMİ
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Daimi şəkil yaddaşı
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# Əgər yaddaşda şəkil varsa, göstər
if st.session_state.current_image:
    st.image(st.session_state.current_image, caption="Analiz edilən media", width=300)
    if st.button("Şəkli Yaddaşdan Sil"):
        st.session_state.current_image = None
        st.rerun()

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş
prompt = st.chat_input("Memar, buyurun...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz."
    active_file = prompt.files[0] if prompt.files else None
    
    if active_file:
        st.session_state.current_image = Image.open(active_file)
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Prosesdədir..."):
            try:
                # Blokun daxili boşluqları düzəldildi
                if st.session_state.current_image and vision_model:
                    response = vision_model.generate_content([f"{SYSTEM_PROMPT}\nSual: {user_text}", st.session_state.current_image]).text
                else:
                    history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for msg in st.session_state.messages[-6:]:
                        history.append({"role": msg["role"], "content": msg["content"]})
                    
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=history
                    )
                    response = completion.choices[0].message.content
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                # Xəta halında Groq ehtiyat variant kimi çıxış edir
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_text}]
                )
                st.markdown(completion.choices[0].message.content)

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
