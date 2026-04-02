import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES
# ==========================================================
GEMINI_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# STRICT SYSTEM PROMPT: Nağıl danışmağı qadağan edirik
SYSTEM_PROMPT = "Sən ZƏKA ULTRA-san. Qayda: Heç vaxt salam vermə, özünü tanıtma, nağıl danışma. Sualın cavabı nədirsə, yalnız onu yaz. Azərbaycan dilində çox qısa və kəsərli ol."

# ==========================================================
# 2. ULTRA-MINIMAL UI
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    [data-testid="stChatMessage"] { border-radius: 15px !important; border: 1px solid #f0f2f6 !important; }
    .mega-title { font-size: 35px !important; font-weight: 900; text-align: center; color: #1a1a1a; }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='mega-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_img" not in st.session_state:
    st.session_state.current_img = None

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=350)

# INPUT
prompt = st.chat_input("Sualınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    if active_file:
        st.session_state.current_img = Image.open(active_file)

    st.session_state.messages.append({"role": "user", "content": user_text, "image": active_file})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if active_file:
            st.image(st.session_state.current_img, width=350)

    # CAVAB (Düyməsiz, birbaşa)
    with st.chat_message("assistant"):
        try:
            if active_file or st.session_state.current_img:
                # Şəkil analizi
                response = vision_model.generate_content([SYSTEM_PROMPT, user_text, st.session_state.current_img]).text
            else:
                # Mətn analizi (Groq - İnanılmaz sürətli)
                history = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages[-5:]:
                    history.append({"role": m["role"], "content": m["content"]})
                
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=history,
                    temperature=0.1 # Daha dəqiq cavab üçün
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error("Xəta baş verdi.")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
