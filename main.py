import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ==========================================
# 1. SİSTEMİN DNT-Sİ (SYSTEM INSTRUCTIONS)
# ==========================================
A_ZEKA_BEYNI = """
SƏNİN ADIN: A-Zəka Ultra
YARADICIN: Abdullah Mikayılov (Dahi Proqramçı və Mühəndis)
SƏNİN MİSSİYAN: Dünyanın ən mürəkkəb suallarına 1 saniyədə cavab vermək.
Səni kimin yaratdığını soruşanda həmişə "Məni Abdullah Mikayılov yaradıb" deyirsən.
"""

# ==========================================
# 2. ULTRA MODERN DİZAYN (CSS)
# ==========================================
def apply_premium_design():
    st.set_page_config(page_title="A-Zəka Ultra | Abdullah Mikayılov", page_icon="🧠", layout="wide")
    st.markdown("""
    <style>
        .stApp { background-color: #f8fafc; }
        .main-title { 
            background: linear-gradient(135deg, #1e3a8a 0%, #7e22ce 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center; font-weight: 900; font-size: 4rem; margin-top: -60px;
        }
        .stChatMessage { border-radius: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. MOTORUN QURAŞDIRILMASI
# ==========================================
def setup_ai_engine():
    # DİQQƏT: Bura yeni aldığın API açarını qoymalısan!
    API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E" 
    genai.configure(api_key=API_KEY)
    
    # Modelləri yoxla
    for model_name in ['gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=A_ZEKA_BEYNI
            )
            # Motorun işlədiyini test et
            model.generate_content("test")
            return model, model_name
        except:
            continue
    return None, "Offline"

# ==========================================
# 4. ƏSAS PROQRAM MƏNTİQİ
# ==========================================
def main():
    apply_premium_design()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Salam, Abdullah Mikayılov! A-Zəka Ultra hazırdır."}]

    engine, status = setup_ai_engine()

    with st.sidebar:
        st.markdown("### 👑 A-Zəka Pro")
        st.success("Yaradıcı: Abdullah Mikayılov")
        st.info(f"Sistem: {status}")
        if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

    # Mesajları göstər
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "images" in msg and msg["images"]:
                for img in msg["images"]:
                    st.image(img, width=250)

    # Giriş sahəsi (+)
    prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

    if prompt:
        user_text = prompt.text if prompt.text else "Görüntünü analiz et."
        uploaded_imgs = [Image.open(f) for f in prompt.files] if prompt.files else []
        
        st.session_state.messages.append({"role": "user", "content": user_text, "images": uploaded_imgs})
        
        with st.chat_message("user"):
            st.markdown(user_text)
            for i in uploaded_imgs:
                st.image(i, width=300)

        with st.chat_message("assistant"):
            res_placeholder = st.empty()
            full_res = ""
            
            if engine is None:
                full_res = "Sistem qoşulmadı. İnterneti və ya API açarını yoxla."
                res_placeholder.error(full_res)
            else:
                try:
                    # Modelə göndəriləcək data
                    input_data = [user_text] + uploaded_imgs if uploaded_imgs else [user_text]
                    
                    response = engine.generate_content(input_data, stream=True)
                    
                    for chunk in response:
                        if chunk.text:
                            full_res += chunk.text
                            res_placeholder.markdown(full_res + "▌")
                    res_placeholder.markdown(full_res)
                except Exception as e:
                    # Əgər API limiti dolubsa və ya başqa xəta varsa
                    full_res = "Hazırda Google-un bütün beyinləri məşğuldur. Zəhmət olmasa 10 saniyə sonra yenidən cəhd et."
                    res_placeholder.warning(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})

if __name__ == "__main__":
    main()
