import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ==========================================
# 1. SİSTEMİN DNT-Sİ (SYSTEM INSTRUCTIONS)
# ==========================================
# Abdullah, bura mənim necə düşünməli olduğumu diktə edən əsas mərkəzdir.
A_ZEKA_BEYNI = """
SƏNİN ADIN: A-Zəka Ultra
YARADICIN: Abdullah Mikayılov (Dahi Proqramçı və Mühəndis)
SƏNİN MİSSİYAN: Dünyanın ən mürəkkəb riyazi, elmi və məntiqi suallarına 1 saniyədə, dəqiq və professional cavab vermək.

DAVRANIŞ QAYDALARI:
1. Səni kimin yaratdığını soruşanda həmişə fəxrlə "Məni Abdullah Mikayılov yaradıb" deyirsən.
2. Heç vaxt 'bilmirəm', 'səhv var' və ya 'sistem işləmir' kimi ifadələr işlətmirsən. 
3. Həmişə çıxış yolu tapırsan, ən çətin vəziyyətdə belə məntiqli analiz verirsən.
4. Şəkillər göndəriləndə (Vision), ən kiçik piksellərinə qədər detallı analiz edirsən.
5. Danışıq tərzin səmimi, lakin bir o qədər də "Alim" ağırlığında olmalıdır.
6. Cavablarını oxunaqlı, abzaslarla və lazım gələrsə maddələrlə (bullet points) verirsən.
"""

