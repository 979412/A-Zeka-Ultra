import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. A-ZƏKA KİMLİYİ VƏ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #1e3c72; text-align: center; font-weight: 900; font-size: 3.5rem; }
    .stChatMessage { border-radius: 15px; border: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# Yaradıcı Abdullah Mikayılov
with st.sidebar:
    st.markdown("### ⚙️ Ayarlar")
    st.write("👨‍💻 Yaradıcı: **Abdullah Mikayılov**")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Abdullah Mikayılovun dahi beyni ilə 1 saniyədə həllər!</p>", unsafe_allow_html=True)

# --- 2. BEYİN QOŞULMASI ---
# Sənin göndərdiyin açarı bura yazdım
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Ən stabil vizual model (Screenshot-dakı xətaları aradan qaldırır)
MODEL = "llama-3.2-11b-vision-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ŞƏKİL ANALİZİ ÜÇÜN FUNKSİYA ---
def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Söhbət tarixçəsini göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ CAVAB ---
prompt = st.chat_input("Dahi sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    # İstifadəçi mesajını ekrana çıxar
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu vizualı analiz et."
    with st.chat_message("user"):
        st.markdown(user_text)

    # A-Zəka-nın təlimatı
    system_instr = "Sən Abdullah Mikayılov tərəfindən yaradılmış dahi A-Zəka-san. Riyazi sualları LaTeX ($...$) ilə həll et."
    
    content_list = [{"type": "text", "text": user_text}]

    # Şəkil yüklənibsə, onu emal et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400, caption="Analiz edilir...")
            base64_img = encode_image(img)
            content_list.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
            })

    # Groq-dan cavab al
    with st.chat_message("assistant"):
        with st.spinner("A-Zəka ildırım sürəti ilə düşünür..."):
            try:
                chat_completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": content_list}
                    ]
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Tarixçəyə yadda saxla
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
