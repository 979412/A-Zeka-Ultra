import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. PROFESSIONAL VƏ TƏMİZ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Mesaj Balonları */
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; margin-bottom: 10px; }
    
    /* Başlıq */
    .main-header { text-align: center; color: #2563eb; font-weight: 800; font-size: 3rem; margin-bottom: 0px; }
    .sub-header { text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 30px; }
    
    /* Yan Panel */
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #ef4444; color: white; border: none; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN KONFİQURASİYASI ---
# Sənin yeni açarın bura daxil edildi
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Həm şəkil, həm mətn üçün ən stabil model
MODEL_NAME = "llama-3.2-11b-vision-preview"

def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov")
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.messages = []
        st.rerun()

# --- 4. ƏSAS EKRAN ---
st.markdown("<h1 class='main-header'>A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Abdullah Mikayılov tərəfindən yaradılmış 10x dahi sistem.</p>", unsafe_allow_html=True)

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. ULTRA GİRİŞ SİSTEMİ (+) ---
# accept_file=True sayəsində şəkil yükləmə düyməsi aktivdir
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu şəkli analiz et."
    image_b64 = None
    
    # Şəkil yüklənibsə onu emal et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400, caption="Yüklənən şəkil")
            image_b64 = encode_image(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # A-Zəka-nın cavabı
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            if image_b64:
                # Şəkilli sorğu formatı
                messages = [
                    {"role": "system", "content": "Sən dahi A-Zəka-san. Şəkilləri görürsən və Abdullahın köməkçisisən."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                        ]
                    }
                ]
            else:
                # Sadə mətn sorğusu
                messages = [{"role": "system", "content": "Sən dahi A-Zəka-san."}] + st.session_state.messages

            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
