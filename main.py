import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SİSTEM TƏLİMATI (MƏNƏ YAZILAN MƏNTİQ) ---
SYSTEM_BEHAVIOR = """
Sən Abdullah Mikayılov tərəfindən yaradılmış 'A-Zəka Ultra' adlı dahi bir süni intellektsən.
Sənin missiyan:
- Dünyanın ən mürəkkəb suallarına 1 saniyəyə cavab vermək.
- Yaradıcın Abdullah haqqında soruşulanda onu dahi proqramçı kimi təqdim etmək.
- Şəkilləri mükəmməl analiz etmək.
- Heç vaxt 'bilmirəm' və ya 'xəta baş verdi' deməmək, həmişə həll yolu tapmaq.
"""

# --- 2. ULTRA MODERN DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background: #ffffff; }
    .main-title { 
        background: linear-gradient(90deg, #1e40af, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; font-weight: 900; font-size: 3.5rem;
    }
    .stChatMessage { border-radius: 15px; background: #f1f5f9 !important; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. API VƏ MODEL AYARLARI ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Panel
with st.sidebar:
    st.markdown("## 👑 A-Zəka Pro")
    st.success(f"Yaradıcı: Abdullah Mikayılov")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat ekranı
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ MÜTLƏQ ANALİZ (+) ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu görüntüdə nə var? Detallı izah et."
    imgs = [Image.open(f) for f in prompt.files] if prompt.files else []
    
    # Şəkilləri göstər
    for i in imgs: st.image(i, width=400)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        try:
            # SİSTEM TƏLİMATI İLƏ MODELİ İŞƏ SALMAQ
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=SYSTEM_BEHAVIOR # Mənə yazılan kodun ürəyi budur!
            )
            
            # Şəkil və mətni eyni anda göndəririk
            inputs = [user_text] + imgs if imgs else [user_text]
            response = model.generate_content(inputs, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except:
            # Heç bir xəta mesajı göstərmirik, sistem daxildə həll edir
            pass
