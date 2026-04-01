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

groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

# 📜 DAHA SƏRT SİSTEM TƏLİMATI
SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. 
Mütləq Azərbaycan dilində cavab ver. 
QAYDA: Əgər söhbət artıq başlayıbsa (yaddaşda mesajlar varsa), hər dəfə 'Salam' demək QADAĞANDIR. 
Birbaşa suala cavab ver və ya söhbəti davam etdir. Səmimi amma konkret ol.
"""

# ==========================================================
# 2. PURE WHITE UI DESIGN
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v8.7", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Bütün qara rəngləri ağla əvəz edirik */
    .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
    
    .main-title {
        font-size: 40px !important;
        font-weight: 800;
        text-align: center;
        color: #1a1a1a;
        padding: 20px;
        border-bottom: 2px solid #f0f2f6;
    }

    /* Chat sahəsi təmizliyi */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #eeeeee !important;
        border-radius: 12px !important;
    }

    /* İstifadəçi mesajı bir az fərqlənsin */
    [data-testid="stChatMessageUser"] {
        background-color: #f9f9f9 !important;
    }

    /* Input sahəsi */
    .stChatInputContainer {
        background-color: #ffffff !important;
    }
    
    /* Toolbar və Header-i gizlət */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

# ==========================================================
# 3. CHAT LOGIC (SMART MEMORY)
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekranda göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Memar, buyurun...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Şəkli analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Düşünürəm..."):
            try:
                # Söhbət tarixçəsini hazırlayırıq
                history = [{"role": "system", "content": SYSTEM_PROMPT}]
                
                # Əgər tarixçədə artıq mesaj varsa, AI bunu görəcək və təkrar salam verməyəcək
                for msg in st.session_state.messages[-8:]: 
                    history.append({"role": msg["role"], "content": msg["content"]})

                if active_file:
                    # ŞƏKİL ANALİZİ (Gemini)
                    img = Image.open(active_file)
                    st.image(img, width=280)
                    # Şəkil üçün də yaddaşı ötürürük
                    response = vision_model.generate_content([SYSTEM_PROMPT + f"\nContext: {user_text}", img]).text
                else:
                    # MƏTN ANALİZİ (Groq)
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=history,
                        temperature=0.6
                    )
                    response = completion.choices[0].message.content
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Xəta: {str(e)}")

# Avtomatik scroll
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
