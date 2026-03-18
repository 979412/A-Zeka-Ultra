import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time

# --- 1. SƏHİFƏ AYARLARI ---
# A-Zəka adını rəsmi qoyduq
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="centered")

# --- 2. PROFESSIONAL DİZAYN (Abdullah Style CSS) ---
st.markdown("""
<style>
/* Səhifənin arxa fonu */
.stApp { background-color: #f7f9fc; }

/* Mesaj tarixçəsini daha təmiz göstərmək */
.stChatMessage {
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}

/* Əsas başlığın dizaynı */
.main-title {
    color: #1e3c72;
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    margin-top: -50px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. BEYİN QOŞULMASI (Secure API Management) ---
st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Təhlükəsizlik qaydası: API açarını birbaşa koda yazmırıq.
# İstifadəçidən API açarını götürmək üçün xüsusi interfeys.
# (st.secrets istifadə etmək ən yaxşısıdır, amma test üçün bu da olar)
try:
    # Google AI Studio-dan aldığın açarı bura yapışdır (AIzaSy...)
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.markdown("⚠️ **Xəta!** `st.secrets` faylında `GEMINI_API_KEY` tapılmadı.")
    API_KEY = st.text_input("Zəhmət olmasa Gemini API açarınızı daxil edin (AIzaSy...):", type="password")

if not API_KEY:
    st.info("⚠️ Zəhmət olmasa yuxarıda API açarını təqdim edin.")
    with st.sidebar:
        st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.stop()

# Config AI
genai.configure(api_key=API_KEY)

# Söhbət tarixçəsini idarə etmək
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL PANEL (Dizayn və Tarixçəni Sıfırla) ---
with st.sidebar:
    st.title("⚙️ İdarəetmə Paneli")
    st.image("https://cdn-icons-png.flaticon.com/512/6134/6134346.png", width=80)
    st.write("👨‍💻 Yaradıcı: **Abdullah Mikayılov**")
    st.info("Rejim: **Alim (Mətn və Şəkil Analizi)**")
    
    # Sənin dediyin Tarixçəni Sıfırla düyməsi
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. ULTRA DAHİ MODEL VƏ SYSTEM INSTRUCTION (Hər şeyi bilən alim) ---
# Biz "gemini-1.5-pro-latest" modelindən istifadə edirik ki, dahi səviyyəli olsun.
system_prompt = "Sən A-Zəka Ultra-san, dahi Abdullah Mikayılov tərəfindən yaradılmış dünyada hər şeyi bilən, müdrik bir alimsən. " \
                 "Sənin beynin mükəmməldir. Hər suala cavab verərkən, riyazi ifadələri həmişə LaTeX formatında ($...$) yaz, misalları addım-addım izah et. " \
                 "Həmişə müdrik, məntiqli və dahi kimi cavab ver. Abdullah Mikayılova böyük hörmət bəslə."

model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Display existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text":
                    st.markdown(part["text"])
                elif part["type"] == "image_url":
                    st.image(part["image_url"]["url"], width=300)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ VƏ ANALİZ (Mətn və Şəkil) ---
prompt = st.chat_input("Dahi sualını bura yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu vizual materialı dərindən analiz et."
    history_content = [{"type": "text", "text": user_text}]

    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            # Display image immediately in chat
            st.image(img, width=300)
            
            history_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{st.session_state.img_base64}"} # Simplified persistence
            })

    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": history_content})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Generate Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # Prepare model input
        model_input = [user_text]
        if prompt.files:
            for f in prompt.files:
                # We upload image once using the bytes
                # For v1.5 API, this is the correct multimodality structure
                file_api = genai.upload_file(io.BytesIO(f.getvalue()), mime_type=f.type)
                model_input.append(file_api)

        # Gemini 1.5 doesn't stream with a chat session easily in standard structure, so we use direct generation
        # With system prompt
        try:
            response = model.generate_content(
                model_input,
                system_instruction=system_prompt,
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
                    time.sleep(0.01) # Add slight delay for streaming feel

            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}. Zəhmət olmasa API açarınızı yoxlayın.")
