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

# Mühərrikləri işə salırıq
groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. 
Həmişə Azərbaycan dilində cavab ver. 
Əgər artıq salamlaşmısınızsa, hər mesajda yenidən 'salam' demə. 
Söhbətin əvvəlini yadda saxla və ona uyğun davam et.
"""

# ==========================================================
# 2. LIGHT UI DESIGN
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v8.6", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .main-title {
        font-size: 40px !important;
        font-weight: 800;
        text-align: center;
        color: #1a1a1a;
        padding: 20px;
        border-bottom: 2px solid #f0f2f6;
    }
    .stChatMessage {
        border-radius: 15px !important;
        border: 1px solid #f0f2f6 !important;
    }
    [data-testid="stChatMessageUser"] { background-color: #f8f9fa !important; }
    [data-testid="stChatMessageAssistant"] { background-color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

# ==========================================================
# 3. CHAT LOGIC
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni göstər
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
        with st.spinner("🚀 Analiz edilir..."):
            try:
                if active_file:
                    img = Image.open(active_file)
                    st.image(img, width=300)
                    # Şəkil analizi üçün təmiz prompt
                    response = vision_model.generate_content([SYSTEM_PROMPT + "\n" + user_text, img]).text
                else:
                    # Tarixçəni mühərrikə ötürürük (CONTEXT)
                    history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for msg in st.session_state.messages[-6:]: # Son 6 mesajı yadda saxla
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
                st.error(f"Sistem xətası: {str(e)}")

# Scroll düzəlişi
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
