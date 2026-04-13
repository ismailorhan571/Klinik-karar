import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Garantili model ismi)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Secrets ayarlarına ekleyin.")

# CSS: Senin Orijinal Tıbbi Teman
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; font-weight: bold; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Gelişmiş Klinik Karar Destek Sistemi")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 1.9 (Hata Düzeltildi)")

# 3. Sidebar: Vitaller
with st.sidebar:
    st.header("📋 Hasta Profili")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sistolik = st.number_input("Sistolik TA", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 4. Semptomlar (Senin Listen)
st.subheader("🔍 Klinik Semptom Seçimi")
t1, t2, t3, t4, t5 = st.tabs(["Genel", "Kardiyo/Solunum", "Gastro", "Nöro", "Üriner/Endo"])

secilen = []
with t1: secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Kilo Kaybı", "Titreme"]))
with t2: secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Nefes Darlığı", "Çarpıntı", "Öksürük"]))
with t3: secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Kusma"]))
with t4: secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Baş Dönmesi", "Bilinç Bulanıklığı", "Güç Kaybı"]))
with t5: secilen.extend(st.multiselect("Üriner/Endo", ["Dizüri", "Hematüri", "Poliüri", "Aseton Kokusu"]))

# 5. Karar Motoru
def analiz_et(belirtiler, ates, ta):
    r = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    b = set(belirtiler)
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(b):
        r["tanilar"].extend(["Akut Miyokard Enfarktüsü", "Pulmoner Emboli"])
        r["tetkikler"].extend(["EKG", "Troponin", "D-Dimer"])
    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(b):
        r["tanilar"].extend(["Akut Apandisit", "Üst GİS Kanaması"])
        r["tetkikler"].extend(["Batın BT", "Hemogram", "CRP", "INR/PTT", "ADBG"])
    return r

# 6. Sonuç Ekranı (Hatanın düzeltildiği yer)
if st.button("ANALİZİ BAŞLAT"):
    if not secilen:
        st.error("Lütfen belirti seçin.")
    else:
        sonuc = analiz_et(secilen, ates, ta_sistolik)
        
        # Olası Tanılar
        st.subheader("📋 Diferansiyel Tanı ve Tetkikler")
        for t in set(sonuc["tanilar"] if sonuc["tanilar"] else ["Genel Değerlendirme"]):
            st.write(f"- {t}")
            
        # Tetkik Önerileri (HATA BURADAYDI, DÜZELTİLDİ)
        st.write("**İstenmesi Gereken Tetkikler:**")
        liste_tetkik = set(sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "Biyokimya"])
        for tetkik in liste_tetkik:
            st.write(f"- {tetkik}")

        # 7. Gemini AI İleri Analizi (Geri Geldi!)
        st.divider()
        st.subheader("🤖 Gemini AI Derin Analiz")
        try:
            v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
            prompt = f"Uzman CDSS: {yas}y hasta. Vitaller: {v_str}. Belirtiler: {', '.join(secilen)}. Ayırıcı tanı ve tetkik öner."
            response = model.generate_content(prompt)
            st.markdown(f"<div class='alert-box info-box'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"AI Analiz Hatası: {e}")

st.markdown("<br><p style='text-align: center; color: gray; font-size: 11px;'>© 2026 Dahiliye Karar Destek v1.9</p>", unsafe_allow_html=True)
