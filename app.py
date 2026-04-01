import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ==========================================================
# 1. CORE CONFIGURATION
# ==========================================================
# Sənin Gemini API Key
API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
genai.configure(api_key=API_KEY)

# Sürətli Analiz üçün Gemini Flash 1.5 modelini tənzimləyirik
generation_config = {
  "temperature": 0.4, # Daha kəsərli analiz üçün
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1024, # Cavabı qısa və kəsərli etmək üçün
}

try:
    vision_model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
except:
    st.error("Kritik Xəta: Gemini Mühərriki tapılmadı. API Key-i yoxla.")
    vision_model = None

# Söhbət yaddaşını yoxla
if "messages" not in st.session_state:
    st.session_state.messages = []
# Sonuncu şəkli yaddaşda saxla (təkrar analiz üçün)
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# ==========================================================
# 2. PURE WHITE UI DESIGN (AĞ RƏNG VƏ MODERN)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA Omni", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Ana Fon */
    .stApp {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    /* Başlıq */
    .main-title {
        font-size: 38px !important;
        font-weight: 800;
        text-align: center;
        color: #1a1a1a;
        padding: 10px;
        margin-bottom: 0px;
        border-bottom: 2px solid #f0f2f6;
    }
    
    /* Chat Mesajları */
    [data-testid="stChatMessage"] {
        border-radius: 12px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
        border: 1px solid #f0f2f6 !important;
    }
    
    /* User Mesajı */
    [data-testid="stChatMessageUser"] {
        background-color: #f8f9fa !important;
    }
    
    /* Assistant Mesajı */
    [data-testid="stChatMessageAssistant"] {
        background-color: #ffffff !important;
    }

    /* Gizli elementləri təmizlə */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)

# ==========================================================
# 3. CHAT LOGIC (INTEGRATED VISION)
# ==========================================================
# Köhnə mesajları göstər (Dizayn tam bu sətirdə başlayır)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Əgər mesajda şəkil varsa, onu eynilə WhatsApp kimi göstər
        if "image" in message and message["image"]:
            st.image(message["image"], width=300)

# Giriş hissəsi (accept_file=True avtomatik '+' ikonası yaradır)
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu təsviri professional analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    # 🧠 Sənin şəklin neçə analiz etdiyimi burada sistemə yükləyirəm
    SYSTEM_INSTRUCTION = """
    Sən Abdullah Mikayılov tərəfindən yaradılmış ZƏKA ULTRA-san. 
    İl 2026. Sən bir şəkli belə analiz edirsən:
    1.  **Giriş:** Şəkil daxil olan kimi detalları dərhal ayırd edirsən.
    2.  **Vizual Detallar:** Rənglər, kompozisiya, əsas mövzu və arxa planı təsvir edirsən.
    3.  **Məna:** Şəklin nə ifadə etdiyini, hansı mənanı verdiyini professional Azərbaycan dilində kəsərli izah edirsən.
    Cavabı həmişə Abdullahın vizyonuna uyğun, soyuqqanlı, dəqiq və professional ver.
    """

    # İstifadəçi mesajını ekrana və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text, "image": active_file})
    with st.chat_message("user"):
        st.markdown(user_text)
        if active_file:
            st.image(Image.open(active_file), width=300)

    # Cavab mexanizmi
    with st.chat_message("assistant"):
        with st.status("🚀 Düşünürəm...", expanded=True) as status:
            try:
                # 1. Prioritet: Əgər yeni şəkil atılıbsa, onu yaddaşa sal və analiz et
                if active_file and vision_model:
                    img = Image.open(active_file)
                    st.session_state.current_image = img # Daimi yaddaşa sal
                    st.write("🔍 Media analizi gedir...")
                    response = vision_model.generate_content([SYSTEM_INSTRUCTION, user_text, img]).text
                # 2. Əgər yaddaşda köhnə şəkil varsa, onu analiz et
                elif st.session_state.current_image and vision_model:
                    st.write("🔍 Yaddaşdakı media analizi gedir...")
                    response = vision_model.generate_content([SYSTEM_INSTRUCTION, user_text, st.session_state.current_image]).text
                # 3. Yoxdursa, ancaq mətni analiz et
                else:
                    st.write("⚡ Mətn analizi...")
                    st.error("Kritik Xəta: Gemini Şəkil Mühərriki hazır deyil. Ancaq mətn analiz edilə bilər.")
                    response = "Şəkil yüklənmədi və ya mühərrik hazır deyil."
                
                status.update(label="Tamamlandı!", state="complete")
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                status.update(label="Xəta!", state="error")
                st.error(f"Süni İntellekt Xətası: {str(e)}")

# Avtomatik scroll (Səhifəni aşağı çək)
st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
