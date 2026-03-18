import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. PREMİUM DİZAYNIN BƏRPASI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; font-family: 'Segoe UI', sans-serif; }
    .ultra-title {
        color: #2c3e50;
        text-align: center;
        font-weight: 800;
        font-size: 3.2rem;
        margin-bottom: 0px;
    }
    .sub-title { text-align: center; color: #7f8c8d; margin-bottom: 30px; font-weight: 500; }
    .stChatMessage { border-radius: 15px; background-color: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .stButton>button { background-color: #e74c3c; color: white; border-radius: 8px; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 2. SOL PANEL (Dizayn Geri Qayıtdı) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.markdown("### ⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.divider()
    
    # SƏNİN GEMİNİ AÇARIN ÜÇÜN YER
    api_key = st.text_input("🔑 Gemini API Key:", type="password", help="aistudio.google.com-dan al")
    
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Abdullah Mikayılovun dahi beyni ilə 1 saniyədə həllər!</p>", unsafe_allow_html=True)

# --- 3. BEYİN QURAŞDIRILMASI ---
if not api_key:
    st.warning("⚠️ Zəhmət olmasa sol tərəfə Gemini API açarını daxil et.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. "+" DÜYMƏSİ VƏ GİRİŞ (Geri Qayıtdı) ---
prompt = st.chat_input("Dahi sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_msg = prompt.text if prompt.text else "Bu şəkli analiz et."
    with st.chat_message("user"):
        st.markdown(user_msg)
    
    content = [user_msg]
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=300)
            content.append(img)

    with st.chat_message("assistant"):
        with st.spinner("Dahi beyin düşünür..."):
            try:
                response = model.generate_content(content)
                res_text = response.text
                st.markdown(res_text)
                
                # Tarixçəyə yaz
                st.session_state.messages.append({"role": "user", "content": user_msg})
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
