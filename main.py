import streamlit as st
from groq import Groq

# --- 1. SƏHİFƏ AYARLARI VƏ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 15px; border: 1px solid #4a4d5a; }
    .stChatMessage { border-radius: 20px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    
    /* Plus düyməsi və Giriş sahəsini yan-yana gətirmək üçün */
    [data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* File uploader-i gizlədib sadəcə icon kimi göstərmək üçün kiçik hiylə */
    .stFileUploader section {
        padding: 0;
        min-height: unset;
    }
    .stFileUploader label {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BEYİN MƏRKƏZİ (Groq) ---
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

# --- 6. PLUS DÜYMƏSİ VƏ SUAL GİRİŞİ (Professional Layout) ---
# Düymə və yazma yerini yan-yana qoyuruq
input_col, button_col = st.columns([0.1, 0.9])

with input_col:
    # Bu sənin istədiyin '+' düyməsinin funksiyasını yerinə yetirir
    # İstifadəçi bura şəkil ata bilər
    uploaded_file = st.file_uploader("+", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")

with button_col:
    prompt = st.chat_input("Dahi alimə sualını ver...")

# --- 7. PROSES ---
if prompt:
    # Əgər fayl yüklənibsə, mesaja fayl məlumatını da əlavə edirik
    display_content = prompt
    if uploaded_file:
        display_content = f"📎 **Fayl əlavə edildi:** {uploaded_file.name}\n\n" + prompt

    st.session_state.messages.append({"role": "user", "content": display_content})
    with st.chat_message("user"):
        st.markdown(display_content)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Sən 'A-Zəka'-san. Səni dahi proqramçı Abdullah Mikayılov yaradıb. Sən hər şeyi saniyələr içində bilən Ultra Alimsən."}
                ] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Bağlantı xətası! VPN-i yoxlayın.")
