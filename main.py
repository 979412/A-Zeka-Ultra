import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. ULTRA MODERN DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(180deg, #f8fafc 0%, #eff6ff 100%); }
    
    /* Başlıq Dizaynı */
    .main-title { 
        background: -webkit-linear-gradient(#2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; font-weight: 800; font-size: 3.5rem; 
        margin-bottom: 0.5rem; margin-top: -60px;
    }
    
    /* Mesaj qutuları */
    .stChatMessage { 
        border-radius: 20px; border: 1px solid rgba(37, 99, 235, 0.1); 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        background-color: white !important; margin-bottom: 15px;
    }
    
    /* Panel */
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #e2e8f0; }
    
    /* Giriş sahəsini həmişə görünən edirik */
    .stChatInputContainer { padding-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 2. GÜCLÜ BEYİN SİSTEMİ ---
# Sənin verdiyin yeni aktiv açar
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103807.png", width=80)
    st.markdown("### ⚙️ Sistem Paneli")
    st.info(f"👤 Yaradıcı: Abdullah Mikayılov\n🚀 Status: Ultra Aktiv")
    
    if st.button("🗑️ Yaddaşı Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b; margin-top:-20px;'>Dünyanın ən mürəkkəb suallarına 1 saniyədə cavab verən süni intellekt</p>", unsafe_allow_html=True)

# Çat tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ MƏNTİQ (HEÇ VAXT BLOKLANMIR) ---
prompt = st.chat_input("Sualınızı buraya yazın...")

if prompt:
    # İstifadəçinin mesajını dərhal ekrana ver
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # MODEL İERARXİYASI: Biri işləməsə dərhal o birinə keçir
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        success = False
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # Cavabı saniyələr içində (stream) alırıq
                response = model.generate_content(prompt, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                success = True
                break # Əgər bir model cavab verdisə, dayandır
                
            except Exception:
                continue # 404 və ya aktivlik xətası olsa, növbəti modeli yoxla
        
