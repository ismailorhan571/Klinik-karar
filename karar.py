import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları (Profesyonel Tıbbi Tema)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# --- GEMINI API YAPILANDIRMASI ---
# Streamlit Secrets üzerinden API anahtarını kontrol eder
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ Gemini API anahtarı bulunamadı. Lütfen Streamlit Secrets ayarlarına GEMINI_API_KEY ekleyin.")

# CSS: Arayüz Tasarımı
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; color: #212529; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; border: none; height: 3em; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #0b5ed7; }
    h1, h2, h3 { color: #0d6efd; border-bottom: 2px solid #dee2e6; padding-bottom: 10px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; font-size: 15px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi Alanı
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("<h1 style='text-align: center; font-size: 50px; border: none;'>⚕️</h1>", unsafe_allow_html=True)
with col2:
    st.title("Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
    st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 1.1 (Gemini AI Entegre)")

st.divider()

# 3. Sol Menü: Vital Bulgular ve Hasta Profili
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
    
    st.markdown("---")
    st.info("💡 **Not:** Bu sistem tanı koymaz, hekime diferansiyel tanı ve tetkik planlamasında kılavuzluk eder.")

# 4. Ana Ekran: Belirtiler
st.subheader("🔍 Klinik Semptom Seçimi")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Sistemik/Genel", "Kardiyovasküler", "Solunum", "Gastrointestinal", "Nörolojik", "Üriner/Renal"
])

secilen_belirtiler = []

with tab1:
    sistemik = st.multiselect("Sistemik Belirtiler", ["Yüksek Ateş", "Halsizlik/Yorgunluk", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Yaygın Kas Ağrısı", "Eklem Ağrısı", "Titreme", "İştahsızlık"])
    secilen_belirtiler.extend(sistemik)
with tab2:
    kardiyo = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı tarzı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Bilateral Alt Ekstremite Ödemi", "Eforla Gelen Nefes Darlığı", "Ortopne"])
    secilen_belirtiler.extend(kardiyo)
with tab3:
    solunum = st.multiselect("Solunum Sistemi", ["Nefes Darlığı (Dispne)", "Kuru Öksürük", "Balgamlı Öksürük", "Hemoptizi", "Hışıltılı Solunum", "Siyanoz"])
    secilen_belirtiler.extend(solunum)
with tab4:
    gastro = st.multiselect("Gastrointestinal", ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Sağ Alt)", "Bulantı", "Kusma", "Diyare", "Melena", "Hematemez", "Sarılık"])
    secilen_belirtiler.extend(gastro)
with tab5:
    noro = st.multiselect("Nörolojik", ["Baş Ağrısı", "Baş Dönmesi", "Bilinç Bulanıklığı", "Tek Taraflı Güç Kaybı", "Konuşma Bozukluğu", "Nö
