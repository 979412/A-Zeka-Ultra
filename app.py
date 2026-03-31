import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# ==========================================================
# 1. GLOBAL CORE SETUP (GEMINI STABLE 2026)
# ==========================================================
# Birbaşa açarı bura yazıram ki, xəta almayasan
API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
genai.configure(api_key=API_KEY)

# Modellərin sazlanması
# 1.5 Flash həm sürətli, həm də şəkil analizində çox güclüdür
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. PREMIUM VİSUAL İNTERFEYS
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v6.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #ffffff; color: #0f172a; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    h1 { text-align: center; color: #1a1a1a; font-weight: 900; }
    .stCaption { text-align: center; color: #94a3b8; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p class='stCaption'>GLOBAL v6.0 | MEMAR: A. MİKAYILOV | GEMINI POWERED</p>", unsafe_allow_html=True)
st.markdown("---")

# Tarixçəni ekrana çıxar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 3. INPUT VƏ MƏNTİQ
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else ""
    active_file = prompt.files[0] if prompt.files else None
    
    # Ekranda göstərmək üçün
    display_text = user_text if user_text else "🖼️ Şəkil yükləndi."
    st.session_state.messages.append({"role": "user", "content": display_text})
    
    with st.chat_message("user"):
        st.write(display_text)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.status("🚀 Zəka Ultra Analiz Edir...", expanded=False) as status:
            st.write("Neyron şəbəkə işə düşür...")
            
            try:
                # Sistem təlimatı
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026. Professional və vəhşi dərəcədə ağıllısan."
                
                content_parts = [system_instruction]
                
                # Əgər şəkil varsa, onu hissələrə əlavə et
                if active_file:
                    img = Image.open(active_file)
                    content_parts.append(img)
                
                # Mətni əlavə et
                if user_text:
                    content_parts.append(user_text)
                else:
                    content_parts.append("Bu şəkli analiz et.")

                # Cavabı al
                response = model.generate_content(content_parts)
                final_answer = response.text
                
                # Xüsusi Memar Tanınması (Opsional - Cavabdan sonra yoxlanılır)
                if "abdullah" in user_text.lower():
                    final_answer = "🛡️ **GİRİŞ:** Memar Abdullah Mikayılov tanındı. Buyurun, sistem sizin nəzarətinizdədir.\n\n" + final_answer

                status.update(label="Analiz Tamamlandı!", state="complete")
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})

            except Exception as e:
                error_msg = f"⚠️ **Xəta baş verdi:** {str(e)}"
                st.error(error_msg)
                status.update(label="Xəta!", state="error")
