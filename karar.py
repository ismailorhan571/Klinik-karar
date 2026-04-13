import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# Gemini API Yapılandırması (404 Hatası Çözüldü)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Hata çözümü: 'models/' ön eki eklendi
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Streamlit Secrets kısmına GEMINI_API_KEY ekleyin.")

# CSS: Tıbbi Tema
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; color: #212529; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; border: none; height: 3em; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #0b5ed7; }
    h1, h2, h3 { color: #0d6efd; border-bottom: 2px solid #dee2e6; padding-bottom: 10px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
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
    st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.3 (Stabil & Genişletilmiş)")

st.divider()

# 3. Sol Menü
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
    st.info("💡 **Not:** Bu sistem tanı koymaz, hekime rehberlik eder.")

# 4. Semptom Seçimi (Ekstra belirtiler eklendi)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Sistemik", "Kardiyo", "Solunum", "Gastro", "Nöro", "Üriner/Endokrin"])

secilen_belirtiler = []

with tabs[0]:
    sistemik = st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik/Yorgunluk", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Miyalji", "Atralji", "Titreme", "İştahsızlık", "Lenfadenopati"])
    secilen_belirtiler.extend(sistemik)
with tabs[1]:
    kardiyo = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Ödem", "Efor Dispnesi", "Ortopne", "Juguler Venöz Dolgunluk"])
    secilen_belirtiler.extend(kardiyo)
with tabs[2]:
    solunum = st.multiselect("Solunum", ["Nefes Darlığı", "Kuru Öksürük", "Balgamlı Öksürük", "Hemoptizi", "Wheezing", "Plöretik Ağrı", "Siyanoz"])
    secilen_belirtiler.extend(solunum)
with tabs[3]:
    gastro = st.multiselect("Gastrointestinal", ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Bulantı", "Kusma", "Diyare", "Melena", "Hematemez", "Sarılık", "Asit"])
    secilen_belirtiler.extend(gastro)
with tabs[4]:
    noro = st.multiselect("Nörolojik", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği", "Ataksi"])
    secilen_belirtiler.extend(noro)
with tabs[5]:
    uriner = st.multiselect("Üriner/Endokrin", ["Dizüri", "Hematüri", "Pollaküri", "Poliüri", "Oligüri", "Flank Ağrı", "Polidipsi (Çok Su İçme)", "Aseton Kokusu"])
    secilen_belirtiler.extend(uriner)

# 5. Genişletilmiş Karar Algoritması
def gelismis_analiz(belirtiler, yas, ates, ta_sistolik, spo2):
    rapor = {"teshisler": [], "kan": [], "goruntuleme": [], "kirmizi": ""}
    b_seti = set(belirtiler)

    # Kardiyak & Pulmoner Aciller
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(b_seti):
        rapor["teshisler"].extend(["Akut Miyokard Enfarktüsü", "Pulmoner Emboli", "Pnömotoraks"])
        rapor["kan"].extend(["Troponin", "CK-MB", "D-Dimer", "Arter Kan Gazı"])
        rapor["goruntuleme"].extend(["EKG (Acil)", "Ekokardiyografi", "PA AC Grafisi"])
        rapor["kirmizi"] = "Acil Kardiyak/Pulmoner değerlendirme gereklidir!"

    # Gastrointestinal & Cerrahi Aciller
    if {"Karın Ağrısı (Sağ Alt)", "Karın Ağrısı (Yaygın)", "Melena"}.intersection(b_seti):
        rapor["teshisler"].extend(["Akut Apandisit", "GİS Kanaması", "İleus"])
        rapor["kan"].extend(["Hemogram", "CRP", "Laktat", "Koagülasyon Paneli"])
        rapor["goruntuleme"].extend(["Tüm Batın USG", "Batın BT", "ADBG"])
        if "Melena" in b_seti: rapor["kirmizi"] = "Aktif GİS Kanaması Şüphesi!"

    # Endokrin & Renal (Yeni Eklendi)
    if {"Poliüri", "Polidipsi", "Aseton Kokusu", "Konfüzyon"}.intersection(b_seti):
        rapor["teshisler"].append("Diyabetik Ketoasidoz (DKA)")
        rapor["kan"].extend(["Kan Şekeri", "Keton", "HbA1c", "VİS Elektrolitler"])
    
    if "Oligüri" in b_seti or "Flank Ağrı" in b_seti:
        rapor["teshisler"].append("Akut Böbrek Hasarı / Nefrolitiazis")
        rapor["kan"].extend(["Üre, Kreatinin", "Tam İdrar Tetkiki (TİT)"])
        rapor["goruntuleme"].append("Uriner Sistem USG")

    # Temel raporlama
    if not rapor["teshisler"]:
        rapor["teshisler"].append("Spesifik sendrom eşleşmedi (Viral/Enfeksiyöz?)")
        rapor["kan"].extend(["Hemogram", "CRP", "Biyokimya"])
        
    return rapor

def gemini_analiz_et(yas, cinsiyet, vitals, belirtiler):
    prompt = f"Hasta: {yas}y, {cinsiyet}. Vitals: {vitals}. Semptomlar: {', '.join(belirtiler)}. Profesyonel tıbbi analiz ve tetkik önerileri yap."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Hatası (404/Bağlantı): {str(e)}"

# 6. Sonuç Ekranı
if st.button("ANALİZİ BAŞLAT"):
    if not secilen_belirtiler:
        st.error("⚠️ En az bir belirti seçin.")
    else:
        with st.spinner("Klinik veriler işleniyor..."):
            sonuc = gelismis_analiz(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            time.sleep(1)
            
            if sonuc["kirmizi"]:
                st.markdown(f"<div class='alert-box critical'>🚨 {sonuc['kirmizi']}</div>", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### 📋 Diferansiyel Tanı ve Tetkikler")
                st.write("**Olası Teşhisler:**")
                for t in list(set(sonuc["teshisler"])): st.write(f"- {t}")
                st.write("**Laboratuvar & Görüntüleme:**")
                for tetkik in list(set(sonuc["kan"] + sonuc["goruntuleme"])): st.write(f"- {tetkik}")
                    
            with col_b:
                st.markdown("### 🤖 Yapay Zeka (Gemini) İleri Analizi")
                v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                ai_cevap = gemini_analiz_et(yas, cinsiyet, v_str, secilen_belirtiler)
                st.markdown(f"<div class='alert-box info-box'>{ai_cevap}</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: gray; font-size: 12px;'>© 2026 Dahiliye Klinik Karar Destek</p>", unsafe_allow_html=True)
