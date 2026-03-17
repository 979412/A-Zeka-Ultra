import streamlit as st
from groq import Groq

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. GİZLİ API QURULUMU ---
# Bu hissə proqramı serverə qoyanda açarı 'Secrets' hissəsindən götürəcək
try:
    # Əgər lokalda işlədirsənsə, birbaşa açarı bura yaza bilərsən
    # Amma server üçün st.secrets istifadə etmək mütləqdir
    api_key = st.secrets["GROQ_API_KEY"]
except:
    # Lokalda yoxlamaq üçün öz açarını bura müvəqqəti qoya bilərsən
    api_key = "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"

client = Groq(api_key=api_key)

# --- 3. ULTRA ALİM TƏLİMATI ---
system_prompt = """
Sən 'A-Zəka'-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. 
Sən bütün dünya üçün çalışan, hər şeyi bilən Ultra Alimsən. 
Saniyələr içində ən mürəkkəb sualları həlli ilə cavablandırırsan.
"""

# --- 4. DİZAYN (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 12px; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. YADDAŞ VƏ SÖHBƏT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 A-Zəka Ultra Alim")
st.caption(f"Yaradıcı: Abdullah Mikayılov | Model: Llama-3 (Saniyəlik Sürət)")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. İSTİFADƏÇİ GİRİŞİ ---
prompt = st.chat_input("Dahi alimə sualını ver...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Bağlantı xətası! Zəhmət olmasa VPN-in aktiv olduğunu yoxlayın.")
