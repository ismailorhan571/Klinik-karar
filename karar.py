import streamlit as st
import google.generativeai as genai

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="Karar Destek Sistemi", layout="wide")

# 2. API ANAHTARI (Doğrudan Koda Gömüldü)
# NOT: Anahtarı kopyalarken başında/sonunda boşluk olmadığına emin ol!
MY_API_KEY = "AIzaSyD2DTlEW1mcv07-C3P1LsMHsCkV_XevkBo"

def setup_ai():
    try:
        genai.configure(api_key=MY_API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Kurulum Hatası: {e}")
        return None

model = setup_ai()

# 3. Görsel Tasarım
st.markdown("""
    <style>
    .stButton>button { background-color: #e63946; color: white; width: 100%; border-radius: 8px; font-weight: bold; }
    .ai-box { background-color: #f1faee; padding: 15px; border-radius: 10px; border-left: 5px solid #457b9d; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚕️ Dahiliye Klinik Karar Destek")
st.write(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 4.2")

# 4. Giriş Alanları
with st.sidebar:
    st.header("Hasta Verileri")
    yas = st.number_input("Yaş", 0, 110, 45)
    ates = st.slider("Ateş", 35.0, 41.0, 36.6)
    semptom_listesi = ["Kelebek Döküntü", "Melena", "Hematemez", "Karın Ağrısı (Sağ Alt)", "Göğüs Ağrısı"]
    secilenler = st.multiselect("Semptomlar", semptom_listesi)

# 5. Analiz Kısmı
if st.button("ANALİZİ BAŞLAT"):
    if not secilenler:
        st.warning("Lütfen belirti seçin.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Klinik Ön Tanılar")
            # Basit Algoritma
            if "Kelebek Döküntü" in secilenler:
                st.write("✅ **Sistemik Lupus (SLE)** - *Tetkik: ANA, Anti-dsDNA*")
            if "Melena" in secilenler or "Hematemez" in secilenler:
                st.write("✅ **GİS Kanama** - *Tetkik: Endoskopi, Hb takibi*")
            if "Karın Ağrısı (Sağ Alt)" in secilenler:
                st.write("✅ **Akut Apandisit** - *Tetkik: Batın BT, WBC*")
                
        with col2:
            st.subheader("🤖 Gemini AI Analizi")
            if model:
                try:
                    p = f"Doktor asistanı ol. Yaş:{yas}, Bulgular:{', '.join(secilenler)}. Analiz et."
                    res = model.generate_content(p)
                    st.markdown(f"<div class='ai-box'>{res.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    # Hata mesajını detaylı basıyoruz
                    st.error(f"API Hatası Oluştu: {e}")
            else:
                st.error("Model yüklenemedi, API anahtarını kontrol edin.")
