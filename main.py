import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PROFESSIONAL VƏ İŞIQLI DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #1e293b; }
    
    /* Başlıq Dizaynı */
    .main-header {
        text-align: center;
        color: #2563eb;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-text { text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 30px; }
    
    /* Çat Mesajları */
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; }
    
    /* Yan Panel */
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
    
    /* Düymələr */
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: #ef4444; color: white;
        border: none; padding: 10px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. AYARLAR VƏ BEYİN ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Ayarlar</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.info("Yaradıcı: Abdullah Mikayılov")
    
    # Bura öz Gemini API Key-ni daxil et
    api_key = st.text_input("🔑 Gemini API Key:", type="password")
    
    st.divider()
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.messages = []
        st.rerun()

# Beyini işə sal
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ Davam etmək üçün sol panelə Gemini API Key daxil edin.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ƏSAS EKRAN ---
st.markdown("<h1 class='main-header'>A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Dahi Abdullah Mikayılov tərəfindən idarə olunan 10x zəka.</p>", unsafe_allow_html=True)

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ "+" DÜYMƏSİ ---
# accept_file=True mütləqdir ki, "+" düyməsi görünsün
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for f in prompt.files:
                img = Image.open(f)
                st.image(img, width=400)

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            try:
                # Mətn və şəkli eyni anda göndəririk
                content_to_send = [user_text]
                if prompt.files:
                    for f in prompt.files:
                        content_to_send.append(Image.open(f))
                
                response = model.generate_content(content_to_send)
                res_text = response.text
                st.markdown(res_text)
                
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
