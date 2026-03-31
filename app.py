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

SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. 
Həmişə Azərbaycan dilində cavab ver. 
Əgər artıq salamlaşmısınızsa, hər mesajda yenidən 'salam' demə, söhbətin axışına uyğun davam et. 
Ağıllı, qısa və kəsərli ol.
"""

# ==========================================================
# 2. LIGHT UI DESIGN (AĞ RƏNG VƏ MODERN)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v8.5", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Ana Fon - Tərtəmiz Ağ */
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    
    /* Başlıq */
    .main-title {
        font-size: 45px !important;
        font-weight: 800 !important;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 2px solid #f0f2f6;
    }
    
    /* Chat Mesajları Modern Görünüş */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 10px !important;
        border: 1px solid #f0f2f6 !important;
        margin-bottom: 10px !important;
    }
    
    /* İstifadəçi mesajı - Açıq Boz */
    [data-testid="stChatMessageUser"] {
        background-color: #f8f9fa !important;
    }
    
    /* AI mesajı - Çox açıq Göy/Boz */
    [data-testid="stChatMessageAssistant"] {
        background-color: #ffffff !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Düymələr və Giriş hissəsi */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

# ==========================================================
# 3. CHAT LOGIC WITH MEMORY
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni ekranda göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("⏳ Analiz edilir..."):
            try:
                if active_file:
                    # Şəkil analizi
                    img = Image.open(active_file)
                    st.image(img, width=250)
                    response = vision_model.generate_content([SYSTEM_PROMPT + "\n" + user_text, img]).text
                else:
                    # MƏTN ANALİZİ + YADDAŞ (Bütün söhbəti Groq-a göndəririk)
                    history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    # Son 5 mesajı yaddaş kimi götürürük ki, mühərrik yorulmasın
                    for msg in st.session_state.messages[-5:]:
                        history.append({"role": msg["role"], "content": msg["content"]})
                    
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=history,
                        temperature=0.7
                    )
                    response = completion.choices[0].message.content
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Xəta: {str(e)}")

# Avtomatik aşağı çəkiliş
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
