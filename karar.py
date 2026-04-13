import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları ve API Yapılandırması
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

def gemini_baslat():
    try:
        # Secrets'tan anahtarı alıyoruz
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            # 'models/' ön eki 404 hatalarını önlemek için en güvenli yoldur
            return genai.GenerativeModel('models/gemini-1.5-flash')
        else:
            st.warning("⚠️ API Anahtarı eksik! Streamlit Secrets ayarlarına GEMINI_API_KEY ekleyin.")
            return None
    except Exception as e:
        st.error(f"Bağlantı Hatası: {str(e)}")
        return None

model = gemini_baslat()

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
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("<h1 style='text-align: center; font-size: 50px; border: none;'>⚕️</h1>", unsafe_allow_html=True)
with col2:
    st.title("Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
    st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.6 (Maksimum Stabilite)")

st.divider()

# 3. Sidebar: Vitaller
with st.sidebar:
    st.header("📋 Hasta Profili")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    
    st.header("🫀 Vital Bulgular")
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sistolik = st.number_input("Sistolik TA", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 4. Semptom Seçimi (Daha da zenginleştirildi)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel", "Kardiyo/Solunum", "Gastro", "Nöro", "Üriner/Endo", "Romatoloji/Hematoloji"])

secilen_belirtiler = []

with tabs[0]:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Miyalji", "Titreme", "Lenfadenopati", "Kaşıntı"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Dispne", "Ortopne", "Kuru Öksürük", "Hemoptizi"]))
with tabs[2]:
    secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Bulantı", "Kusma", "Diyare", "Melena", "Hematemez", "Sarılık"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with tabs[4]:
    secilen.extend(st.multiselect("Üriner/Endo", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Flank Ağrı", "Polidipsi", "Aseton Kokusu"]))
with tabs[5]:
    secilen.extend(st.multiselect("Özel Alanlar", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk"]))

secilen_belirtiler = list(set(secilen))

# 5. Tanı Algoritması (Orijinal Mantığın + Zenginleştirme)
def gelismis_analiz(belirtiler, yas, ates, ta_sistolik, spo2):
    rapor = {"teshisler": [], "kan": [], "goruntuleme": [], "kirmizi": ""}
    b_seti = set(belirtiler)

    if {"Göğüs Ağrısı (Baskı)", "Dispne"}.intersection(b_seti):
        rapor["teshisler"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli"])
        rapor["kan"].extend(["Troponin", "D-Dimer", "CK-MB", "Arter Kan Gazı"])
        rapor["goruntuleme"].extend(["EKG (Acil)", "EKO", "PAAC Grafisi"])
        rapor["kirmizi"] = "Kardiyak Acil Şüphesi! İlk 10 dk içinde EKG çekilmelidir."

    if {"Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez"}.intersection(b_seti):
        rapor["teshisler"].extend(["Akut Apandisit", "GİS Kanama"])
        rapor["kan"].extend(["Hemogram", "CRP", "INR/PTT", "Laktat"])
        rapor["goruntuleme"].extend(["Batın BT", "Tüm Batın USG", "ADBG"])
        if "Melena" in b_seti: rapor["kirmizi"] = "Aktif GİS Kanaması Şüphesi! Acil konsültasyon."

    if {"Poliüri", "Aseton Kokusu", "Polidipsi"}.intersection(b_seti):
        rapor["teshisler"].append("Diyabetik Ketoasidoz (DKA)")
        rapor["kan"].extend(["Kan Şekeri", "VİS Elektrolitler", "Keton"])

    if ates > 38.5 and ta_sistolik < 100:
        rapor["teshisler"].append("Sepsis / Septik Şok?")
        rapor["kirmizi"] = "Sepsis Şüphesi! Laktat takibi ve IV antibiyotik planlanmalı."

    return rapor

# 6. Analiz Tetikleme
if st.button("TIBBİ ALGORİTMAYI ÇALIŞTIR VE AI ANALİZİ YAP"):
    if not secilen_belirtiler:
        st.error("⚠️ Lütfen en az bir belirti seçiniz.")
    else:
        with st.spinner("Analiz ediliyor..."):
            sonuc = gelismis_analiz(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            time.sleep(0.5)
            
            if sonuc["kirmizi"]:
                st.markdown(f"<div class='alert-box critical'>🚨 {sonuc['kirmizi']}</div>", unsafe_allow_html=True)
            
            col_l, col_r = st.columns(2)
            with col_l:
                st.subheader("📋 Algoritmik Teşhis Paneli")
                st.write("**Olası Tanılar:**")
                for t in list(set(sonuc["teshisler"] if sonuc["teshisler"] else ["Spesifik sendrom eşleşmedi."])): st.write(f"- {t}")
                st.write("**Önerilen Tetkikler:**")
                for tetkik in list(set(sonuc["kan"] + sonuc["goruntuleme"])): st.write(f"- {tetkik}")
                    
            with col_r:
                st.subheader("🤖 Gemini AI Derin Analiz")
                if model:
                    try:
                        v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                        istek = f"Sen uzman bir CDSS'sin. Hasta: {yas}y, {cinsiyet}. Vitaller: {v_str}. Belirtiler: {', '.join(secilen_belirtiler)}. Ayırıcı tanı ve tetkik öner."
                        response = model.generate_content(istek)
                        st.markdown(f"<div class='alert-box info-box'>{response.text}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"AI Analiz Hatası: {str(e)}")
                else:
                    st.info("AI bağlantısı hazır değil, lütfen Secrets ayarlarını kontrol et.")

st.markdown("<br><p style='text-align: center; color: gray; font-size: 11px;'>© 2026 Dahiliye Karar Destek v1.6</p>", unsafe_allow_html=True)
