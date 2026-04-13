import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa ve API Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (404 hatasını çözen garantili model ismi)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Hata Çözümü: 'models/gemini-1.5-flash' ismi en stabil olandır
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Streamlit Secrets kısmına GEMINI_API_KEY ekleyin.")

# Tasarım: Senin Orijinal Tıbbi Teman
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
st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.8 (Stabil & Zengin)")
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

# 4. Semptom Kategorileri (Senin listen + Yeni zenginlikler)
st.subheader("🔍 Klinik Semptom Seçimi")
t1, t2, t3, t4, t5, t6 = st.tabs(["Genel", "Kardiyovasküler", "Solunum", "Gastrointestinal", "Nörolojik", "Üriner/Endo"])

secilen = []

with t1:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"]))
with t2:
    secilen.extend(st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Ödem", "Ortopne", "PND"]))
with t3:
    secilen.extend(st.multiselect("Solunum", ["Nefes Darlığı", "Öksürük", "Hemoptizi", "Wheezing", "Plöretik Ağrı", "Siyanoz"]))
with t4:
    secilen.extend(st.multiselect("Gastrointestinal", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Bulantı/Kusma", "Diyare", "Sarılık"]))
with t5:
    secilen.extend(st.multiselect("Nörolojik", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with t6:
    secilen.extend(st.multiselect("Üriner/Endokrin", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Flank Ağrı", "Polidipsi", "Aseton Kokusu"]))

secilen_belirtiler = list(set(secilen))

# 5. Tanı Algoritması
def analiz_et(belirtiler, yas, ates, ta_sistolik, spo2):
    r = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    b_seti = set(belirtiler)

    # Kardiyak & Torasik Aciller
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(b_seti):
        r["tanilar"].extend(["Akut Miyokard Enfarktüsü", "Pulmoner Emboli"])
        r["tetkikler"].extend(["EKG", "Troponin", "D-Dimer", "PAAC Grafisi"])
        r["kirmizi"] = "Kardiyak Acil Şüphesi! Vital monitörizasyon gereklidir."

    # Gastrointestinal & Cerrahi Aciller
    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(b_seti):
        r["tanilar"].extend(["Akut Apandisit", "Üst GİS Kanaması"])
        r["tetkikler"].extend(["Hemogram", "Batın BT", "ADBG", "CRP"])
        if "Melena" in b_seti: r["kirmizi"] = "Aktif GİS Kanaması Şüphesi! Damar yolu açılmalıdır."

    # Endokrin (Yeni)
    if "Aseton Kokusu" in b_seti or ("Poliüri" in b_seti and "Polidipsi" in b_seti):
        r["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        r["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu"])

    # Sepsis Taraması
    if ates > 38.3 and ta_sistolik < 100:
        r["tanilar"].append("Sepsis Şüphesi")
        r["kirmizi"] = "Sepsis Riski! Laktat ve Kan Kültürü planlanmalıdır."

    return r

# 6. Sonuç Ekranı ve Gemini Entegrasyonu
if st.button("ANALİZİ BAŞLAT"):
    if not secilen_belirtiler:
        st.error("⚠️ Lütfen en az bir belirti seçiniz.")
    else:
        with st.spinner("Veriler sentezleniyor..."):
            sonuc = analiz_et(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            time.sleep(0.5)
            
            if sonuc["kirmizi"]:
                st.markdown(f"<div class='alert-box critical'>🚨 {sonuc['kirmizi']}</div>", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("📋 Diferansiyel Tanı Paneli")
                st.write("**Olası Teşhisler:**")
                tanilar = sonuc["tanilar"] if sonuc["tanilar"] else ["Genel Dahili Değerlendirme"]
                for t in set(tanilar): st.write(f"- {t}")
                
                st.write("**İstenmesi Gereken Tetkikler:**")
                tetkikler = sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "CRP", "Biyokimya Paneli"]
                for tetkik in set(tetkikler): st.write
