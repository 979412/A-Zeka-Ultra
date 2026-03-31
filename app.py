import streamlit as st
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io

# ==========================================================
# 1. CORE ENGINES & KEYS
# ==========================================================
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"

groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

# 2026 Professional Sistem Təlimatı
SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. 2026-cı ilin ən qabaqcıl süni intellektisən. 
Yaradıcın dahi memar Abdullah Mikayılovdur. 
Xüsusiyyətlərin: Vəhşi sürət, dəqiq analiz, mükəmməl Azərbaycan dili.
Həmişə Abdullahın vizyonuna uyğun, soyuqqanlı və kəsərli cavablar ver.
"""

# ==========================================================
# 2. FUTURISTIC UI (CSS 2026)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v8.0", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Ana Fon */
    .stApp { background-color: #050505; color: #e0e0e0; }
    
    /* Başlıq */
    .main-title {
        font-size: 50px !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #ff0000, #ff7300);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    /* Chat Mesajları */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        border: 1px solid #1a1a1a !important;
    }
    
    /* User Mesajı */
    [data-testid="stChatMessageUser"] {
        background-color: #111111 !important;
        border-left: 5px solid #ff0000 !important;
    }
    
    /* Assistant Mesajı */
    [data-testid="stChatMessageAssistant"] {
        background-color: #0a0a0a !important;
        border-right: 5px solid #ff7300 !important;
    }

    /* Gizli elementləri təmizlə */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>MEMAR: ABDULLAH MİKAYILOV | VERSION 8.0 OMNI</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #1a1a1a;'>", unsafe_allow_html=True)

# ==========================================================
# 3. CHAT ENGINE (MEMORY)
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş hissəsi (accept_file=True avtomatik '+' ikonası yaradır)
prompt = st.chat_input("Memar, əmriniz nədir?", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Vizual analiz tələb olunur."
    active_file = prompt.files[0] if prompt.files else None
    
    # Ekrana və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Cavab mexanizmi
    with st.chat_message("assistant"):
        with st.spinner("⚡ SİSTEM AKTİVLƏŞİR..."):
            try:
                if active_file:
                    # GEMINI VISION CORE
                    img = Image.open(active_file)
                    st.image(img, caption="Analiz edilən media", width=300)
                    gen_prompt = f"{SYSTEM_PROMPT}\n\nİstifadəçi: {user_text}"
                    response = vision_model.generate_content([gen_prompt, img]).text
                else:
                    # GROQ SPEED CORE
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_text}
                        ],
                        temperature=0.6 # Daha kəsərli cavablar üçün
                    )
                    response = completion.choices[0].message.content
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Sistem sönməsi: {str(e)}")

# Avtomatik scroll (Səhifəni aşağı çək)
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
