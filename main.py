import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Gemini", page_icon="♊", layout="wide")

# --- 2. GÖZƏL DİZAYN ---
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    .main-title { color: #1a73e8; text-align: center; font-weight: 900; font-size: 3rem; }
    .stChatMessage { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# --- 3. GEMİNİ BEYİN MƏRKƏZİ ---
# Bura öz Google AI Studio API key-ini yazmalısan
GEMINI_API_KEY = "BURAYA_OZ_API_KEY_INI_YAZ" 
genai.configure(api_key=GEMINI_API_KEY)

# Modeli başladırıq (Flash 1.5 - Sürətli və Ağıllı)
model = genai.GenerativeModel('gemini-1.5-flash')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 4. SOL PANEL ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304fb62aa2586aed.svg", width=100)
    st.title("A-Zəka Control")
    st.info("Beyin: **Gemini 1.5 Flash** Active")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    st.write("Yaradıcı: **Abdullah Mikayılov**")

# --- 5. ƏSAS EKRAN ---
st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Gemini</h1>", unsafe_allow_html=True)

# Tarixçəni göstər
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    # İstifadəçi mesajını göstər
    with st.chat_message("user"):
        st.markdown(prompt.text if prompt.text else "Şəkil göndərildi.")
        input_data = [prompt.text] if prompt.text else []
        
        if prompt.files:
            for f in prompt.files:
                img = Image.open(f)
                st.image(img, width=300)
                input_data.append(img)

    # Gemini-dən cavab al
    with st.chat_message("assistant"):
        with st.spinner("Gemini düşünür..."):
            try:
                # System instructions (Səni tanıması üçün)
                full_prompt = [
                    "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılmış dahi AI-san. "
                    "Riyaziyyatı və elmi mükəmməl bilirsən. Cavablarını LaTeX formatında yaz."
                ] + input_data
                
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                
                # Tarixçəyə əlavə et
                st.session_state.chat_history.append({"role": "user", "content": prompt.text if prompt.text else "Şəkil"})
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Xəta: {e}")
