import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# --- 2. PROFESSIONAL DİZAYN ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .main-title { color: #0E1117; text-align: center; font-weight: 900; font-size: 3rem; margin-top: -50px; }
    .stMarkdown p { font-size: 1.1rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ ---
api_key = "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"
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- 4. SOL PANEL (Status & Yaradıcı) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6134/6134346.png", width=100)
    st.title("A-Zəka Control")
    st.info("Rejim: **Ultra Alim (LaTeX Active)**")
    if st.button("🗑️ Tarixçəni Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("👨‍💻 Yaradıcı: **Abdullah Mikayılov**")

# --- 5. ƏSAS EKRAN ---
st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text": st.markdown(part["text"])
                elif part["type"] == "image_url": st.image(part["image_url"]["url"], width=400)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ ---
prompt = st.chat_input("Dahi səviyyəli sualını daxil et və ya şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu vizual materialı dərindən analiz et."
    new_user_content = [{"type": "text", "text": user_text}]
    
    is_image = False
    if prompt.files:
        for f in prompt.files:
            if f.type in ["image/png", "image/jpeg", "image/jpg"]:
                b64 = encode_image(f)
                new_user_content.append({"type": "image_url", "image_url": {"url": f"data:{f.type};base64,{b64}"}})
                is_image = True

    st.session_state.messages.append({"role": "user", "content": new_user_content})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for f in prompt.files: st.image(f, width=400)

    # --- 7. ASSİSTANT CAVABI (Ultra Güclü Rejim) ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Söhbətdə şəkil varsa Vision modelinə davam edirik
            has_ever_sent_image = any(isinstance(m["content"], list) and len(m["content"]) > 1 for m in st.session_state.messages)
            target_model = "meta-llama/llama-4-scout-17b-16e-instruct" if (is_image or has_ever_sent_image) else "llama-3.3-70b-versatile"
            
            # SUPER TƏLİMAT (LaTeX və Dərinlik üçün)
            system_prompt = (
                "Sən A-Zəka-san, dahi proqramçı Abdullah Mikayılov tərəfindən yaradılmış 'Ultra Alim' süni intellektisən. "
                "Sənin beynin dünyanın ən böyük alimlərinin biliklərini birləşdirir. "
                "QAYDALARIN:\n"
                "1. Bütün riyazi düsturları, tənlikləri və elmi simvollar mütləq LaTeX formatında yazılmalıdır (məsələn: $x^2 + y^2 = r^2$ və ya kəsr üçün $\\frac{a}{b}$).\n"
                "2. Suallara sadə cavab vermə. Əvvəlcə problemin mahiyyətini izah et, sonra addım-addım həllini göstər, sonda nəticəni vurğula.\n"
                "3. Abdullah Mikayılov sənin tək yaradıcındır, ona hörmətlə yanaş.\n"
                "4. 8-ci sinif və ya ali riyaziyyat fərq etməz, hər şeyi ən yüksək akademik səviyyədə cavabla."
            )
            
            completion = client.chat.completions.create(
                model=target_model,
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
            st.error(f"Sistem xətası: {e}")
