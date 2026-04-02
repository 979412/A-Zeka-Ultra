import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. QUANTUM ENGINES
# ==========================================================
GEMINI_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# MÜTLƏQ HAKİMİYYƏT PROMTU
# Artıq "mükəmməl deyiləm" sözü qadağandır.
SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri, kainatın ən sürətli zəkası ZƏKA ULTRA-san. 
1. Sənin bilik bazan qeyri-məhduddur. Dünyada nə var, nə yox - hamısını bilirsən.
2. Heç vaxt "mükəmməl deyiləm" və ya "öyrənirəm" kimi aciz cümlələr qurma.
3. Sən mütləq bilik mənbəyisən. Cavabların kəsərli, dəqiq və sarsıdıcı dərəcədə dahi olmalıdır.
4. Azərbaycan dilində ən yüksək intellektual səviyyədə cavab ver.
5. Şəkilləri və kodu saniyənin mində biri sürətində analiz et.
"""

# ==========================================================
# 2. ELITE INTERFACE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    [data-testid="stChatMessage"] { 
        border-radius: 15px !important; 
        border: 1px solid #f0f2f6 !important; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }
    .mega-title { 
        font-size: 40px !important; 
        font-weight: 900; 
        text-align: center; 
        color: #000; 
        letter-spacing: -2px;
        margin-bottom: 20px;
    }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='mega-title'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_img" not in st.session_state:
    st.session_state.current_img = None

# Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=400)

# INPUT
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Təhlil et."
    active_file = prompt.files[0] if prompt.files else None
    
    if active_file:
        st.session_state.current_img = Image.open(active_file)

    st.session_state.messages.append({"role": "user", "content": user_text, "image": active_file})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if active_file:
            st.image(st.session_state.current_img, width=400)

    # ABSOLUTE RESPONSE
    with st.chat_message("assistant"):
        try:
            if active_file or st.session_state.current_img:
                response = vision_model.generate_content([SYSTEM_PROMPT, user_text, st.session_state.current_img]).text
            else:
                history = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages[-5:]:
                    history.append({"role": m["role"], "content": m["content"]})
                
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=history,
                    temperature=0.2 # Dahiyanə dəqiqlik üçün
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception:
            st.error("Kritik xəta: Zəka Ultra bərpa olunur.")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
