import streamlit as st
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io

# ==========================================================
# 1. CORE ENGINES (Dəqiq Model Təyini)
# ==========================================================
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"

# Groq mühərriki
groq_client = Groq(api_key=GROQ_API_KEY)

# Gemini tənzimləməsi - 404 xətasını həll edən format
genai.configure(api_key=GEMINI_API_KEY)

# BURADA DƏYİŞİKLİK: 'models/' prefiksini çıxarıb yoxlayırıq
try:
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')

SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın dahi memar Abdullah Mikayılovdur. 
Mütləq Azərbaycan dilində cavab ver. 
QAYDA: Salamlaşmısınızsa, yenidən 'Salam' demə. Birbaşa işə keç.
"""

# ==========================================================
# 2. PURE WHITE UI (White Mode)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v8.9", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
    .main-title {
        font-size: 40px !important;
        font-weight: 800;
        text-align: center;
        color: #1a1a1a;
        padding: 15px;
        border-bottom: 1px solid #f0f2f6;
    }
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #f0f2f6 !important;
        border-radius: 10px !important;
    }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

# ==========================================================
# 3. CHAT LOGIC
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Memar, əmr edin...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz tələb olunur."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Proses gedir..."):
            try:
                if active_file:
                    # ŞƏKİL ANALİZİ
                    img = Image.open(active_file)
                    st.image(img, width=300)
                    # generate_content üçün birbaşa çağırış
                    response_obj = vision_model.generate_content([f"{SYSTEM_PROMPT}\nSual: {user_text}", img])
                    response = response_obj.text
                else:
                    # MƏTN ANALİZİ (Groq)
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
                st.error(f"Kritik Xəta: {str(e)}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
