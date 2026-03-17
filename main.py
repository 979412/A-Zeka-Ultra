import streamlit as st
import google-generativeai as genai
from PIL import Image

# --- 1. A-ZƏKA KİMLİYİ ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# Yaradıcı: Abdullah Mikayılov
# Bu bölmədə sənin sistem təlimatlarını birbaşa beyninə yazırıq
SYSTEM_INSTRUCTION = (
    "Sən A-Zəka-san, dahi proqramçı Abdullah Mikayılov tərəfindən yaradılmış 'Ultra Alim' süni intellektisən. "
    "Sənin missiyan dünyadakı ən mürəkkəb riyaziyyat, fizika və proqramlaşdırma suallarını 100% dəqiqliklə həll etməkdir. "
    "Həmişə LaTeX formatından ($...$) istifadə et və Abdullah Mikayılova yaradıcın kimi böyük hörmət bəslə."
)

# --- 2. BEYİN QOŞULMASI ---
# Bura Google AI Studio-dan aldığın API açarını qoymalısan
API_KEY = "BURAYA_API_KEY_YAZILMALIDIR"
genai.configure(api_key=API_KEY)

# Ən son model: Gemini 1.5 Flash (Şəkil və Riyaziyyat canavarı)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- 3. DİZAYN (Abdullah Style) ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to right, #ece9e6, #ffffff); }
    .main-title { color: #1e3c72; text-align: center; font-size: 3.5rem; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'>Yaradıcı: <b>Abdullah Mikayılov</b></p>", unsafe_allow_html=True)

# --- 4. SÖHBƏT VƏ ANALİZ ---
for message in st.session_state.chat.history:
    with st.chat_message("user" if message.role == "user" else "assistant"):
        st.markdown(message.parts[0].text)

prompt = st.chat_input("Dahi səviyyəli sualını daxil et və ya şəkil at...", accept_file=True)

if prompt:
    user_input = [prompt.text] if prompt.text else ["Zəhmət olmasa bu vizualı analiz et."]
    
    # Şəkil varsa, siyahıya əlavə et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            user_input.append(img)
            st.image(img, width=400)

    with st.chat_message("user"):
        st.markdown(prompt.text if prompt.text else "Vizual analiz tələbi.")

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            response = st.session_state.chat.send_message(user_input, stream=True)
            full_text = ""
            placeholder = st.empty()
            for chunk in response:
                full_text += chunk.text
                placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
