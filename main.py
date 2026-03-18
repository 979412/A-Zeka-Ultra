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
    .sub-title { text-align: center; color: #555; font-size: 1.2rem; margin-bottom: 30px; }
    .stChatMessage { border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 12px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 2. SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=100)
    st.markdown("### ⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.write("Sistem: **Groq 10x Ultra**")
    st.divider()
    
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Dünyanın ən mürəkkəb suallarını 1 saniyədə həll edən sistem.</p>", unsafe_allow_html=True)

# --- 3. GROQ API KONFİQURASİYASI ---
# Sənin rəsmi açarın bura sabitləndi:
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Ən son və ən güclü işlək model:
MODEL_NAME = "llama-3.3-70b-versatility"

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

# --- 5. GİRİŞ VƏ CAVAB ---
prompt = st.chat_input("Sualını yaz və ya şəkil yüklə (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    
    with st.chat_message("user"):
        st.markdown(user_text)

    # A-Zəka-nın beyni üçün təlimat
    system_instruction = "Sən Abdullah Mikayılov tərəfindən yaradılmış, dünyanın ən güclü süni intellekti A-Zəka-san. Riyazi məsələləri mütləq LaTeX ($...$) formatında addım-addım həll et."
    
    with st.chat_message("assistant"):
        with st.spinner("A-Zəka 10x Ultra düşünür..."):
            try:
                # Groq üzərindən cavab alırıq
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
                
                # Tarixçəyə əlavə et
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": final_res})
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
