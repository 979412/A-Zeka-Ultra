import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. A-ZƏKA KİMLİYİ VƏ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    .main-title { color: #1e3c72; text-align: center; font-weight: 900; font-size: 3rem; margin-bottom: 20px; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# Yaradıcı məlumatı sidebar-da
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6134/6134346.png", width=80)
    st.title("⚙️ A-Zəka Paneli")
    st.write("👨‍💻 Yaradıcı: **Abdullah Mikayılov**")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)

# --- 2. GROQ KEY VƏ MODEL (DÜZƏLDİLDİ) ---
# Sənin göndərdiyin rəsmi açarı bura qoydum:
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Screenshot-da çıxan 400 xətasını aradan qaldırmaq üçün AKTİV model:
MODEL = "llama-3.2-11b-vision-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ŞƏKİL ANALİZİ FUNKSİYASI ---
def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ CAVAB MEXANİZMİ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    # İstifadəçi tərəfi
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu vizualı analiz et."
    with st.chat_message("user"):
        st.markdown(user_text)
    
    # A-Zəka-nın təlimatı (Alim rejimi)
    system_instr = "Sən Abdullah Mikayılov tərəfindən yaradılmış dahi A-Zəka-san. Riyazi sualları LaTeX ($...$) ilə həll et."
    
    content_list = [{"type": "text", "text": user_text}]

    # Şəkil varsa analizə əlavə et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400, caption="Analiz edilir...")
            base_4_img = encode_image(img)
            content_list.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base_4_img}"}
            })

    # Groq API-yə müraciət
    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            try:
                chat_completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": content_list}
                    ],
                    temperature=0.1
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Tarixçəyə əlavə et
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