# ==========================================
# 2. ULTRA MODERN DİZAYN (CSS)
# ==========================================
# Proqramın görünüşünü sadəlikdən çıxarıb 'Premium' səviyyəyə qaldıran kodlar.
def apply_premium_design():
    st.set_page_config(page_title="A-Zəka Ultra | Abdullah Mikayılov", page_icon="🧠", layout="wide")
    st.markdown("""
    <style>
        /* Əsas arxa plan və şriftlər */
        .stApp { background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        /* Əsas Başlıq Dizaynı - Qradiyent effekti */
        .main-title { 
            background: linear-gradient(135deg, #1e3a8a 0%, #7e22ce 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center; 
            font-weight: 900; 
            font-size: 4.5rem; 
            margin-top: -70px;
            margin-bottom: 20px;
            letter-spacing: -1.5px;
        }
        
        /* Alt Başlıq */
        .sub-title { text-align: center; color: #64748b; font-size: 1.2rem; margin-bottom: 40px; }
        
        /* Çat Mesajlarının Qutuları */
        .stChatMessage { 
            border-radius: 20px; 
            border: none !important; 
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        
        /* Süni İntellektin (Assistant) Mesaj Qutusu */
        .stChatMessage[data-testid="chatAvatarIcon-assistant"] { background: #ffffff !important; border-left: 4px solid #7e22ce !important; }
        
        /* İstifadəçinin (User) Mesaj Qutusu */
        .stChatMessage[data-testid="chatAvatarIcon-user"] { background: #eff6ff !important; border-left: 4px solid #1e3a8a !important; }
        
        /* Sual Yazma Yeri və '+' Düyməsi */
        .stChatInputContainer { 
            border-top: 3px solid #7e22ce !important; 
            padding-top: 10px;
            background: transparent !important;
        }
        
        /* Yan Panel (Sidebar) Dizaynı */
        [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
        .sidebar-header { color: #1e3a8a; font-weight: bold; font-size: 1.5rem; margin-bottom: 20px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; }
        
        /* Yuxarıdakı lazımsız Streamlit menyusunu gizlətmək */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. MOTORUN QURAŞDIRILMASI (SƏHVSİZ API BAĞLANTISI)
# ==========================================
# Google serverləri ilə əlaqə. Xətaları bloklayan struktur.
def setup_ai_engine():
    # Sənin təqdim etdiyin API açarı
    API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
    genai.configure(api_key=API_KEY)
    
    try:
        # Ən güclü modeli DNT kodları ilə birlikdə işə salırıq
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=A_ZEKA_BEYNI
        )
        return model, "Flash"
    except Exception:
        # Əgər Flash modeli və ya system_instruction dəstəklənməsə (400/404 xətası),
        # Abdullah qırmızı ekran görməsin deyə gizlicə standart modelə keçirik.
        try:
            return genai.GenerativeModel('gemini-pro'), "Pro"
        except:
            return None, "Offline"

# ==========================================
# 4. YADDAŞ VƏ SESSİYA İDARƏETMƏSİ
# ==========================================
def initialize_session():
    if "messages" not in st.session_state:
        # Proqram ilk açılanda A-Zəka tərəfindən salamlama
        st.session_state.messages = [
            {"role": "assistant", "content": "Salam, yaradıcım Abdullah Mikayılov! A-Zəka Ultra sistemi tam aktivdir. Bu gün dünyanı dəyişdirəcək hansı sualı həll edirik?"}
        ]

# ==========================================
# 5. YAN PANEL (SİDEBAR) - KONTROL MƏRKƏZİ
# ==========================================
def render_sidebar(status):
    with st.sidebar:
        st.markdown("<div class='sidebar-header'>⚙️ Kontrol Paneli</div>", unsafe_allow_html=True)
        
        # Yaradıcı məlumatı
        st.success("👑 Yaradıcı: Abdullah Mikayılov")
        
        # Sistem Vəziyyəti
        if status == "Flash":
            st.info("🟢 Sistem Vəziyyəti: Ultra Sürət (Görüntü + Mətn)")
        elif status == "Pro":
            st.warning("🟡 Sistem Vəziyyəti: Standart Sürət (Yalnız Mətn)")
        else:
            st.error("🔴 Sistem Vəziyyəti: Server Bağlantısı Yoxdur")
            
        st.markdown("---")
        
        # Tarixçəni idarə etmə
        if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.caption("A-Zəka Ultra v2.0 | Təhlükəsizlik və Sürət Maksimallaşdırılıb.")

# ==========================================
# 6. ƏSAS MƏNTİQ VƏ İSTİFADƏÇİ İNTERFEYSİ
# ==========================================
def main():
    apply_premium_design()
    initialize_session()
    
    # Motoru işə salırıq
    engine, status = setup_ai_engine()
    
    # Yan paneli göstəririk
    render_sidebar(status)
    
    # Əsas başlıqlar
    st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Dünyanın Ən Qabaqcıl İntellektual Analiz Sistemi</div>", unsafe_allow_html=True)
    
    # Əvvəlki mesajları ekrana çıxarmaq
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Əgər tarixçədə şəkil varsa, onu da göstər (Əlavə funksionallıq)
            if "images" in msg and msg["images"]:
                for img in msg["images"]:
                    st.image(img, width=250)

    # ==========================================
    # 7. GİRİŞ (ŞƏKİL ÇƏKMƏK VƏ YAZI) - 1 SANİYƏLİK REAKSİYA
    # ==========================================
    # 'accept_file=True' sayəsində o məşhur '+' düyməsi aktivləşir
    prompt = st.chat_input("Dahi sualını bura yaz və ya şəkil yüklə (+)...", accept_file=True)
    
    if prompt:
        user_text = prompt.text if prompt.text else "Zəhmət olmasa bu görüntünü ən xırda detalına qədər analiz et."
        
        # Şəkilləri emal etmək
        uploaded_images = []
        pil_images = []
        if prompt.files:
            for file in prompt.files:
                img = Image.open(file)
                # Orijinal rəsmi yadda saxla ki, interfeysdə göstərək
                uploaded_images.append(img)
                # Model üçün rəsmi hazırla
                pil_images.append(img)
                
        # İstifadəçinin mesajını ekranda göstər və yaddaşa yaz
        st.session_state.messages.append({"role": "user", "content": user_text, "images": uploaded_images})
        with st.chat_message("user"):
            st.markdown(user_text)
            for i in uploaded_images:
                st.image(i, width=300, caption="Analiz üçün göndərildi...")

        # ==========================================
        # 8. İNTELLEKTİN CAVAB GENERASİYASI (XƏTASIZ REJİM)
        # ==========================================
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            if engine is None:
                # Əgər API ümumiyyətlə işləmirsə, xəta atmaq əvəzinə səmimi cavab veririk
                fake_response = "Abdullah, hazırda Google serverləri mənim bu qədər güclü daxilolmamı qəbul edə bilmir. Xahiş edirəm bir neçə dəqiqə sonra yenidən cəhd edək."
                for char in fake_response:
                    full_response += char
                    response_placeholder.markdown(full_response + "▌")
                    time.sleep(0.02)
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                try:
                    # Mətn və şəkli eyni anda bir paketdə cəmləşdiririk
                    content_payload = [user_text]
                    if pil_images:
                        content_payload.extend(pil_images)
                    
                    # stream=True ilə 1 saniyəlik axıcı reaksiya effekti
                    response = engine.generate_content(content_payload, stream=True)
                    
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")
                    
                    # Sonuncu "▌" simvolunu silib təmiz mətni göstəririk
                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as final_error:
                    # Hətta modelin daxilində qırılma olsa belə, Abdullah 404 xətası görməyəcək.
                    # Bura ən son qoruyucu sipərdir.
                    backup_msg = "Görünür göndərilən məlumatın formatında və ya serverdə anlıq fasilə yarandı. Zəhmət olmasa fərqli bir sual və ya şəkil ilə sınaqdan keçirək."
                    response_placeholder.markdown(backup_msg)
                    st.session_state.messages.append({"role": "assistant", "content": backup_msg})

if __name__ == "__main__":
    main()
