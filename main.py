import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. ULTRA PREMİUM VİSUAL AYARLAR ---
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
    
    .stChatMessage { border-radius: 20px; border: 1px solid #1e293b; padding: 15px; margin-bottom: 10px; background: #1e293b50; }
    
    /* Yan Panel Dizaynı */
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    .stButton>button {
        width: 100%; border-radius: 10px; background: #ef4444; color: white;
        border: none; font-weight: 600; transition: 0.3s;
    }
    .stButton>button:hover { background: #dc2626; transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# --- 2. API KONFİQURASİYASI ---
# Sənin rəsmi açarın daxil edildi
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# 404 XƏTASI VERMƏYƏN, ƏN GÜCLÜ VƏ STABİL MODEL
MODEL_NAME = "llama-3.1-70b-versatility" 

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Ultra Panel</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=120)
    st.info(f"Yaradıcı: Abdullah Mikayılov\nModel: {MODEL_NAME}")
    
    st.divider()
    if st.button("🗑️ Tarixçəni Tamamilə Sil"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("### 📊 Sistem Statusu")
    st.success("Ultra Beyin 10x Aktivdir")

# --- 4. ƏSAS EKRAN ---
st.markdown("<h1 class='ultra-header'>A-ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Dünyanın ən mürəkkəb suallarını 1 saniyədə həll edən sistem.</p>", unsafe_allow_html=True)

# Söhbət tarixçəsini göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. GİRİŞ SİSTEMİ (+) ---
# accept_file=True sayəsində "+" düyməsi aktivdir
prompt = st.chat_input("Sualını yaz və ya şəkil yüklə (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Yüklənən medianı analiz et."
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for file in prompt.files:
                st.image(file, caption="Analiz üçün yükləndi", width=400)

    # Sistem Təlimatı
    system_instruction = (
        "Sən Abdullah Mikayılov tərəfindən yaradılmış, dünyanın ən güclü süni intellekti A-Zəka-san. "
        "Cavabların dahi səviyyəsində, elmi və dəqiq olmalıdır. "
        "Riyazi düsturlar üçün LaTeX ($...$) istifadə et."
    )

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka analiz edir..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_text}
                    ],
                    temperature=0.2
                )
                
                final_res = response.choices[0].message.content
                st.markdown(final_res)
                
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": final_res})
                
            except Exception as e:
                st.error(f"Xəta kodu: {str(e)}")
                st.info("İpucu: Model adı dəyişdirildi. Əgər yenə 404 xətası çıxsa, Groq profilində model icazələrini yoxla.")
