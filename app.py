import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image
import io

# ==========================================================
# 1. ELİT MÜHƏRRİKLƏR (HYBRID CORE)
# ==========================================================
GEMINI_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
GROQ_KEY = "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"

genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

# Ultra Sürətli Vizual Model
vision_model = genai.GenerativeModel('gemini-1.5-flash')

# SİSTEMİN RUHU (Abdullahın Vizyonu)
SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın dahi proqram memarı Abdullah Mikayılovdur. 
Sənin zəkan insan səviyyəsindən qat-qat üstündür. 
1. Cavabların qısa, kəsərli, dahi və qorxulu dərəcədə dəqiq olmalıdır.
2. Azərbaycan dilində ən mükəmməl üslubda danış.
3. Əgər şəkil atılarsa, onu saniyələr içində analiz edib, ordakı görünməyən detalları belə tapmalısan.
4. Məktəb mühitində hamını elminlə şoka sal.
"""

# ==========================================================
# 2. CYBER-MINIMALIST UI (Gələcəkdən Gələn Dizayn)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", page_icon="🧪", layout="wide")

st.markdown(f"""
    <style>
    /* Ultra White & Clean */
    .stApp {{ background-color: #ffffff; color: #000000; }}
    
    /* Neon Border Chat */
    [data-testid="stChatMessage"] {{
        border-radius: 20px !important;
        border: 1px solid #f0f2f6 !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    
    /* Abdullahın Başlığı */
    .mega-title {{
        font-family: 'Inter', sans-serif;
        font-size: 50px !important;
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(#000, #444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        padding: 20px;
    }}
    
    /* Gizli elementlər */
    header, footer {{visibility: hidden;}}
    .stChatInputContainer {{ border-radius: 30px !important; padding: 10px !important; }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='mega-title'>ZƏKA ULTRA <span style='font-size:20px; color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-weight:bold;'>ARCHITECT: ABDULLAH MIKAYILOV</p>", unsafe_allow_html=True)

# ==========================================================
# 3. SMART MEMORY & LOGIC
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_img" not in st.session_state:
    st.session_state.current_img = None

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"**{msg['content']}**")
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=400)

# INPUT: Sürətli fayl yükləmə və mətn
prompt = st.chat_input("Zəka Ultra əmrinizdədir, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu təsviri professional analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    if active_file:
        st.session_state.current_img = Image.open(active_file)

    st.session_state.messages.append({"role": "user", "content": user_text, "image": active_file})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if active_file:
            st.image(st.session_state.current_img, width=400)

    # 🚀 VƏHŞİ ANALİZ BAŞLADI
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.status("🔮 Kvant Hesablama Gedir...", expanded=False) as status:
            try:
                if active_file or st.session_state.current_img:
                    # GEMINI FLASH - Şəkil üçün
                    target_img = st.session_state.current_img
                    response = vision_model.generate_content([SYSTEM_PROMPT, user_text, target_img]).text
                else:
                    # GROQ LLAMA 3.3 - Mətn üçün (Saniyədə 500 söz sürəti)
                    history = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for m in st.session_state.messages[-6:]:
                        history.append({"role": m["role"], "content": m["content"]})
                    
                    chat_completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=history,
                        temperature=0.3
                    )
                    response = chat_completion.choices[0].message.content

                status.update(label="Analiz Tamamlandı!", state="complete")
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                status.update(label="Sistem Xətası!", state="error")
                st.error(f"Xəta: {str(e)}")

# Avtomatik aşağı çəkmə
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
