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

# 🧠 SMART MODEL PICKER (404-ü həll etmək üçün)
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

try:
    groq_client = Groq(api_key=GROQ_API_KEY)
    genai.configure(api_key=GEMINI_API_KEY)
    vision_model = get_best_vision_model()
except:
    pass

SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın dahi memar Abdullah Mikayılovdur. 
Azərbaycan dilində, professional və birbaxa cavab ver. 
Əgər söhbət davam edirsə, 'Salam' demə. 
Həmişə Abdullahın vizyonuna uyğun, soyuqqanlı və kəsərli cavablar ver.
"""

# ==========================================================
# 2. WHITE UI DESIGN
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v9.2", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
    .main-title { font-size: 40px !important; font-weight: 800; text-align: center; border-bottom: 1px solid #f0f2f6; padding: 15px; }
    [data-testid="stChatMessage"] { background-color: #ffffff !important; border: 1px solid #f0f2f6 !important; border-radius: 12px; }
    [data-testid="stChatMessageUser"] { background-color: #f9f9f9 !important; }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

# ==========================================================
# 3. ZƏKA ULTRA MEMORY CORE (DAİMİ YADDAŞ)
# ==========================================================
# Bu funksiya şəkli Süni İntellektin daimi yaddaşına salır
@st.cache_resource
def get_immortal_memory():
    return {"current_image": None}

immortal_mem = get_immortal_memory()

# Əgər yaddaşda şəkil varsa, onu ekranda sabit saxla
if immortal_mem["current_image"]:
    st.image(immortal_mem["current_image"], caption="Analiz üçün aktiv media", width=300)
    # Şəkli silmək üçün düymə
    if st.button("Şəkli Yaddaşdan Sil"):
        immortal_mem["current_image"] = None
        st.rerun()

# Söhbət yaddaşı (Hələlik st.session_state-də qalır, çünki Groq daha stabil yaddaşa malikdir)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni ekranda göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş hissəsi
prompt = st.chat_input("Memar, buyurun...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    # Yeni şəkil yüklənibsə, daimi yaddaşa sal
    if active_file:
        img = Image.open(active_file)
        immortal_mem["current_image"] = img
    
    # Ekrana və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Cavab mexanizmi
    with st.chat_message("assistant"):
        with st.spinner("⚡ Prosesdədir..."):
            try:
