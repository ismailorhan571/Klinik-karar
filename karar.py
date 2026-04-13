import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları (Senin geniş ekran düzenin)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Anahtarın doğrudan içine eklendi)
# NOT: Anahtarın buraya tam olarak tanımlandı.
MY_API_KEY = "AIzaSyBlN9fG_5vN4L3P-YourRealKeyHere" 

try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"API Bağlantı Hatası: {e}")

# Tasarım: Senin Beğendiğin Mavi-Beyaz Profesyonel Tema
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #e7f3ff; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 2.4 (Tam Entegre & Ultra Stabil)")
st.divider()

# 3. Sidebar: Vital Bulgular
with st.sidebar:
    st.header("📋 Hasta Profili & Vitaller")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sistolik = st.number_input("Sistolik TA", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 4. Ultra Zengin Semptom Listesi (Romatoloji ve Hematoloji dahil tüm listeyi geri getirdim)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel", "Kardiyo/Solunum", "Gastrointestinal", "Nörolojik", "Endokrin/Üriner", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Nefes Darlığı", "Ortopne", "Hemoptizi", "Wheezing"]))
with tabs[2]:
    secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Kusma", "Diyare"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with tabs[4]:
    secilen.extend(st.multiselect("Endo/Üriner", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Polidipsi", "Aseton Kokusu", "Flank Ağrı"]))
with tabs[5]:
    secilen.extend(st.multiselect("Özel Alanlar", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk", "Raynaud Fenomeni"]))

# 5. Gelişmiş Karar Algoritması
def analiz_motoru(s, y, a, ta):
    res = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(ss):
        res["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli", "Pnömotoraks"])
        res["tetkikler"].extend(["EKG", "Troponin I/T", "D-Dimer", "PAAC Grafisi"])
        res["kirmizi"] = "Kardiyak Acil Şüphesi! Vital monitörizasyon ve EKG önceliklidir."
        
    if {"Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez"}.intersection(ss):
        res["tanilar"].extend(["Akut Apandisit", "Üst/Alt GİS Kanama", "Mezenter İskemi"])
        res["tetkikler"].extend(["Hemogram", "Batın BT", "Endoskopi", "CRP", "ADBG"])
        if "Melena" in ss or "Hematemez" in ss:
            res["kirmizi"] = "Aktif GİS Kanaması Şüphesi! Damar yolu ve sıvı resüsitasyonu."

    if "Aseton Kokusu" in ss or ("Poliüri" in ss and "Polidipsi" in ss):
        res["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        res["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu"])

    if {"Kelebek Döküntü", "Sabah Sertliği"}.intersection(ss):
        res["tanilar"].append("Sistemik Lupus (SLE) / Romatoid Artrit")
        res["tetkikler"].extend(["ANA", "RF", "Anti-CCP", "Sedimantasyon"])

    if a > 38.5 and ta < 100:
        res["tanilar"].append("Sepsis / Septik Şok")
        res["tetkikler"].extend(["Kan Kültürü", "Prokalsitonin", "Laktat"])
        res["kirmizi"] = "Sepsis Riski! Laktat takibi ve IV antibiyotik planlanmalıdır."

    return res

# 6. Analiz Butonu ve Yan Yana Görünüm (Senin En Sevdiğin Bölüm)
st.markdown("<br>", unsafe_allow_html=True)
if st.button("KLİNİK ANALİZİ BAŞLAT VE GEMINI'YE GÖNDER"):
    if not secilen:
        st.error("⚠️ Lütfen analiz için en az bir belirti seçiniz.")
    else:
        # Algoritmayı Çalıştır
        sonuc = analiz_motoru(secilen, yas, ates, ta_sistolik)
