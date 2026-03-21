import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# =====================================================================
# BÖLMƏ 1: KONFİQURASİYA
# =====================================================================
APP_NAME = "A-Zəka Ultra"
CREATOR = "Abdullah Mikayılov"
GLOBAL_API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"

# =====================================================================
# BÖLMƏ 2: DAHİ NÜVƏ (Şəkil və Mətn üçün Tam Sabitlik)
# =====================================================================
class AzekaEngine:
    def __init__(self, api_key, temperature):
        self.api_key = api_key
        self.temp = temperature
        # Ən yeni model adları bunlardır:
        self.models_to_try = [
            'gemini-1.5-flash', 
            'gemini-1.5-pro',
            'gemini-pro-vision' # Şəkil üçün ehtiyat model
        ]

    def get_model(self, has_image=False):
        genai.configure(api_key=self.api_key)
        # Şəkil varsa, mütləq 1.5-flash və ya pro istifadə edilməlidir
        for m_name in self.models_to_try:
            try:
                model = genai.GenerativeModel(model_name=m_name)
                # Kiçik bir yoxlama
                return model, m_name
            except:
                continue
        return None, None

    def generate(self, prompt, context, images=None):
        model, active_m = self.get_model(has_image=bool(images))
        
        if not model:
            yield "🆘 KRİTİK XƏTA: Google API ilə bağlantı qurula bilmədi."
            return

        try:
            # Şəkil və mətni Google-un istədiyi formatda birləşdiririk
            contents = []
            if images:
                for img in images:
                    contents.append(img)
            contents.append(prompt)

            response = model.generate_content(
                contents,
                stream=True,
                generation_config={"temperature": self.temp}
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"⚠️ Xəta: Model şəkil analizini dəstəkləmir və ya {str(e)}"

# =====================================================================
# BÖLMƏ 3: INTERFEYS
# =====================================================================
def main():
    st.set_page_config(page_title=APP_NAME, layout="wide")
    
    # Dizayn hissəsini bura əlavə edə bilərsən (st.markdown ilə)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Salam Abdullah! Şəkilləri bura ata bilərsən."}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input (Şəkil dəstəyi ilə)
    user_input = st.chat_input("Sual və ya şəkil...", accept_file=True)

    if user_input:
        txt = user_input.text if user_input.text else "Bu şəkildə nə var?"
        # Şəkilləri PIL formatına salırıq
        imgs = [Image.open(f) for f in user_input.files] if user_input.files else []

        st.session_state.messages.append({"role": "user", "content": txt})
        with st.chat_message("user"):
            st.markdown(txt)
            for img in imgs:
                st.image(img, width=300)

        with st.chat_message("assistant"):
            res_box = st.empty()
            full_res = ""
            engine = AzekaEngine(GLOBAL_API_KEY, 0.7)
            
            with st.spinner("Analiz edilir..."):
                for chunk in engine.generate(txt, st.session_state.messages, imgs):
                    full_res += chunk
                    res_box.markdown(full_res + " ▌")
                res_box.markdown(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})

if __name__ == "__main__":
    main()
