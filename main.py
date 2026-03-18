import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. ULTRA DİZAYN VƏ AYARLAR ---
st.set_page_config(page_title="A-Zəka 10x Ultra", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    /* Arxa fon və ümumi şriftlər */
    .stApp { background-color: #f4f7fb; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Əsas başlıq */
    .ultra-title {
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 3.8rem;
        margin-bottom: 5px;
        padding-top: 20px;
    }
    .sub-title { text-align: center; color: #555; font-size: 1.1rem; margin-bottom: 30px; font-weight: bold; }
    
    /* Mesaj qutuları (Çat kürəcikləri) */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #eaeaea;
    }
    
    /* Sol panel (Sidebar) düymələri */
    .stButton>button {
        background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff1c1c; box-shadow: 0 4px 10px rgba(255,75,75,0.4); }
</style>
""", unsafe_allow_html=True)

# --- 2. İDARƏETMƏ PANELİ VƏ BEYİN ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=100)
    st.markdown("### ⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.write("Güc: **Ultra 10x (Görmə Aktiv)**")
    st.divider()
    
    # Yeni sistemin işləməsi üçün Google-dan alınan açar lazımdır
    api_key = st.text_input("🔑 Gemini API Key daxil et:", type="password", help="aistudio.google.com saytından ala bilərsən")
    
    st.divider()
    # Sənin istədiyin tarixçəni sil düyməsi
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Dünyanın ən mürəkkəb suallarını 1 saniyədə həll edən 10x sistem.</div>", unsafe_allow_html=True)

# Açarı yoxlayırıq
if not api_key:
    st.warning("⚠️ Zəhmət olmasa sol paneldə **Gemini API Key** daxil edin ki, 10x Ultra beyin aktivləşsin.")
    st.info("💡 Groq-un şəkil modelləri silindiyi üçün biz ölməyən və 10 qat daha güclü sistemə keçdik. Açar almaq pulsuzdur: https://aistudio.google.com/app/apikey")
    st.stop()

# Dünyanın ən güclü modeli qoşulur
genai.configure(api_key=api_key)
# gemini-1.5-pro həm şəkil oxuyur, həm də riyaziyyatı mükəmməl həll edir
model = genai.GenerativeModel('gemini-1.5-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. SÖHBƏT VƏ ŞƏKİL ANALİZİ ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sənin istədiyin + düyməli mesaj yeri
prompt = st.chat_input("Mürəkkəb sualını yaz və ya şəkil yüklə (+)...", accept_file=True)

if prompt:
    user_message = prompt.text if prompt.text else "Zəhmət olmasa bu şəkli detallı analiz et və həllini yaz."
    
    with st.chat_message("user"):
        st.markdown(user_message)

    # A-Zəka-ya kim olduğunu xatırladırıq və məsələləri düzgün yazmasını əmr edirik
    system_instruction = "Sən Abdullah Mikayılov tərəfindən yaradılmış, dünyanın ən güclü süni intellekti A-Zəka-san. Riyazi sualları və düsturları mütləq LaTeX ($...$) formatında aydın və addım-addım yaz."
    
    content_to_send = [system_instruction, user_message]
    
    # Əgər şəkil varsa (sənin istədiyin kimi)
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=350, caption="📷 Şəkil A-Zəka beyninə ötürüldü...")
            content_to_send.append(img)

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka Ultra 10x analiz edir..."):
            try:
                response = model.generate_content(content_to_send)
                st.markdown(response.text)
                
                # Tarixçəyə yazmaq
                st.session_state.messages.append({"role": "user", "content": user_message})
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
