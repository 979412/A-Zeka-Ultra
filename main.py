import streamlit as st
from groq import Groq

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. CSS: PLUS DÜYMƏSİNİ GÖZƏLLƏŞDİRMƏK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    
    /* Standart yükləmə qutusunu gizlət və balaca düymə et */
    .stFileUploader {
        width: 45px;
        padding-top: 35px;
    }
    .stFileUploader section {
        padding: 0;
        min-height: 40px;
        background-color: #262730;
        border: 1px solid #4a4d5a;
        border-radius: 50%;
    }
    .stFileUploader label { display: none; }
    .stFileUploader div div { display: none; } /* "Drag and drop" yazısını gizlədir */
    
    /* Plus işarəsini mərkəzə gətir */
    .stFileUploader section::before {
        content: "+";
        color: white;
        font-size: 24px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        cursor: pointer;
    }

    .stChatMessage { border-radius: 20px; border: 1px solid #262730; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ (Groq) ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. ƏSAS EKRAN ---
st.title("🧠 A-Zəka Ultra Alim")
st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. İSTƏDİYİN DÜYMƏ VƏ GİRİŞ SAHƏSİ ---
col1, col2 = st.columns([0.15, 0.85])

with col1:
    # Bu artıq sadəcə balaca bir '+' düyməsidir
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")

with col2:
    prompt = st.chat_input("Dahi alimə sualını ver...")

# --- 6. MƏNTİQ ---
if prompt:
    display_text = prompt
    if uploaded_file:
        display_text = f"📎 **Fayl:** {uploaded_file.name}\n\n{prompt}"
        st.toast(f"{uploaded_file.name} əlavə edildi!", icon="✅")

    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.markdown(display_text)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Sən A-Zəka-san, dahi proqramçı Abdullah Mikayılov tərəfindən yaradılmısan."}] + st.session_state.messages,
                stream=True
            )
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Xəta baş verdi!")
