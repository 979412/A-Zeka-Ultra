import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. PREMİUM VİSUAL AYARLAR ---
st.set_page_config(page_title="A-Zəka Ultra 10x", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    .ultra-header {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; font-size: 4rem; font-weight: 700;
        margin-bottom: 5px;
    }
    
    .stChatMessage { border-radius: 20px; border: 1px solid #1e293b; padding: 15px; margin-bottom: 10px; }
    .stChatInputContainer { border-top: 1px solid #1e293b !important; }
    
    /* Yan Panel Dizaynı */
    .css-1d391kg { background-color: #1e293b !important; }
    .stButton>button {
        width: 100%; border-radius: 10px; background: #ef4444; color: white;
        border: none; font-weight: 600; transition: 0.3s;
    }
    .stButton>button:hover { background: #dc2626; transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN VƏ API KONFİQURASİYASI ---
# Sənin Groq API açarın birbaşa bura daxil edildi
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Ən stabil və ultra güclü model (400 xətası verməyən versiya)
# Gemini 1.5 Flash-dan 10 qat güclü cavablar üçün Llama 3.3 70B istifadə edirik
MODEL_NAME = "llama-3.3-70b-versatility"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL (ADMİN PANALİ) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Ultra Panel</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=120)
    st.info("Yaradıcı: Abdullah Mikayılov\nStatus: Ultra 10x Aktiv")
    
    st.divider()
    if st.button("🗑️ Tarixçəni Tamamilə Sil"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("### 📊 Sistem Yükü")
    st.progress(98, text="Ultra Beyin Aktivdir")

# --- 4. ƏSAS EKRAN ---
st.markdown("<h1 class='ultra-header'>A-ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Dünyanın ən mürəkkəb suallarını 1 saniyədə həll edən 10x sistem.</p>", unsafe_allow_html=True)

# Söhbət tarixçəsini göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. ULTRA GİRİŞ SİSTEMİ (+) ---
# Burada accept_file=True mütləq olmalıdır ki, "+" düyməsi çıxsın
prompt = st.chat_input("Sualını yaz və ya şəkil yüklə (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu faylı/şəkli analiz et."
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for file in prompt.files:
                st.image(file, caption="Yüklənən media", width=400)

    # A-Zəka-nın təlimatı (Alim Beyni)
    system_instruction = (
        "Sən Abdullah Mikayılov tərəfindən yaradılmış, Gemini 1.5-dən 10 qat güclü A-Zəka-san. "
        "Dünyanın ən mürəkkəb suallarına birbaşa, dəqiq və elmi cavablar ver. "
        "Riyazi düsturları LaTeX ($...$) ilə göstər."
    )

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka 10x analiz edir..."):
            try:
                # Groq üzərindən müraciət
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_text}
                    ],
                    temperature=0.1 # Daha dəqiq cavablar üçün
                )
                
                final_res = response.choices[0].message.content
                st.markdown(final_res)
                
                # Yaddaşa əlavə et
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": final_res})
                
            except Exception as e:
                # Şəkillərdə görünən 400 və 404 xətalarını bura tuturuq
                st.error(f"Texniki xəta: {str(e)}")
                st.warning("Model adı və ya API key xətası. Lütfən modeli 'llama-3.3-70b-versatility' olaraq yoxlayın.")
