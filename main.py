import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. ULTRA DİZAYN VƏ AYARLAR ---
st.set_page_config(page_title="A-Zəka 10x Ultra", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    /* Arxa fon və ümumi şriftlər */
    .stApp { background-color: #f4f7fb; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Əsas başlıq */
    .ultra-title {
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 3.8rem;
        margin-bottom: 5px;
        padding-top: 20px;
    }
    .sub-title { text-align: center; color: #555; font-size: 1.1rem; margin-bottom: 30px; font-weight: bold; }
    
    /* Mesaj qutuları (Çat kürəcikləri) */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #eaeaea;
    }
    
    /* Sol panel (Sidebar) düymələri */
    .stButton>button {
        background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff1c1c; box-shadow: 0 4px 10px rgba(255,75,75,0.4); }
</style>
""", unsafe_allow_html=True)

# --- 2. İDARƏETMƏ PANELİ VƏ BEYİN ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=100)
    st.markdown("### ⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.write("Güc: **Ultra 10x (Groq Beyni)**")
    st.divider()
    
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Dünyanın ən mürəkkəb suallarını 1 saniyədə həll edən 10x sistem.</div>", unsafe_allow_html=True)

# --- GROQ API KEY ELAVE EDİLDİ ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Ən stabil vizual analiz modeli
MODEL_NAME = "llama-3.2-11b-vision-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. FUNKSİYALAR ---
def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Söhbət tarixçəsini göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# + Düyməli mesaj yeri
prompt = st.chat_input("Mürəkkəb sualını yaz və ya şəkil yüklə (+)...", accept_file=True)

if prompt:
    user_message = prompt.text if prompt.text else "Zəhmət olmasa bu şəkli detallı analiz et."
    
    with st.chat_message("user"):
        st.markdown(user_message)

    # A-Zəka Sistem Təlimatı
    system_instruction = "Sən Abdullah Mikayılov tərəfindən yaradılmış, dünyanın en güclü süni intellekti A-Zəka-san. Riyazi sualları mütləq LaTeX ($...$) formatında addım-addım həll et."
    
    content_list = [{"type": "text", "text": user_message}]
    
    # Şəkil yüklənibsə emal et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=350, caption="📷 Şəkil analizə hazırlandı...")
            base64_image = encode_image(img)
            content_list.append({
                "type": "image_url",
                "image_url
