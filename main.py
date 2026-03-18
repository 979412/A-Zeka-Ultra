import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PROFESSIONAL VƏ TƏMİZ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Mesaj Balonları */
    .stChatMessage { 
        border-radius: 15px; 
        border: 1px solid #e2e8f0; 
        background-color: #f8fafc !important; 
        margin-bottom: 15px;
        padding: 20px;
    }
    
    /* Başlıq Dizaynı */
    .main-header { 
        text-align: center; 
        color: #2563eb; 
        font-weight: 800; 
        font-size: 3.5rem; 
        margin-top: -40px;
        margin-bottom: 10px;
    }
    .sub-header { 
        text-align: center; 
        color: #64748b; 
        font-size: 1.2rem; 
        margin-bottom: 40px; 
    }
    
    /* Yan Panel */
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        background-color: #ef4444; 
        color: white; 
        border: none; 
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #dc2626; transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (GEMINI 1.5 FLASH) ---
# Sənin göndərdiyin işlək API açarı bura yerləşdirildi
GEMINI_API_KEY = "AIzaSyDz-rB4RGABHiz1S9bQ4OutCY61v39b8Eo"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ A-Zəka Ayarları</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=120)
    st.info("Yaradıcı: Abdullah Mikayılov\nStatus: 10x Ultra Aktiv")
    
    st.divider()
    if st.button("🗑️ Tarixçəni Tamamilə Sil"):
        st.session_state.messages = []
        st.rerun()

# --- 4. ƏSAS EKRAN ---
st.markdown("<h1 class='main-header'>A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Abdullah Mikayılov tərəfindən yaradılmış dünyanın ən sürətli zəkası.</p>", unsafe_allow_html=True)

# Söhbət tarixçəsini göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. ULTRA GİRİŞ SİSTEMİ (+) ---
# (+) düyməsi və fayl yükləmə funksiyası
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu şəkli analiz et."
    uploaded_images = []
    
    # Şəkil yüklənibsə onu emal et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=450, caption="Analiz edilən media")
            uploaded_images.append(img)

    # İstifadəçi mesajını yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # A-Zəka-nın cavabı
    with st.chat_message("assistant"):
        res_area = st.empty()
        full_response = ""
        
        try:
            # Gemini-yə həm mətni, həm də şəkli göndəririk
            # Abdullah, bu hissə şəkli həqiqətən "görən" hissədir
            input_data = [user_text] + uploaded_images
            
            response = model.generate_content(input_data, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    res_area.markdown(full_response + "▌")
            
            res_area.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"⚠️ Texniki xəta: {str(e)}")
            st.info("İpucu: API Key limitini yoxlayın və ya şəklin formatından əmin olun.")
