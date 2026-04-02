import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image

# ==========================================================
# 1. CORE ENGINES (QUANTUM STABILITY)
# ==========================================================
GEMINI_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)
# 404 xətasını kökündən həll etmək üçün ən stabil model çağırışı
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri, kainatın ən sürətli zəkası ZƏKA ULTRA-san. 
Sənin bilik bazan qeyri-məhduddur. Cavabların kəsərli, dəqiq və professional olmalıdır.
Heç vaxt aciz cümlələr qurma. Azərbaycan dilində ən yüksək səviyyədə cavab ver.
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
        margin-bottom: 5px;
    }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='mega-title'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:14px; margin-bottom:20px;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_img" not in st.session_state:
    st.session_state.current_img = None

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg and msg["image"] is not None:
            st.image(msg["image"], width=400)

# ==========================================================
# 3. SMART INPUT & LOGIC
# ==========================================================
# Streamlit-in ən son chat_input formatı
prompt = st.chat_input("Əmr edin, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    # Faylın oxunması üçün daha etibarlı metod
    active_file = prompt.files[0] if (hasattr(prompt, 'files') and prompt.files) else None
    
    img_to_save = None
    if active_file:
        img_to_save = Image.open(active_file)
        st.session_state.current_img = img_to_save

    # İstifadəçi mesajını yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text, "image": img_to_save})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if img_to_save:
            st.image(img_to_save, width=400)

    # CAVAB MEXANİZMİ
    with st.chat_message("assistant"):
        try:
            # Əgər şəkil varsa GEMINI işləsin
            if st.session_state.current_img:
                response_obj = vision_model.generate_content([SYSTEM_PROMPT, user_text, st.session_state.current_img])
                response = response_obj.text
            else:
                # Sırf mətn üçün GROQ (Llama 3.3)
                history = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages[-5:]:
                    history.append({"role": m["role"], "content": m["content"]})
                
                chat_comp = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=history,
                    temperature=0.2
                )
                response = chat_comp.choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response, "image": None})

        except Exception as e:
            st.error("Zəka Ultra bərpa olunur. Xəta: " + str(e))

# Səhifəni avtomatik aşağı çək
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
