import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları (Senin orijinal ayarların)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# Gemini API Yapılandırması (404 hatasını çözen en güncel yapı)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # NOT: 'models/' ön eki v1beta hatalarını önlemek için zorunludur.
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Streamlit Secrets kısmına GEMINI_API_KEY ekleyin.")

# CSS: Senin profesyonel tıbbi teman
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; color: #212529; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; font-weight: bold; height: 3em; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.7 (Entegre & Stabil)")
st.divider()

# 3. Sol Menü: Vital Bulgular
with st.sidebar:
    st.header("📋 Hasta Profili")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    
    st.header("🫀 Vital Bulgular")
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sistolik = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    nabiz = st.number_input("Nabız (/dk)", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 4. Ana Ekran: Semptom Kategorileri (Orijinal yapın aynen korundu)
st.subheader("🔍 Klinik Semptom Seçimi")
t1, t2, t3, t4, t5, t6 = st.tabs(["Genel", "Kardiyovasküler", "Solunum", "Gastrointestinal", "Nörolojik", "Üriner/Diğer"])

secilen_belirtiler = []

with t1:
    g1 = st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"])
    secilen_belirtiler.extend(g1)
with t2:
    g2 = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Ödem", "Ortopne"])
    secilen_belirtiler.extend(g2)
with t3:
    g3 = st.multiselect("Solunum", ["Nefes Darlığı", "Öksürük", "Hemoptizi", "Wheezing", "Plöretik Ağrı", "Siyanoz"])
    secilen_belirtiler.extend(g3)
with t4:
    g4 = st.multiselect("Gastrointestinal", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Bulantı/Kusma", "Diyare"])
    secilen_belirtiler.extend(g4)
with t5:
    g5 = st.multiselect("Nörolojik", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"])
    secilen_belirtiler.extend(g5)
with t6:
    g6 = st.multiselect("Üriner/Endokrin", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Flank Ağrı", "Polidipsi", "Aseton Kokusu"])
    secilen_belirtiler.extend(g6)

# 5. Senin Orijinal Karar Algoritman (Zenginleştirilmiş Hali)
def analiz_et(belirtiler, yas, ates, ta_sistolik, spo2):
    r = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    b_seti = set(belirtiler)

    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(b_seti):
        r["tanilar"].extend(["Akut Miyokard Enfarktüsü", "Pulmoner Emboli"])
        r["tetkikler"].extend(["EKG", "Troponin", "D-Dimer", "PAAC Grafisi"])
        r["kirmizi"] = "Kardiyak Acil Şüphesi! Vital monitörizasyon ve EKG önceliklidir."

    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(b_seti):
        r["tanilar"].extend(["Akut Apandisit", "Üst GİS Kanaması"])
        r["tetkikler"].extend(["Hemogram", "Batın BT", "Tüm Batın USG", "ADBG", "CRP"])
        if "Melena" in b_seti: r["kirmizi"] = "GİS Kanama Şüphesi! Damar yolu ve sıvı resüsitasyonu."

    if "Aseton Kokusu" in b_seti or ("Poliüri" in b_seti and "Polidipsi" in b_seti):
        r["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        r["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu"])

    if ates > 38.5 and ta_sistolik < 100:
        r["tanilar"].append("Sepsis / Septik Şok")
        r["tetkikler"].extend(["Kan Kültürü", "Prokalsitonin", "Laktat"])

    # Listeleri temizle ve boş kalmamasını sağla
    r["tanilar"] = list(set(r["tanilar"])) if r["tanilar"] else ["Diferansiyel değerlendirme gereklidir."]
    r["tetkikler"] = list(set(r["tetkikler"])) if r["tetkikler"] else ["Hemogram", "Biyokimya Paneli"]
    return r

# 6. Sonuç Ekranı ve Gemini Entegrasyonu
if st.button("ANALİZİ BAŞLAT"):
    if not secilen_belirtiler:
        st.error("⚠️ Lütfen belirti seçiniz.")
    else:
        with st.spinner("Klinik veri ve AI sentezleniyor..."):
            sonuc = analiz_et(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            
            if sonuc["kirmizi"]:
                st.markdown(f"<div class='alert-box critical'>"
