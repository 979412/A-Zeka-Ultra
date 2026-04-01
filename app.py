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

# 🧠 SMART MODEL PICKER: 404 xətasını qabaqlamaq üçün
@st.cache_resource
def get_best_vision_model():
    try:
        # Sənin açarın üçün aktiv olan modelləri tapırıq
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Əgər flash varsa onu götür, yoxdursa siyahıdan birini seç
        for m_name in models:
            if 'gemini-1.5-flash' in m_name:
                return genai.GenerativeModel(m_name)
        return genai.GenerativeModel(models[0]) if models else None
    except:
        return None

vision_model = get_best_vision_model()

SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın dahi memar Abdullah Mikayılovdur. 
Azərbaycan dilində, professional və birbaşa cavab ver. 
Əgər söhbət davam edirsə, 'Salam' demə.
"""

# ==========================================================
# 2. PURE WHITE UI (White Edition)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v9.0", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
    .main-title { font-size: 40px !important; font-weight: 800; text-align: center; border-bottom: 1px solid #f0f2f6; padding: 15px; }
    [data-testid="stChatMessage"] { background-color: #ffffff !important; border: 1px solid #f0f2f6 !important; border-radius: 12px; }
    [data-testid="stChatMessageUser"] { background-color: #f9f9f9 !important; }
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

prompt = st.chat_input("Memar, buyurun...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Prosesdədir..."):
            try:
                if active_file and vision_model:
                    img = Image.open(active_file)
                    st.image(img, width=300)
                    response = vision_model.generate_content([f"{SYSTEM_PROMPT}\nSual: {user_text}", img]).text
                else:
                    # MƏTN (Groq - Həmişə işləyir)
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
                
            except Exception:
                st.warning("⚠️ Media mühərriki hazırda məşğuldur, mətni analiz edirəm...")
                # Əgər Gemini çöksə, avtomatik Llama (Groq) cavab versin
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_text}]
                )
                response = completion.choices[0].message.content
                st.markdown(response)

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
