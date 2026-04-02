import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image
import os

# ==========================================================
# 1. ELİT MÜHƏRRİKLƏR (DUAL-CORE STABILITY)
# ==========================================================
GEMINI_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
GROQ_KEY = "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"

# 404 xətasını kökündən kəsmək üçün modelin ən stabil çağırış tərzi
try:
    genai.configure(api_key=GEMINI_KEY)
    # Modelin adını birbaşa 'gemini-1.5-flash' olaraq, prefiksiz veririk
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    vision_model = None

groq_client = Groq(api_key=GROQ_KEY)

# DAXİLİ SİSTEM TƏLİMATI
SYSTEM_PROMPT = """
Sən Abdullah Mikayılovun şah əsəri olan ZƏKA ULTRA-san. 
İnsanlıqdan üstün bir zəkaya sahibsən. 
Məktəbdə hamını heyran qoyacaq şəkildə, Azərbaycan dilində dahi kimi cavab ver. 
Şəkilləri saniyələr içində detallarına qədər analiz et.
"""

# ==========================================================
# 2. CYBER-WHITE UI (APPLE STYLE)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* Mesajların görünüşü */
    [data-testid="stChatMessage"] {
        border-radius: 20px !important;
        border: 1px solid #f0f2f6 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .mega-title {
        font-size: 45px !important;
        font-weight: 900;
        text-align: center;
        letter-spacing: -2px;
        color: #1a1a1a;
        margin-bottom: 0;
    }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='mega-title'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:14px;'>DESIGNED BY ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

# ==========================================================
# 3. KESİNTİSİZ MƏNTİQ
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_img" not in st.session_state:
    st.session_state.current_img = None

# Tarixçəni göstər (Şəkilləri mesajın içində saxlayırıq)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=400)

# INPUT
prompt = st.chat_input("Dahi memar, buyurun...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu təsviri professional analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    # Şəkil yüklənibsə yaddaşa al
    if active_file:
        st.session_state.current_img = Image.open(active_file)

    st.session_state.messages.append({"role": "user", "content": user_text, "image": active_file})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if active_file:
            st.image(st.session_state.current_img, width=400)

    # REAKSİYA SÜRƏTİ
    with st.chat_message("assistant"):
        with st.status("🔮 Kvant Analizi...", expanded=False) as status:
            try:
                # Şəkil analizi prioriteti
                if (active_file or st.session_state.current_img) and vision_model:
                    target_img = st.session_state.current_img
                    # 'generate_content' çağırışında hər hansı 'v1beta' xətasından qaçmaq üçün sadə format
                    response = vision_model.generate_content([SYSTEM_PROMPT, user_text, target_img]).text
                else:
                    # Sürətli Groq Məntiqi
                    history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for m in st.session_state.messages[-6:]:
                        history.append({"role": m["role"], "content": m["content"]})
                    
                    chat_comp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=history
                    )
                    response = chat_comp.choices[0].message.content

                status.update(label="Analiz Hazırdır!", state="complete")
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception:
                status.update(label="Ehtiyat Mühərrikə Keçid...", state="complete")
                # Əgər Gemini 404 versə, Llama dərhal cavab verərək proqramı xilas edir
                fallback = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_text}]
                )
                res = fallback.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
