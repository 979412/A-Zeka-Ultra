import streamlit as st
from groq import Groq
import os

# --- 1. SƏHİFƏ AYARLARI VƏ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 15px; border: 1px solid #4a4d5a; }
    .stChatMessage { border-radius: 20px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 10px; background-color: #2e3139; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BEYİN MƏRKƏZİ (Groq) ---
# Secrets-dən açarı götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

# --- 3. YADDAŞ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL PANEL ---
with st.sidebar:
    st.title("⚙️ A-Zəka Control")
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("Yaradıcı: **Abdullah Mikayılov**")

# --- 5. ƏSAS İNTERFEYS ---
st.title("🧠 A-Zəka Ultra Alim")
st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. SUAL VƏ CAVAB PROSESİ ---
prompt = st.chat_input("Dahi alimə sualını ver...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Dünyanın ən mürəkkəb suallarını cavablayan Alim Təlimatı
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Sən 'A-Zəka'-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. Sən hər şeyi saniyələr içində bilən Ultra Alimsən. Cavabların professional, dəqiq və həlli ilə olmalıdır."}
                ] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # --- YENİ ÖZƏLLİK: SƏSLİ OXUMA (OPSİONAL) ---
            # İstəsən bura Google-un pulsuz gTTS kitabxanasını əlavə edib cavabı səsləndirə bilərik.
            
        except Exception as e:
            st.error("Bağlantıda kiçik bir problem oldu. Zəhmət olmasa VPN-i və ya açarı yoxlayın.")
