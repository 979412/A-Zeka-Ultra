import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# =====================================================================
# BÖLMƏ 1: MƏRKƏZİ SİSTEM KONFİQURASİYASI
# =====================================================================
APP_NAME = "A-Zəka Ultra"
APP_VERSION = "Global Edition 6.0 (Titan Supreme)"
CREATOR = "Abdullah Mikayılov"
CREATOR_TITLE = "Proqram Təminatı Mühəndisi və Süni İntellekt Mütəxəssisi"
GLOBAL_API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E" #

A_ZEKA_BEYNI = f"""
SƏNİN ADIN: {APP_NAME}
YARADICIN: {CREATOR} ({CREATOR_TITLE})
MİSSİYAN: Dünyanın ən dahi süni intellekti olaraq mürəkkəb sualları dəqiqliklə cavablandırmaq.
DAVRANIŞ: İntellektual, nəzakətli və mühəndis dəqiqliyi ilə cavab ver.
"""

# =====================================================================
# BÖLMƏ 2: PREMİUM LIGHT UI DİZAYNI
# =====================================================================
def apply_design():
    st.set_page_config(page_title=f"{APP_NAME}", page_icon="🤖", layout="wide")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'SF Pro Display', sans-serif; background-color: #f4f7f9; }
    .stChatMessage { background-color: white !important; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 10px; }
    .global-title { background: linear-gradient(135deg, #2563eb, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 800; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# BÖLMƏ 3: DAHİ İNTELLEKT NÜVƏSİ (FALLBACK LOGIC)
# =====================================================================
class AzekaEngine:
    def __init__(self, api_key, temperature):
        self.api_key = api_key
        self.temp = temperature
        # İntellekt Pilləkəni: Biri işləməsə, digəri işə düşür
        self.models = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro'] #

    def get_active_model(self):
        genai.configure(api_key=self.api_key)
        for m in self.models:
            try:
                model = genai.GenerativeModel(model_name=m, system_instruction=A_ZEKA_BEYNI)
                model.generate_content("test", generation_config={"max_output_tokens": 1})
                return model, m
            except: continue
        return None, None

    def generate(self, prompt, context_messages, images=None):
        model, m_name = self.get_active_model()
        if not model: yield "🆘 Bağlantı xətası: Heç bir nüvə cavab vermir."; return
        
        try:
            # Kontekstual Yaddaş: Son 5 mesajı xatırla
            history = context_messages[-5:]
            full_prompt = f"Tarixçə: {history}\n\nYeni Sual: {prompt}"
            
            payload = [full_prompt]
            if images: payload.extend(images)
            
            response = model.generate_content(payload, stream=True, generation_config={"temperature": self.temp})
            for chunk in response:
                if chunk.text: yield chunk.text
        except Exception as e:
            yield f"⚠️ Texniki xəta: {str(e)}"

# =====================================================================
# BÖLMƏ 4: ƏSAS TƏTBİQ
# =====================================================================
def main():
    apply_design()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Salam, mən A-Zəka. Səni dinləyirəm, dahi yaradıcım."}]

    # Sidebar
    with st.sidebar:
        st.title(f"👑 {APP_NAME}")
        st.caption(f"Yaradıcı: {CREATOR}") #
        st.divider()
        temp = st.slider("Yaradıcılıq", 0.0, 1.0, 0.7)
        if st.button("🗑️ Yaddaşı Təmizlə"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()

    # Main UI
    st.markdown(f"<div class='global-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    user_input = st.chat_input("Dahi yaradıcı, əmriniz nədir?", accept_file=True)

    if user_input:
        txt = user_input.text if user_input.text else "Təsviri analiz et."
        imgs = [Image.open(f) for f in user_input.files] if user_input.files else []

        st.session_state.messages.append({"role": "user", "content": txt})
        with st.chat_message("user"): st.markdown(txt)

        with st.chat_message("assistant"):
            res_box = st.empty()
            full_res = ""
            engine = AzekaEngine(GLOBAL_API_KEY, temp)
            for chunk in engine.generate(txt, st.session_state.messages, imgs):
                full_res += chunk
                res_box.markdown(full_res + " ▌")
            res_box.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

if __name__ == "__main__":
    main()
