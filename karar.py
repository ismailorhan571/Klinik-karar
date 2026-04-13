import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Bağlantı sorunu için en güvenli yol)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # NOT: 'gemini-1.5-flash-latest' bazen daha hızlı yanıt verir.
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Lütfen Secrets ayarlarına ekleyin.")

# CSS: Tıbbi Arayüz (Senin stilin)
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; color: #212529; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 10px; font-weight: bold; height: 3.5em; }
    .critical-card { background-color: #f8d7da; color: #842029; padding: 15px; border-radius: 10px; border: 1px solid #f5c2c7; margin-bottom: 15px; }
    .info-card { background-color: #e7f3ff; color: #0c5460; padding: 15px; border-radius: 10px; border: 1px solid #bee5eb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.title("⚕️ Gelişmiş Dahiliye CDSS (v1.5)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Bağlantı Durumu:** Stabil")
st.divider()

# 3. Sidebar (Vitals & Profile)
with st.sidebar:
    st.header("📋 Hasta Bilgileri")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Diğer"])
    
    st.header("🫀 Vital Bulgular")
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sistolik = st.number_input("Sistolik TA", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 4. Semptomlar (Maksimum Zenginlik)
st.subheader("🔍 Klinik Semptom Seçimi")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["Genel", "Kardiyo/Solunum", "Gastro", "Nöro", "Üriner/Endo", "Romatoloji", "Hematoloji/Onko"])

secilen = []

with t1:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"]))
with t2:
    secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Dispne", "Ortopne", "Öksürük", "Hemoptizi"]))
with t3:
    secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Sağ Alt)", "Karın Ağrısı (Sol Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Diyare", "Kabızlık"]))
with t4:
    secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği", "Görüş Kaybı"]))
with t5:
    secilen.extend(st.multiselect("Üriner/Endo", ["Dizüri", "Hematüri", "Poliüri", "Oligüri", "Polidipsi", "Aseton Kokusu", "Flank Ağrı"]))
with t6:
    secilen.extend(st.multiselect("Romatoloji", ["Sabah Sertliği (>30 dk)", "Eklem Şişliği", "Raynaud Fenomeni", "Kelebek Döküntü", "Ağız Kuruluğu"]))
with t7:
    secilen.extend(st.multiselect("Hematoloji/Onkoloji", ["Peteşi/Purpura", "Diş Eti Kanaması", "Splenomegali", "Solukluk (Anemi Bulgusu)", "Kemik Ağrısı"]))

# 5. Dev Algoritma (Her Şey Dahil)
def klinik_karar_motoru(s, y, a, ta, sp):
    r = {"tanilar": [], "tetkikler": [], "acil": ""}
    ss = set(s)

    # Kardiyak/Pulmoner Acil
    if {"Göğüs Ağrısı (Baskı)", "Dispne"}.intersection(ss):
        r["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli"])
        r["tetkikler"].extend(["Troponin", "D-Dimer", "EKG", "PAAC Grafisi", "Arter Kan Gazı"])
        r["acil"] = "🚨 KARDİYAK ACİL! EKG ve Monitorizasyon önceliklidir."

    # Akut Batın
    if {"Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez"}.intersection(ss):
        r["tanilar"].extend(["Akut Apandisit", "Üst/Alt GİS Kanama"])
        r["tetkikler"].extend(["Hemogram", "Batın BT", "Endoskopi", "ADBG", "CRP"])
        if "Melena" in ss: r["acil"] = "🚨 AKTİF KANAMA! Sıvı resüsitasyonu ve konsültasyon."

    # Romatoloji/Otoimmün (Yeni)
    if {"Kelebek Döküntü", "Sabah Sertliği (>30 dk)"}.intersection(ss):
        r["tanilar"].append("Sistemik Lupus Eritematozus (SLE) / Romatoid Artrit")
        r["tetkikler"].extend(["ANA", "Anti-dsDNA", "RF", "Sedimantasyon"])

    # Hematoloji (Yeni)
    if {"Peteşi/Purpura", "Splenomegali"}.intersection(ss):
        r["tanilar"].append("İmmün Trombositopeni (İTP) / Lösemi Şüphesi")
        r["tetkikler"].extend(["Periferik Yayma", "LDH", "Geniş Hemogram"])

    # Sepsis Taraması
    if (a > 38.5 or a < 36.0) and ta < 100:
        r["tanilar"].append("Sepsis / Septik Şok")
        r["tetkikler"].extend(["Kan Kültürü", "Prokalsitonin", "Laktat"])
        r["acil"] = "🚨 SEPSİS ŞÜPHESİ! IV Antibiyotik ve Sıvı başlanmalı."

    return r

# 6. Analiz ve Sunum
if st.button("KLİNİK ANALİZİ BAŞLAT"):
    if not secilen:
        st.error("⚠️ Lütfen belirti seçin.")
    else:
        with st.spinner("AI ve Algoritmalar Sentezleniyor..."):
            sonuc = klinik_karar_motoru(secilen, yas, ates, ta_sistolik, spo2)
            
            if sonuc["acil"]:
                st.markdown(f"<div class='critical-card'>{sonuc['acil']}</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### 📋 Algoritmik Teşhis Paneli")
                st.write("**Olası Tanılar:**")
                for t in list(set(sonuc["tanilar"] if sonuc["tanilar"] else ["Genel Değerlendirme"])):
                    st.write(f"• {t}")
                st.write("**İstenmesi Gereken Tetkikler:**")
                for tetkik in list(set(sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "CRP"])):
                    st.write(f"• {tetkik}")
            
            with c2:
                st.markdown("### 🤖 Gemini AI Derin Analiz")
                v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                try:
                    # Promptu daha profesyonel hale getirdim
                    prompt = f"Sen uzman doktora destek olan bir CDSS'sin. Hasta: {yas}y, {cinsiyet}. Semptomlar: {', '.join(secilen)}. Vitaller: {v_str}. Literatür eşliğinde ayırıcı tanı ve tedavi stratejisi öner."
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='info-card'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI Yanıt Vermedi: {e}")

st.markdown("<br><p style='text-align: center; color: gray;'>© 2026 Dahiliye Karar Destek v1.5</p>", unsafe_allow_html=True)
