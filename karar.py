import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# Gemini API Yapılandırması (404 Hatasını Çözen Yeni Yapı)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # HATA ÇÖZÜMÜ: Bazı sistemlerde 'models/' eki şarttır.
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Streamlit Secrets kısmına GEMINI_API_KEY ekleyin.")

# CSS: Senin profesyonel tıbbi teman
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
    st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.4 (Maksimum Zenginlik)")

st.divider()

# 3. Sol Menü (Hasta Profili & Vitaller)
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
    st.info("💡 **Bilgi:** CDSS, hekimin klinik yargısını desteklemek için tasarlanmıştır.")

# 4. Semptom Seçimi (Daha Zengin İçerik)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel/Sistemik", "Kardiyovasküler", "Solunum", "Gastrointestinal", "Nörolojik", "Üriner/Endokrin"])

secilen_belirtiler = []

with tabs[0]:
    sistemik = st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik/Yorgunluk", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Yaygın Miyalji", "Artralji", "Titreme", "İştahsızlık", "Lenfadenopati (LAP)", "Kaşıntı"])
    secilen_belirtiler.extend(sistemik)
with tabs[1]:
    kardiyo = st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Periferik Ödem", "Efor Dispnesi", "Ortopne", "PND", "Asit"])
    secilen_belirtiler.extend(kardiyo)
with tabs[2]:
    solunum = st.multiselect("Solunum", ["Dispne", "Kuru Öksürük", "Balgamlı Öksürük", "Hemoptizi", "Hışıltılı Solunum", "Plöretik Ağrı", "Siyanoz", "Ses Kısıklığı"])
    secilen_belirtiler.extend(solunum)
with tabs[3]:
    gastro = st.multiselect("Gastrointestinal", ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Sağ Alt)", "Karın Ağrısı (Sol Alt)", "Epigastrik Ağrı", "Bulantı", "Kusma", "Diyare", "Melena", "Hematemez", "Sarılık", "Disfaji"])
    secilen_belirtiler.extend(gastro)
with tabs[4]:
    noro = st.multiselect("Nörolojik", ["Baş Ağrısı", "Vertigo", "Konfüzyon", "Fokal Güç Kaybı", "Dizartri/Afazi", "Nöbet", "Ense Sertliği", "Ataksi", "Fotofobi"])
    secilen_belirtiler.extend(noro)
with tabs[5]:
    uriner = st.multiselect("Üriner/Endokrin", ["Dizüri", "Hematüri", "Pollaküri", "Poliüri", "Oligüri/Anüri", "Flank Ağrı", "Polidipsi", "Aseton Kokusu", "Hiperglisemi Bulguları"])
    secilen_belirtiler.extend(uriner)

# 5. Karar Algoritması (Zenginleştirilmiş Versiyon)
def gelismis_analiz(belirtiler, yas, ates, ta_sistolik, spo2):
    rapor = {"teshisler": [], "kan": [], "goruntuleme": [], "kirmizi": ""}
    b_seti = set(belirtiler)

    # Kardiyak & Torasik Aciller
    if {"Göğüs Ağrısı (Baskı)", "Dispne", "Ortopne"}.intersection(b_seti):
        rapor["teshisler"].extend(["AKS (MI Şüphesi)", "Kalp Yetmezliği", "Pulmoner Emboli"])
        rapor["kan"].extend(["Troponin", "CK-MB", "D-Dimer", "NT-proBNP"])
        rapor["goruntuleme"].extend(["EKG (Acil)", "EKO", "PAAC Grafisi"])
        rapor["kirmizi"] = "Kardiyak acil! EKG ve Vital takibi kritik."

    # Akut Batın & GİS
    if {"Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez"}.intersection(b_seti):
        rapor["teshisler"].extend(["Akut Apandisit", "Üst/Alt GİS Kanama", "Perforasyon"])
        rapor["kan"].extend(["Hemogram", "CRP", "INR/PTT", "Laktat"])
        rapor["goruntuleme"].extend(["Tüm Batın USG", "ADBG", "Batın BT"])
        if "Melena" in b_seti: rapor["kirmizi"] = "Aktif Kanama Şüphesi! Damar yolu ve sıvı desteği."

    # Nefroloji & Endokrin (Zenginleştirme)
    if {"Oligüri/Anüri", "Flank Ağrı", "Hematüri"}.intersection(b_seti):
        rapor["teshisler"].append("Akut Böbrek Hasarı (ABH) / Üreter Taşı")
        rapor["kan"].extend(["Üre, Kreatinin", "Elektrolit Paneli", "TİT"])
        rapor["goruntuleme"].append("Üriner USG / Kontrastsız Batın BT")

    if {"Poliüri", "Polidipsi", "Aseton Kokusu"}.intersection(b_seti):
        rapor["teshisler"].append("Diyabetik Ketoasidoz (DKA) / Hiperglisemik Durum")
        rapor["kan"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu"])

    # Enfeksiyon & Sepsis
    if (ates > 38.3 or ates < 36.0) and ta_sistolik < 100:
        rapor["teshisler"].append("Sepsis / Septik Şok?")
        rapor["kan"].extend(["Kan Kültürü", "Prokalsitonin", "Laktat"])

    # Boş kalmasın
    if not rapor["teshisler"]:
        rapor["teshisler"].append("Genel Dahili Değerlendirme Gereklidir")
        rapor["kan"].extend(["Hemogram", "Biyokimya"])

    return rapor

# Gemini Fonksiyonu
def ai_analizi_yap(yas, cinsiyet, vitals, belirtiler):
    prompt = f"""
    Sen bir Klinik Karar Destek asistanısın.
    Hasta: {yas} yaşında, {cinsiyet}.
    Vitaller: {vitals}.
    Semptomlar: {', '.join(belirtiler)}.
    
    Lütfen:
    1. En olası 3 Diferansiyel Tanı,
    2. İleri Laboratuvar ve Görüntüleme önerileri,
    3. Tedaviye yönelik kısa klinik notlar yaz.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Bağlantı Hatası: {str(e)}"

# 6. Analiz Ekranı
if st.button("KLİNİK ANALİZİ BAŞLAT"):
    if not secilen_belirtiler:
        st.error("⚠️ Lütfen en az bir semptom seçin.")
    else:
        with st.spinner("Algoritmalar ve AI çalışıyor..."):
            sonuc = gelismis_analiz(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            time.sleep(0.5)
            
            if sonuc["kirmizi"]:
                st.markdown(f"<div class='alert-box critical'>🚨 {sonuc['kirmizi']}</div>", unsafe_allow_html=True)
            
            col_left, col_right = st.columns(2)
            with col_left:
                st.subheader("📋 Algoritmik Bulgular")
                st.write("**Olası Tanılar:**")
                for t in list(set(sonuc["teshisler"])): st.write(f"- {t}")
                st.write("**Tetkik Önerileri:**")
                for tetkik in list(set(sonuc["kan"] + sonuc["goruntuleme"])): st.write(f"- {tetkik}")
                    
            with col_right:
                st.subheader("🤖 Gemini AI Derin Analiz")
                v_str = f"
