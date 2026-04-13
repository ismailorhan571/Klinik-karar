import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ Gemini API anahtarı eksik! Streamlit Secrets ayarlarına GEMINI_API_KEY ekleyin.")

# Tasarım (CSS)
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; color: #212529; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; border: none; height: 3em; font-weight: bold; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("<h1 style='text-align: center; font-size: 50px; border: none;'>⚕️</h1>", unsafe_allow_html=True)
with col2:
    st.title("Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
    st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.1")

st.divider()

# 3. Sol Menü
with st.sidebar:
    st.header("📋 Hasta Profili")
    yas = st.number_input("Yaş", min_value=0, max_value=120, value=45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    
    st.header("🫀 Vital Bulgular")
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sistolik = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    nabiz = st.number_input("Nabız (/dk)", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 4. Semptomlar (Hatanın olduğu bölüm düzeltildi)
st.subheader("🔍 Klinik Semptom Seçimi")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Genel", "Kardiyo", "Solunum", "Gastro", "Nöro", "Üriner"])

secilen_belirtiler = []

with tab1:
    sistemik = st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Kilo Kaybı", "Titreme"])
    secilen_belirtiler.extend(sistemik)
with tab2:
    kardiyo = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı)", "Çarpıntı", "Ödem", "Nefes Darlığı"])
    secilen_belirtiler.extend(kardiyo)
with tab3:
    solunum = st.multiselect("Solunum", ["Öksürük", "Hemoptizi", "Hışıltılı Solunum"])
    secilen_belirtiler.extend(solunum)
with tab4:
    gastro = st.multiselect("Gastrointestinal", ["Karın Ağrısı", "Bulantı", "Kusma", "Melena"])
    secilen_belirtiler.extend(gastro)
with tab5:
    noro = st.multiselect("Nörolojik", ["Baş Ağrısı", "Baş Dönmesi", "Bilinç Bulanıklığı", "Güç Kaybı"])
    secilen_belirtiler.extend(noro)
with tab6:
    uriner = st.multiselect("Üriner", ["Dizüri", "Hematüri", "Yan Ağrısı"])
    secilen_belirtiler.extend(uriner)

st.divider()

# 5. Analiz Fonksiyonları
def ai_analiz(yas, cinsiyet, vitals, belirtiler):
    if "GEMINI_API_KEY" not in st.secrets: return "API Key Ayarlanmamış."
    prompt = f"Hasta: {yas}y, {cinsiyet}. Vitals: {vitals}. Semptomlar: {', '.join(belirtiler)}. Olası tanılar ve tetkikler nelerdir?"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Hata: {str(e)}"

# 6. Çalıştır
if st.button("ANALİZ ET"):
    if not secilen_belirtiler:
        st.error("Lütfen belirti seçin.")
    else:
        with st.spinner("İşleniyor..."):
            v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
            cevap = ai_analiz(yas, cinsiyet, v_str, secilen_belirtiler)
            
            c1, c2 = st.columns(2)
            with c1:
                st.info("📌 Seçilen Belirtiler: " + ", ".join(secilen_belirtiler))
            with c2:
                st.markdown(f"<div class='alert-box info-box'><b>🤖 AI Analizi:</b><br>{cevap}</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Dahiliye Karar Destek</p>", unsafe_allow_html=True)
