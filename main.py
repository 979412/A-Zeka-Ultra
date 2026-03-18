import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. PREMİUM VİSUAL AYARLAR ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Mesaj Balonları */
    .stChatMessage { border-radius: 15px; border: 1px solid #e2e8f0; padding: 15px; margin-bottom: 10px; }
    
    /* Yan Panel */
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
    
    /* Başlıq */
    .ultra-title { color: #2563eb; text-align: center; font-size: 3rem; font-weight: 800; margin-bottom: 0px; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN KONFİQURASİYASI ---
# ƏGƏR BU AÇAR İŞLƏMƏSƏ, YENİSİNİ BURA YAPIŞDIR
API_KEY = "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"

def get_client():
    try:
        return Groq(api_key=API_KEY)
    except:
        return None

client = get_client()
STABLE_MODEL = "llama-3.2-11b-vision-preview" # Həm şəkil, həm mətn üçün ən stabil model

def encode_image(image):
    buffered = io.BytesIO()
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
st.markdown("<h1 class='ultra-title'>A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b;'>Dahi Abdullah tərəfindən idarə olunan 10x sistem.</p>", unsafe_allow_html=True)

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. GİRİŞ VƏ MƏNTİQ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    image_b64 = None
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            image_b64 = encode_image(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Şəkilli və ya mətni sorğu formatı
            if image_b64:
                messages = [
                    {"role": "system", "content": "Sən Abdullahın dahi A-Zəka-sısan. Şəkilləri dərindən analiz edirsən."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                        ]
                    }
                ]
            else:
                messages = [{"role": "system", "content": "Sən Abdullahın dahi A-Zəka-sısan."}] + st.session_state.messages

            completion = client.chat.completions.create(
                model=STABLE_MODEL,
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
            if "401" in str(e):
                st.error("❌ Xəta: API Key səhvdir və ya ləğv edilib. Lütfən yeni bir API Key daxil edin.")
            else:
                st.error(f"⚠️ Texniki xəta: {str(e)}")
