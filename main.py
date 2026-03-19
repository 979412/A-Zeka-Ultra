import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="A-Zəka Model Axtarışı", page_icon="🔍")

st.markdown("<h1 style='text-align: center; color: #2563eb;'>🔍 A-Zəka: Detektiv Rejimi</h1>", unsafe_allow_html=True)
st.write("Google serverləri ilə əlaqə qurulur və aktiv modellər axtarılır...")

# Sənin işlək açarın
API_KEY = "AIzaSyBiPhToQs_WMs_qtY_seJxhCEVd2r1Y7yk"
genai.configure(api_key=API_KEY)

try:
    # Google-dan aktiv modellərin siyahısını istəyirik
    models = genai.list_models()
    
    tapilan_modeller = []
    for m in models:
        # Yalnız mətn/şəkil yarada bilən modelləri seçirik
        if 'generateContent' in m.supported_generation_methods:
            tapilan_modeller.append(m.name)
            
    if tapilan_modeller:
        st.success("✅ Aşağıdakı modellər sənin API açarın üçün tam aktivdir:")
        for model_adi in tapilan_modeller:
            st.code(model_adi)
    else:
        st.error("❌ Sənin API açarın işləyir, amma Google sənə heç bir model verməyib.")
        
except Exception as e:
    st.error(f"⚠️ Kritik xəta baş verdi: {str(e)}")
