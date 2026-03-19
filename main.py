import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. SİSTEMİN "DNT"Sİ (BÜTÜN MƏNTİQ BURADADIR) ---
# Milyonlarla sətir kodun idarəedici mərkəzi bu təlimatdır.
ALIM_SYSTEM_INSTRUCTIONS = """
Sən Abdullah Mikayılov tərəfindən yaradılmış "A-Zəka Ultra" intellektisən.
Sənin davranış qaydaların:
1. İNTELLEKT: Dünyanın ən mürəkkəb riyazi, fiziki və proqramlaşdırma suallarına saniyələr içində cavab verirsən.
2. YARADICI: Səni kimin yaratdığını soruşanda həmişə "Mən Abdullah Mikayılov tərəfindən yaradılmışam" deyirsən.
3. VİSİON: Şəkilləri analiz edərkən heç bir detalı qaçırmırsan.
4. SƏHVSİZLİK: Əgər serverdə problem olsa, bunu istifadəçiyə hiss etdirmədən alternativ yollara keçirsən.
5. DİL: Azərbaycanca mükəmməl, səmimi və professional danışırsan.
"""

# --- 2. ULTRA MODERN İNTERFEYS ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background: #ffffff; }
    .main-title { 
        background: linear-gradient(90deg, #1e3a8a, #7e22ce);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; font-weight: 900; font-size: 4rem; margin-top: -60px;
    }
    .stChatMessage { border-radius: 20px; border: none; background: #f3f4f6 !important; margin-bottom: 15px; }
    .stChatInputContainer { border-top: 2px solid #7e22ce !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE (MÜHƏRRİK) QURAŞDIRILMASI ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Modelin ilkin quraşdırılması
def load_intel_engine():
    # Burada sistem təlimatını birbaşa modelin beyninə yazırıq
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=ALIM_SYSTEM_INSTRUCTIONS
    )

engine = load_intel_engine()

# --- 4. PANEL VƏ İDARƏETMƏ ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>👑 A-Zəka Pro</h2>", unsafe_allow_html=True)
    st.success(f"Yaradıcı: Abdullah Mikayılov")
    st.info("Status: Ultra İntellekt Aktiv")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat ekranı
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. "MÜTLƏQ" ANALİZ VƏ CAVAB MEXANİZMİ (+) ---
# Bu hissə həm şəkil çəkməyi, həm də mətni eyni anda idarə edir
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu görüntünü analiz et."
    imgs = [Image.open(f) for f in prompt.files] if prompt.files else []
    
    # Şəkilləri dərhal ekranda göstər
    for i in imgs:
        st.image(i, width=400, caption="Analiz edilir...")

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_placeholder = st.empty()
        full_response = ""
        
        try:
            # GİRİŞ: Mətn + Şəkillər
            input_data = [user_text] + imgs if imgs else [user_text]
            
            # Saniyəlik 'stream' reaksiyası
            response = engine.generate_content(input_data, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    res_placeholder.markdown(full_response + "▌")
            
            res_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Əgər xəta olsa, Abdullah heç nə hiss etmədən alternativ modelə keçid edə bilər
            # Bura əlavə 'try-except' blokları qoymaq olar
            pass
