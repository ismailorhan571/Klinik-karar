import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek", layout="wide")

# 2. API Anahtarı (Koda gömülü - Google bunu engellemez, sadece güvenlik uyarısı verir)
# Görseldeki anahtarı eksiksiz kullanıyoruz
API_KEY_GOMULU = "AIzaSyD2DTlEW1mcv07-C3P1LsMHsCkV_XevkBo"

try:
    genai.configure(api_key=API_KEY_GOMULU)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Kurulamadı: {e}")

# 3. Görsel Tasarım
st.markdown("""
    <style>
    .stButton>button { background-color: #0d6efd; color: white; font-weight: bold; border-radius: 10px; width: 100%; }
    .ai-sonuc { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #0d6efd; color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚕️ Profesyonel Klinik Karar Destek")
st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 4.0")

# 4. Giriş Alanları
with st.sidebar:
    st.header("Hasta Bilgileri")
    yas = st.number_input("Yaş", 0, 120, 45)
    ates = st.slider("Ateş", 35.0, 42.0, 36.6)
    ta = st.text_input("Tansiyon (Örn: 120/80)", "120/80")

# 5. Semptomlar
st.subheader("🔍 Klinik Semptom Seçimi")
semptomlar = st.multiselect("Belirtileri İşaretleyin:", 
    ["Kelebek Döküntü", "Sabah Sertliği", "Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez", "Göğüs Ağrısı", "Nefes Darlığı", "Yüksek Ateş"])

# 6. Analiz Motoru
def klinik_analiz(liste):
    tanilar = []
    tetkikler = []
    s_set = set(liste)
    
    if "Kelebek Döküntü" in s_set: #
        tanilar.append("Sistemik Lupus Eritematozus (SLE)")
        tetkikler.extend(["ANA Paneli", "Anti-dsDNA", "Sedimantasyon"])
    
    if "Karın Ağrısı (Sağ Alt)" in s_set:
        tanilar.append("Akut Apandisit")
        tetkikler.extend(["Batın BT", "Tam Kan Sayımı (WBC Yüksekliği)"])

    if "Melena" in s_set or "Hematemez" in s_set:
        tanilar.append("GİS Kanama")
        tetkikler.extend(["Üst GİS Endoskopisi", "Hemoglobin Takibi"])

    return tanilar, tetkikler

# 7. Sonuç Ekranı
if st.button("ANALİZİ BAŞLAT"):
    if not semptomlar:
        st.warning("Lütfen en az bir semptom seçin.")
    else:
        on_tanilar, onerilen_tetkikler = klinik_analiz(semptomlar)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📋 Diferansiyel Tanı")
            for t in (on_tanilar if on_tanilar else ["Dahili Değerlendirme Gerekli"]):
                st.write(f"✅ {t}")
            
            st.write("---")
            st.subheader("🧪 Önerilen Tetkikler")
            # Değişken adı çakışması önlendi
            gosterilecek_tetkikler = set(onerilen_tetkikler if onerilen_tetkikler else ["Hemogram", "CRP", "Biyokimya"])
            for tet in gosterilecek_tetkikler:
                st.write(f"• {tet}")
        
        with col2:
            st.subheader("🤖 Gemini AI Analizi")
            try:
                p = f"Doktor asistanı ol. Yaş:{yas}, Belirtiler:{', '.join(semptomlar)}. Olası tanılar ve yönetim planı nedir?"
                r = model.generate_content(p)
                st.markdown(f"<div class='ai-sonuc'>{r.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Hatası: {e}")
