import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları (Senin orijinal görsel düzenin)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Doğrudan Tanımlama)
# Sırlar kısmı çalışmadığı için anahtarı buraya elle giriyoruz.
MY_API_KEY = "API_ANAHTARINI_BURAYA_YAZ" 

if MY_API_KEY != "AIzaSyD2DTlEW1mcvO7-C3P1LsMHsCkV_XevkBo":
    genai.configure(api_key=MY_API_KEY)
    # 404 hatasını önlemek için stabil model ismi
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("⚠️ Lütfen kodun içindeki 'MY_API_KEY' kısmına geçerli API anahtarınızı yazın.")

# CSS: Senin profesyonel tıbbi teman
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 10px; font-weight: bold; height: 3.5em; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #e7f3ff; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.title("⚕️ Gelişmiş Dahiliye CDSS (Ultra Zengin Sürüm)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 2.1 (API Entegre & Stabil)")

# 3. Sidebar: Vital Bulgular
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

# 4. Maksimum Zenginleştirilmiş Semptom Listesi
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel/Sistemik", "Kardiyo/Solunum", "Gastrointestinal", "Nöroloji", "Endokrin/Üriner", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]:
    secilen.extend(st.multiselect("Sistemik Belirtiler", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme", "Anoreksiya"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik Belirtiler", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Nefes Darlığı", "Ortopne", "PND", "Hemoptizi", "Wheezing"]))
with tabs[2]:
    secilen.extend(st.multiselect("Gastrointestinal", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Diyare", "Kusma", "Karında Şişkinlik"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nörolojik", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği", "Ataksi"]))
with tabs[4]:
    secilen.extend(st.multiselect("Endokrin & Üriner", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Polidipsi", "Aseton Kokusu", "Flank Ağrı", "Amenore"]))
with tabs[5]:
    secilen.extend(st.multiselect("Romatoloji & Hematoloji", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk", "Raynaud Fenomeni"]))

secilen_belirtiler = list(set(secilen))

# 5. Gelişmiş Karar Algoritması (Daha Fazla Klinik Korelasyon)
def klinik_analiz(s, y, a, ta, sp):
    r = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    
    # Kardiyovasküler & Pulmoner
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı", "Çarpıntı"}.intersection(ss):
        r["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli", "Aort Diseksiyonu"])
        r["tetkikler"].extend(["EKG", "Troponin I/T", "D-Dimer", "PAAC Grafisi", "Ekokardiyografi"])
        if ta > 180: r["kirmizi"] = "Hipertansif Acil Durum! Kan basıncı kontrolü gerekli."
        
    # Gastrointestinal Aciller
    if {"Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez"}.intersection(ss):
        r["tanilar"].extend(["Akut Apandisit", "Üst/Alt GİS Kanama", "Perforasyon"])
        r["tetkikler"].extend(["Hemogram", "Batın BT", "Endoskopi/Kolonoskopi", "INR/PTT", "ADBG"])
        if "Melena" in ss or "Hematemez" in ss: r["kirmizi"] = "Aktif GİS Kanaması Şüphesi! Sıvı resüsitasyonu ve acil konsültasyon."

    # Endokrin & Metabolik
    if {"Aseton Kokusu", "Poliüri", "Polidipsi"}.intersection(ss):
        r["tanilar"].append("Diyabetik Ketoasidoz (DKA) / HHS")
        r["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı (pH/HCO3)", "İdrar Ketonu", "HbA1c"])

    # Romatolojik / Hematolojik
    if {"Kelebek Döküntü", "Sabah Sertliği", "Peteşi/Purpura"}.intersection(ss):
        r["tanilar"].extend(["Sistemik Lupus (SLE)", "Vaskülit", "İmmün Trombositopeni (İTP)"])
        r["tet
