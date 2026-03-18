import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. A-ZƏKA KİMLİYİ VƏ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    .main-title { color: #1e3c72; text-align: center; font-weight: 900; font-size: 3.5rem; }
    .stChatMessage { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# Yaradıcı məlumatı
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Dünyanın ən mürəkkəb suallarını Abdullah Mikayılovun köməyi ilə həll edirik.</p>", unsafe_allow_html=True)

# --- 2. BEYİN VƏ MODEL QOŞULMASI ---
# Groq API açarını bura daxil et
API_KEY = "BURAYA_GROQ_KEY_YAZ" 
client = Groq(api_key=API_KEY)

# Ən yeni və işlək model (Screenshot-dakı xətanı aradan qaldırır)
MODEL = "llama-3.3-70b-versatility"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ŞƏKİL ANALİZ FUNKSİYASI ---
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ CAVAB ---
prompt = st.chat_input("Sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    # İstifadəçi mesajını göstər
    with st.chat_message("user"):
        st.markdown(prompt.text if prompt.text else "Vizual analiz tələbi.")
    
    # Sistemin hazırlanması
    full_query = f"Sən Abdullah Mikayılovun yaratdığı dahi A-Zəka-san. Riyazi sualları LaTeX ($...$) ilə həll et. Sual: {prompt.text}"
    
    messages = [{"role": "user", "content": full_query}]
    
    # Şəkil varsa əlavə et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            base64_image = encode_image(img)
            # Vizual model üçün mesaj quruluşu
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": full_query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }]

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            try:
                # Modeli çağırırıq
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.1
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "user", "content": prompt.text})
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
