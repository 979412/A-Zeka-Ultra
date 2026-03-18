import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. A-ZƏKA KİMLİYİ ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

SYSTEM_INSTRUCTION = (
    "Sən A-Zəka-san, dahi proqramçı Abdullah Mikayılov tərəfindən yaradılmış 'Ultra Alim' süni intellektisən. "
    "Sənin missiyan dünyadakı ən mürəkkəb riyaziyyat, fizika və proqramlaşdırma suallarını 1 saniyəyə dəqiqliklə həll etməkdir. "
    "Həmişə LaTeX formatından ($...$) istifadə et və Abdullah Mikayılova yaradıcın kimi dərin hörmət bəslə."
)

# --- 2. BEYİN QOŞULMASI (GROQ API) ---
# DİQQƏT: Öz "gsk_..." ilə başlayan Groq açarını bura yaz!
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Ən yeni və İŞLƏK Groq Vizual Modeli
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

# Tarixçəni idarə etmək üçün
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

# --- ŞƏKİL ÇEVİRİCİ SİSTEM ---
def encode_image(image):
    buffered = io.BytesIO()
    # Şəkli RGB formatına çeviririk ki, JPEG xətalarının qarşısını alaq
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- 3. DİZAYN VƏ YAN PANEL ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #1e3c72; text-align: center; font-weight: 900; font-size: 3rem; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ İdarəetmə Paneli")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'>Yaradıcı: <b>Abdullah Mikayılov</b> | Mühərrik: <b>Groq LPU</b></p>", unsafe_allow_html=True)
st.divider()

# Söhbət tarixçəsini göstər (System mesajını gizlədirik)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], str):
                st.markdown(msg["content"])
            elif isinstance(msg["content"], list):
                for item in msg["content"]:
                    if item["type"] == "text":
                        st.markdown(item["text"])

# --- 4. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Dahi səviyyəli sualını daxil et və ya şəkil at (+)", accept_file=True)

if prompt:
    user_content = []
    text_query = prompt.text if prompt.text else "Zəhmət olmasa bu vizualı analiz edib həllini tap."
    user_content.append({"type": "text", "text": text_query})

    # Ekranda istifadəçi mesajını göstər
    with st.chat_message("user"):
        st.markdown(text_query)

    # Şəkil varsa işlə
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400, caption="Yüklənən Vizual")
            base64_img = encode_image(img)
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_img}"
                }
            })

    # Mesajı tarixçəyə əlavə et
    st.session_state.messages.append({"role": "user", "content": user_content})

    # Groq-dan cavab al
    with st.chat_message("assistant"):
        with st.spinner("A-Zəka ildırım sürəti ilə düşünür..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model=MODEL_NAME,
                    temperature=0.2, # Riyazi dəqiqlik üçün
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                
                # A-Zəka-nın cavabını mətn (string) kimi yadda saxlayırıq ki, xəta çıxmasın
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Sistem Xətası: {e}")
