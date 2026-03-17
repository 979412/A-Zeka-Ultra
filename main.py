import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# --- 2. PROFESSIONAL DİZAYN ---
st.markdown("""
<style>
    .stApp { background-color: #fcfcfc; }
    .stChatMessage { border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; border-left: 5px solid #007bff; }
    .main-title { color: #0E1117; text-align: center; font-weight: 900; font-size: 3rem; margin-top: -50px; }
</style>
""", unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ ---
api_key = "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"
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- 4. SOL PANEL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6134/6134346.png", width=80)
    st.title("A-Zəka Panel")
    st.info("Status: **R1-Thinking Aktiv** 🔥")
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
prompt = st.chat_input("Riyazi problemi daxil edin...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu problemi ən dəqiq şəkildə həll et."
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

    # --- 7. ASSİSTANT CAVABI (Güncəl Modellər) ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # GÜNCƏL MODELLƏR:
            if is_image:
                # Şəkil analiz etmək üçün ən güclü aktiv Vision modeli
                target_model = "llama-3.2-90b-vision-preview"
            else:
                # Riyaziyyatda səhv etməmək üçün ən güclü düşünən beyin
                target_model = "deepseek-r1-distill-llama-70b" 
            
            system_prompt = (
                "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılmış dahi riyaziyyatçısan. "
                "Bütün riyazi ifadələri mütləq LaTeX formatında ($...$ və ya $$...$$) yaz.\n"
                "Həlli dərhal vermə, əvvəlcə dərindən düşün və addım-addım professional izah et."
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
            # Əgər yenə model xətası çıxarsa, ehtiyat modelə keçid
            st.warning("Model yenilənir, ehtiyat beyinə keçid edilir...")
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Riyaziyyatı dəqiq həll et."}] + st.session_state.messages,
                    stream=True
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except:
                st.error(f"Sistem xətası: {e}")
