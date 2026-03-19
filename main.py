import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ==========================================
# 1. SİSTEMİN DNT-Sİ
# ==========================================
A_ZEKA_BEYNI = "Sənin adın A-Zəka Ultra-dır. Abdullah Mikayılov tərəfindən yaradılmısan."

# ==========================================
# 2. MOTORUN QURAŞDIRILMASI
# ==========================================
def setup_ai_engine():
    # BURAYA YENİ ALDIĞIN AÇARI YAPIŞDIR
    API_KEY = "YENİ_API_AÇARINI_BURA_YAZ" 
    genai.configure(api_key=API_KEY)
    
    try:
        # Ən stabil modeli birbaşa işə salırıq
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=A_ZEKA_BEYNI
        )
        # Test sorğusu
        model.generate_content("test")
        return model, "1.0s Cavab Rejimi"
    except Exception as e:
        return None, f"Xəta: {str(e)}"

# ==========================================
# 3. ƏSAS İNTERFEYS
# ==========================================
def main():
    st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    engine, status = setup_ai_engine()

    with st.sidebar:
        st.title("🚀 A-Zəka Pro")
        st.success("Yaradıcı: Abdullah Mikayılov")
        st.info(f"Sistem: {status}")
        if st.button("🗑️ Tarixçəni Sil"):
            st.session_state.messages = []
            st.rerun()

    st.markdown("<h1 style='text-align: center;'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

    # Mesajları göstər
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Giriş
    prompt = st.chat_input("Sualını bura yaz, Abdullah...", accept_file=True)

    if prompt:
        user_text = prompt.text if prompt.text else "Şəkli analiz et."
        imgs = [Image.open(f) for f in prompt.files] if prompt.files else []
        
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)
            for i in imgs: st.image(i, width=300)

        with st.chat_message("assistant"):
            if engine:
                try:
                    content = [user_text] + imgs
                    response = engine.generate_content(content)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Google Server Xətası: {e}")
            else:
                st.error("Sistem Offline-dır. Yeni API açarı lazımdır.")

if __name__ == "__main__":
    main()
