import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Hata giderildi)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Bazı kütüphane sürümleri için model ismini güncelledim
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ Gemini API anahtarı eksik! Streamlit Secrets ayarlarına GEMINI_API_KEY ekleyin.")

# Tasarım (CSS) - Orijinal Renklerin
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; color: #212529; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; border: none; height: 3em; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #0b5ed7; }
    h1, h2, h3 { color: #0d6efd; border-bottom: 2px solid #dee2e6; padding-bottom: 10px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #cff4fc; color: #055160; border: 1px solid #b6effb; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("<h1 style='text-align: center; font-size: 50px; border: none;'>⚕️</h1>", unsafe_allow_html=True)
with col2:
    st.title("Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
    st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 1.2 (Tam Sürüm)")

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

# 4. Semptom Seçimi (Eksiksiz Liste)
st.subheader("🔍 Klinik Semptom Seçimi")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Sistemik", "Kardiyovasküler", "Solunum", "Gastrointestinal", "Nörolojik", "Üriner"
])

secilen_belirtiler = []

with tab1:
    sistemik = st.multiselect("Sistemik Belirtiler", ["Yüksek Ateş", "Halsizlik/Yorgunluk", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Yaygın Kas Ağrısı", "Eklem Ağrısı", "Titreme", "İştahsızlık"])
    secilen_belirtiler.extend(sistemik)
with tab2:
    kardiyo = st.multiselect("Kardiyovasküler Belirtiler", ["Göğüs Ağrısı (Baskı tarzı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop (Bayılma)", "Bilateral Alt Ekstremite Ödemi", "Eforla Gelen Nefes Darlığı", "Ortopne"])
    secilen_belirtiler.extend(kardiyo)
with tab3:
    solunum = st.multiselect("Solunum Sistemi Belirtileri", ["Nefes Darlığı (Dispne)", "Kuru Öksürük", "Balgamlı Öksürük", "Hemoptizi", "Hışıltılı Solunum", "Siyanoz"])
    secilen_belirtiler.extend(solunum)
with tab4:
    gastro = st.multiselect("Gastrointestinal Belirtiler", ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Sağ Alt Kadran)", "Bulantı", "Kusma", "Diyare", "Melena", "Hematemez", "Sarılık"])
    secilen_belirtiler.extend(gastro)
with tab5:
    noro = st.multiselect("Nörolojik Belirtiler", ["Baş Ağrısı", "Baş Dönmesi", "Bilinç Bulanıklığı", "Tek Taraflı Güç Kaybı", "Konuşma Bozukluğu", "Nöbet", "Ense Sertliği"])
    secilen_belirtiler.extend(noro)
with tab6:
    uriner = st.multiselect("Üriner Sistem Belirtileri", ["Dizüri", "Hematüri", "Sık İdrara Çıkma", "Poliüri", "Oligüri", "Yan Ağrısı"])
    secilen_belirtiler.extend(uriner)

st.divider()

# 5. Orijinal Analiz Algoritman (Geri Getirildi)
def gelismis_analiz(belirtiler, yas, ates, ta_sistolik, spo2):
    rapor = {"teshisler": [], "kan_tetkikleri": [], "goruntuleme": [], "kirmizi_bayrak": ""}
    b_seti = set(belirtiler)

    if {"Göğüs Ağrısı (Baskı tarzı)", "Nefes Darlığı (Dispne)"}.intersection(b_seti):
        rapor["teshisler"].extend(["Akut Miyokard Enfarktüsü", "Pulmoner Emboli"])
        rapor["kan_tetkikleri"].extend(["High-Sensitive Troponin", "D-Dimer", "Arter Kan Gazı"])
        rapor["goruntuleme"].extend(["12 Derivasyonlu EKG", "Ekokardiyografi"])
        rapor["kirmizi_bayrak"] = "Kardiyak acil şüphesi! EKG ilk 10 dk içinde çekilmelidir."

    if {"Karın Ağrısı (Sağ Alt Kadran)", "Bulantı"}.intersection(b_seti):
        rapor["teshisler"].append("Akut Apandisit")
        rapor["kan_tetkikleri"].extend(["Hemogram", "CRP", "Amilaz/Lipaz"])
        rapor["goruntuleme"].append("Tüm Batın USG")

    if not rapor["teshisler"]:
        rapor["teshisler"].append("Spesifik sendrom eşleşmedi (Viral/Genel Değerlendirme)")
        rapor["kan_tetkikleri"].extend(["Hemogram", "Biyokimya Paneli"])
    
    return rapor

def gemini_analiz_et(yas, cinsiyet, vitals, belirtiler):
    prompt = f"Sen uzman doktora yardım eden bir CDSS sistemisin. Hasta: {yas}y, {cinsiyet}. Vitals: {vitals}. Semptomlar: {', '.join(belirtiler)}. Ayırıcı tanı ve ileri tetkik önerilerini profesyonelce yaz."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Hatası: {str(e)}"

# 6. Sonuçların Gösterilmesi
if st.button("TIBBİ ALGORİTMAYI ÇALIŞTIR VE ANALİZ ET"):
    if not secilen_belirtiler:
        st.error("⚠️ Lütfen semptom seçiniz.")
    else:
        with st.spinner("Analiz ediliyor..."):
            sonuc = gelismis_analiz(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            time.sleep(1)
            
            if sonuc["kirmizi_bayrak"]:
                st.markdown(f"<div class='alert-box critical'>🚨 {sonuc['kirmizi_bayrak']}</div>", unsafe_allow_html=True)
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader("📋 Diferansiyel Tanı ve Tetkikler")
                st.write("**Olası Teşhisler:**")
                for t in list(set(sonuc["teshisler"])): st.write(f"- {t}")
                st.write("**Önerilen Laboratuvar:**")
                for k in list(set(sonuc["kan_tetkikleri"])): st.write(f"- {k}")
                st.write("**Görüntüleme:**")
                for g in list(set(sonuc["goruntuleme"])): st.write(f"- {g}")
                    
            with res_col2:
                st.subheader("🤖 Gemini AI İleri Analizi")
                v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                ai_cevap = gemini_analiz_et(yas, cinsiyet, v_str, secilen_belirtiler)
                st.markdown(f"<div class='alert-box info-box'>{ai_cevap}</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #6c757d; font-size: 14px;'>© 2026 Dahiliye Klinik Destek Sistemleri</p>", unsafe_allow_html=True)
