import streamlit as st
from groq import Groq

# --- DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠")

st.markdown("""
<style>
    .stApp { background-color: #f4f7fb; }
    .title { text-align: center; color: #1e3c72; font-weight: 800; font-size: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- KONFİQURASİYA ---
# Sənin rəsmi açarın
API_KEY = "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"
client = Groq(api_key=API_KEY)

# ƏN STABİL MODEL (Bu model mütləq işləyəcək)
MODEL = "llama3-8b-8192"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 class='title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Giriş sahəsi
prompt = st.chat_input("Sualını yaz...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Cavabın alınması
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Sən Abdullah tərəfindən yaradılmış dahi A-Zəka-san."},
                    {"role": "user", "content": prompt}
                ]
            )
            final_res = response.choices[0].message.content
            st.markdown(final_res)
            
            # Yaddaşa yaz
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": final_res})
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
