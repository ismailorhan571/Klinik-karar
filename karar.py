import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları (Senin geniş ekran düzenin)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Anahtarın doğrudan içine eklendi)
MY_API_KEY = "AIzaSyBlN..." # Anahtarını buraya senin için tanımladım İsmail

genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

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
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 2.3 (Tam Entegre)")
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

# 4. Ultra Zengin Semptom Listesi (Geri Getirildi)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel", "Kardiyo/Solunum", "Gastro", "Nöro", "Endokrin/Üriner", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Nefes Darlığı", "Hemoptizi", "Wheezing"]))
with tabs[2]:
    secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Kusma", "Diyare"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with tabs[4]:
    secilen.extend(st.multiselect("Endo/Üriner", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Polidipsi", "Aseton Kokusu", "Flank Ağrı"]))
with tabs[5]:
    secilen.extend(st.multiselect("Özel Alanlar", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk"]))

# 5. Karar Algoritması
def analiz_motoru(s, y, a, ta):
    res = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(ss):
        res["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli"])
        res["tetkikler"].extend(["EKG", "Troponin", "D-Dimer"])
        res["kirmizi"] = "Kardiyak Acil Şüphesi! Monitörizasyon önerilir."
    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(ss):
        res["tanilar"].extend(["Akut Apandisit", "GİS Kanama"])
        res["tetkikler"].extend(["Batın BT", "Hemogram", "CRP", "ADBG"])
    if "Aseton Kokusu" in ss:
        res["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        res["tetkikler"].extend(["Kan Şekeri", "VİS Kan Gazı"])
    if a > 38.5 and ta < 100:
        res["tanilar"].append("Sepsis / Septik Şok")
        res["kirmizi"] = "Sepsis Riski! Laktat ve Kan Kültürü planlanmalıdır."
    return res

# 6. Analiz Butonu ve Yan Yana Görünüm (İsmail'in Favorisi)
if st.button("KLİNİK ANALİZİ BAŞLAT"):
    if not secilen:
        st.error("⚠️ Belirti seçmeden analiz yapılamaz.")
    else:
        sonuc = analiz_motoru(secilen, yas, ates, ta_sistolik)
        
        if sonuc["kirmizi"]:
            st.markdown(f"<div class='alert-box critical'>🚨 **KRİTİK:** {sonuc['kirmizi']}</div>", unsafe_allow_html=True)
            
        col_sol, col_sag = st.columns(2)
        
        with col_sol:
            st.subheader("📋 Diferansiyel Tanı ve Tetkikler")
            st.write("**Olası Ön Tanılar:**")
            for t in set(sonuc["tanilar"] if sonuc["tanilar"] else ["Dahilî Değerlendirme"]):
                st.write(
