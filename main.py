import streamlit as st
from groq import Groq
import base64 # Şəkilləri kodlaşdırmaq üçün lazımdır

# --- Səhifə və API Ayarları ---
st.set_page_config(page_title="A-Zəka Ultra Vision", page_icon="👀", layout="centered")

# API açarını təhlükəsiz şəkildə secrets-dən oxuyuruq
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    # Lokal test üçün açarı bura yaza bilərsən, amma GitHub-a yükləmə!
    api_key = "GSK_..." # Öz API açarınla əvəz et

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Şəkil faylını base64 formatına çevirən funksiya
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- İnterfeys ---
st.title("👀 A-Zəka Ultra Vision")
st.markdown("Şəkilləri analiz edən dahi AI köməkçin.")

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Əgər mesajın məzmunu siyahıdırsa (multimodal format), mətni göstəririk
        if isinstance(msg["content"], list):
            for content_part in msg["content"]:
                if content_part["type"] == "text":
                    st.markdown(content_part["text"])
        else:
            st.markdown(msg["content"])

# --- Sual və Şəkil Girişi ---
# accept_file=True ilə chat_input-a fayl yükləmə imkanı veririk
prompt = st.chat_input("Şəkil yüklə və ya sualını yaz...", accept_file=True)

# --- Məntiq ---
if prompt:
    user_text = prompt.text if prompt.text else ""
    user_messages_to_display = [] # Ekranda göstərmək üçün sətirlər siyahısı

    # Mesajın məzmununu multimodal formatda hazırlayırıq
    message_content = [{"type": "text", "text": user_text}]
    
    # Əgər şəkil yüklənibsə
    if prompt.files:
        for uploaded_file in prompt.files:
            if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                # Şəkli base64 formatına çeviririk
                base64_image = encode_image(uploaded_file)
                # Mesajın məzmununa şəkli də əlavə edirik
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{uploaded_file.type};base64,{base64_image}"
                    }
                })
                # Ekranda faylın adını göstərmək üçün siyahıya əlavə edirik
                user_messages_to_display.append(f"🖼️ **Şəkil əlavə edildi:** {uploaded_file.name}")

    # İstifadəçi mesajını sessiyaya əlavə edirik (ekran üçün sadələşdirilmiş format)
    display_content = user_text + ("\n\n" + "\n".join(user_messages_to_display) if user_messages_to_display else "")
    st.session_state.messages.append({"role": "user", "content": display_content})
    
    # İstifadəçi mesajını dərhal ekrana yazırıq
    with st.chat_message("user"):
        st.markdown(display_content)

    # Botun cavabı
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Groq-a göndəriləcək mesajlar siyahısını hazırlayırıq
        api_messages = [
            {"role": "system", "content": "Sən A-Zəka-san, dahi proqramçı Abdullah Mikayılov tərəfindən yaradılmısan. Şəkilləri analiz etmək qabiliyyətin var."}
        ]
        
        # Sessiya tarixçəsini API-ın multimodal formatına uyğunlaşdırırıq
        # Bu sadələşdirilmiş versiyadır, daha mürəkkəb tarixçə üçün əlavə məntiq lazımdır.
        api_messages.append({"role": "user", "content": message_content})

        try:
            # Şəkil analizi üçün multimodal modeldən istifadə edirik (məsələn, llama-3.2-11b-vision-preview)
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview", # Multimodal model adı
                messages=api_messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta baş verdi: {e}")
