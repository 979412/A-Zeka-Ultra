import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PROFESSIONAL AĞ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; }
    .main-header { text-align: center; color: #2563eb; font-weight: 800; font-size: 3rem; margin-top: -40px; }
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (AVTOMATİK MODEL TAYİNİ) ---
API_KEY = "AIzaSyBiPhToQs_WMs_qtY_seJxhCEVd2r1Y7yk"
genai.configure(api_key=API_KEY)

# Bu funksiya sənin açarın üçün ən uyğun modeli ÖZÜ TAPIR
@st.cache_resource
def get_best_model():
    try:
        # Google-dan sənə icazə verilən modelləri alırıq
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Üstünlük sırası: Flash 1.5 -> Pro 1.5 -> Pro 1.0
        preferred = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        for p in preferred:
            if p in available_models:
                return genai.GenerativeModel(p)
        
        # Əgər heç biri yoxdursa, tapılan ilk modeli ver
        return genai.GenerativeModel(available_models[0]) if available_models else None
    except:
        return None

model = get_best_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov\nStatus: Axtarış Aktiv")
    if model:
        st.success(f"Aktiv Model: {model.model_name.split('/')[-1]}")
    else:
        st.error("Model tapılmadı!")
    
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-header'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 4. ÇAT TARİXÇƏSİ ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bunu analiz et."
    imgs = []
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            imgs.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        try:
            if not model:
                st.error("Google serverləri ilə əlaqə kəsildi. API açarını yoxla.")
            else:
                input_data = [user_text] + imgs if imgs else [user_text]
                response = model.generate_content(input_data, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_area.markdown(full_res + "▌")
                
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
        except Exception as e:
            st.error(f"⚠️ Texniki nasazlıq: {str(e)}")
