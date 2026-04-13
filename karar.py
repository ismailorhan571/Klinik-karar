import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Bağlantı Sorununu Çözen Ayar)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 404 hatasını önlemek için tam model yolu kullanıldı
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Lütfen Streamlit Secrets kısmına ekleyin.")

# CSS: Senin Orijinal Tıbbi Teman
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 10px; font-weight: bold; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #e7f3ff; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.title("⚕️ Gelişmiş Dahiliye CDSS (Full Sürüm)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 2.0 (Maksimum Zenginlik)")

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

# 4. Maksimum Zenginleştirilmiş Semptomlar (Hepsini Geri Getirdim)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel", "Kardiyo/Solunum", "Gastrointestinal", "Nöroloji", "Endokrin/Üriner", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Nefes Darlığı", "Ortopne", "Hemoptizi"]))
with tabs[2]:
    secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Diyare", "Kusma"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with tabs[4]:
    secilen.extend(st.multiselect("Endo/Üriner", ["Dizüri", "Hematüri", "Poliüri", "Polidipsi", "Aseton Kokusu", "Flank Ağrı"]))
with tabs[5]:
    secilen.extend(st.multiselect("Özel Alanlar", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk"]))

# 5. Dev Karar Algoritması
def analiz_motoru(s, y, a, ta):
    r = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(ss):
        r["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli"])
        r["tetkikler"].extend(["EKG", "Troponin", "D-Dimer", "PAAC Grafisi"])
        r["kirmizi"] = "Kardiyak Acil Şüphesi! Monitorizasyon önceliklidir."
        
    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(ss):
        r["tanilar"].extend(["Akut Apandisit", "Üst GİS Kanama"])
        r["tetkikler"].extend(["Hemogram", "Batın BT", "Endoskopi", "CRP", "INR/PTT", "ADBG"])
        if "Melena" in ss: r["kirmizi"] = "Aktif GİS Kanaması! Acil konsültasyon ve sıvı başlanmalı."

    if {"Poliüri", "Aseton Kokusu"}.intersection(ss):
        r["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        r["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu"])

    if {"Kelebek Döküntü", "Sabah Sertliği"}.intersection(ss):
        r["tanilar"].append("Sistemik Lupus (SLE) / Romatoid Artrit")
        r["tetkikler"].extend(["ANA", "Anti-dsDNA", "RF", "Sedimantasyon"])

    if a > 38.5 and ta < 100:
        r["tanilar"].append("Sepsis Şüphesi")
        r["tetkikler"].extend(["Kan Kültürü", "Prokalsitonin", "Laktat"])

    return r

# 6. Sunum ve Gemini Entegrasyonu
if st.button("ANALİZİ BAŞLAT"):
    if not secilen:
        st.error("⚠️ Lütfen belirti seçiniz.")
    else:
        sonuc = analiz_motoru(secilen, yas, ates, ta_sistolik)
        
        if sonuc["kirmizi"]:
            st.markdown(f"<div class='alert-box critical'>🚨 {sonuc['kirmizi']}</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📋 Diferansiyel Tanı ve Tetkikler")
            st.write("**Olası Teşhisler:**")
            for t in set(sonuc["tanilar"] if sonuc["tanilar"] else ["Diferansiyel değerlendirme önerilir."]):
                st.write(f"- {t}")
            
            st.write("**İstenmesi Gereken Tetkikler:**")
            # HATA ÇÖZÜMÜ: tetkikler değişkeni burada garantiye alındı
            tetkik_listesi = set(sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "CRP", "Biyokimya"])
            for tetkik in tetkik_listesi:
                st.write(f"- {tetkik}")
        
        with c2:
            st.subheader("🤖 Gemini AI İleri Analiz")
            try:
                v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                prompt = f"Uzman CDSS: {yas}y, {cinsiyet}. Vitaller: {v_str}. Belirtiler: {', '.join(secilen)}. Literatür bazlı ayırıcı tanı ve tedavi stratejisi öner."
                
                response = model.generate_content(prompt)
                st.markdown(f"<div class='alert-box info-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Gemini Analiz Hatası: {e}")

st.markdown("<br><p style='text-align: center; color: gray; font-size: 11px;'>© 2026 Dahiliye Karar Destek v2.0</p>", unsafe_allow_html=True)
