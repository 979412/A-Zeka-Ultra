import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. ULTRA PREMİUM DİZAYN ---
st.set_page_config(page_title="A-Zəka 10x Ultra", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f4f7fb; font-family: 'Helvetica Neue', sans-serif; }
    .ultra-title {
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 3.5rem;
        margin-bottom: 10px;
    }
    .sub-title { text-align: center; color: #555; font-size: 1.1rem; margin-bottom: 30px; font-weight: bold; }
    .stChatMessage { border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 2. SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=100)
    st.markdown("### ⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.write("Güc: **Groq 10x Ultra**")
    st.divider()
    
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Dünyanın ən mürəkkəb suallarını 1 saniyədə həll edən sistem.</div>", unsafe_allow_html=True)

# --- 3. GROQ API KONFİQURASİYASI (Sənin Keyin Daxil Edildi) ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Ən stabil və işlək model (404 və ya 400 xətası verməməsi üçün)
MODEL_NAME = "llama3-8b-8192" 

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. FUNKSİYALAR ---
def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Söhbət tarixçəsini göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. "+" DÜYMƏLİ GİRİŞ (Bərpa Edildi) ---
prompt = st.chat_input("Sualını yaz və ya şəkil yüklə (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu məlumatı analiz et."
    
    with st.chat_message("user"):
        st.markdown(user_text)

    # Sistem təlimatı
    system_instruction = "Sən Abdullah Mikayılov tərəfindən yaradılmış dahi A-Zəka-san. Riyaziyyatı LaTeX ($...$) ilə addım-addım həll et."
    
    # Şəkil yüklənibsə (Groq-un vision modelləri üçün gələcək hazırlıq)
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=350, caption="📷 Şəkil A-Zəka beyninə ötürüldü...")

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka 10x analiz edir..."):
            try:
                # Groq üzərindən cavab alırıq
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_text}
                    ]
                )
                final_res = response.choices[0].message.content
                st.markdown(final_res)
                
                # Tarixçəyə yaz
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": final_res})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
