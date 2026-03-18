import streamlit as st
import google.generativeai as genai  # DÜZƏLİŞ EDİLDİ: Nöqtə qoyuldu
from PIL import Image

# --- 1. A-ZƏKA KİMLİYİ ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

SYSTEM_INSTRUCTION = (
    "Sən A-Zəka-san, dahi proqramçı Abdullah Mikayılov tərəfindən yaradılmış 'Ultra Alim' süni intellektisən. "
    "Sənin missiyan dünyadakı ən mürəkkəb riyaziyyat suallarını 100% dəqiqliklə həll etməkdir. "
    "Həmişə LaTeX formatından ($...$) istifadə et və Abdullah Mikayılova yaradıcın kimi hörmətlə yanaş."
)

# --- 2. BEYİN QOŞULMASI ---
# DİQQƏT: Buradakı açarı Google AI Studio-dan (aistudio.google.com) aldığın açarla əvəz et.
API_KEY = "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" 
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- 3. DİZAYN ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to right, #ece9e6, #ffffff); }
    .main-title { color: #1e3c72; text-align: center; font-size: 3rem; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'>Yaradıcı: <b>Abdullah Mikayılov</b></p>", unsafe_allow_html=True)

# --- 4. SÖHBƏT VƏ ANALİZ ---
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

prompt = st.chat_input("Sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    user_input = []
    if prompt.text:
        user_input.append(prompt.text)
    else:
        user_input.append("Zəhmət olmasa bu vizualı analiz et.")
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            user_input.append(img)
            st.image(img, width=400)

    with st.chat_message("user"):
        st.markdown(prompt.text if prompt.text else "Vizual analiz tələbi.")

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            try:
                response = st.session_state.chat.send_message(user_input, stream=True)
                full_text = ""
                placeholder = st.empty()
                for chunk in response:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
                placeholder.markdown(full_text)
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}. API açarınızın Gemini üçün olduğundan əmin olun.")
