import streamlit as st
import google.generativeai as genai

# 1. Sayfa Konfigürasyonu (Ultra Geniş Düzen)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# 2. API Yapılandırması (GitHub/Secrets Hatalarını Devre Dışı Bırakan Kesin Çözüm)
# Secrets kısmında hata olsa bile bu anahtar sistemi çalıştıracaktır.
API_KEY = "AIzaSyD2DTlEW1mcv07-C3P1LsMHsCkV_XevkBo" #

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

# 3. Görsel Tasarım (Zengin CSS)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #0d6efd; color: white; font-weight: bold; border-radius: 10px; height: 3.5em; width: 100%; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; }
    .result-card { padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #d1d9e6; }
    .critical-box { background-color: #fff5f5; border-left: 6px solid #e03131; }
    .ai-box { background-color: #f8f9ff; border-left: 6px solid #1971c2; }
    </style>
    """, unsafe_allow_html=True)

# 4. Header
st.title("⚕️ Gelişmiş Dahiliye Klinik Karar Destek Sistemi")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 3.8 (Ultra Zengin & Hata Arındırılmış)")
st.divider()

# 5. Sidebar: Vital Bulgular
with st.sidebar:
    st.header("📋 Hasta Vitalleri")
    yas = st.number_input("Yaş", 0, 120, 45)
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    nabiz = st.number_input("Nabız", 30, 220, 80)
    ta_sistolik = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)
    st.write("---")
    st.info("Sistemik sepsis ve şok taraması vitallere göre otomatik yapılır.")

# 6. En Geniş Semptom Paneli
st.subheader("🔍 Klinik Bulgular ve Semptomlar")
t1, t2, t3, t4, t5 = st.tabs(["Gastro/Genel", "Kardiyo/Solunum", "Nörolojik", "Endokrin/Nefro", "Romatoloji/Hemato"])

secilen = []
with t1:
    secilen.extend(st.multiselect("Gastrointestinal & Genel", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Kusma", "Diyare", "Yüksek Ateş", "Kilo Kaybı", "Lenfadenopati"]))
with t2:
    secilen.extend(st.multiselect("Kardiyovasküler & Solunum", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Nefes Darlığı", "Çarpıntı", "Senkop", "Hemoptizi", "Öksürük", "Ortopne"]))
with t3:
    secilen.extend(st.multiselect("Nöroloji", ["Şiddetli Baş Ağrısı", "Baş Dönmesi", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with t4:
    secilen.extend(st.multiselect("Endokrin & Üriner", ["Dizüri", "Hematüri", "Oligüri", "Poliüri/Polidipsi", "Aseton Kokusu", "Flank Ağrı"]))
with t5:
    #
    secilen.extend(st.multiselect("Romatoloji & Hematoloji", ["Kelebek Döküntü", "Sabah Sertliği", "Eklem Şişliği", "Peteşi/Purpura", "Splenomegali", "Solukluk"]))

# 7. Manuel Karar Motoru (Geliştirilmiş)
def analiz_algoritmasi(s, a, ts):
    res = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    
    # - GİS ve Akut Batın
    if {"Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez"}.intersection(ss):
        res["tanilar"].extend(["Akut Apandisit", "Üst/Alt GİS Kanama", "Mezenter İskemi"])
        res["tetkikler"].extend(["Batın BT", "Hemogram", "Endoskopi", "ADBG", "Laktat"])
        if "Melena" in ss or "Hematemez" in ss:
            res["kirmizi"] = "Aktif GİS Kanaması Şüphesi! Acil Konsültasyon ve Resüsitasyon."

    # Kardiyak
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(ss):
        res["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli"])
        res["tetkikler"].extend(["EKG", "Troponin", "D-Dimer", "PAAC"])
    
    # - Romatoloji
    if "Kelebek Döküntü" in ss or "Sabah Sertliği" in ss:
        res["tanilar"].extend(["Sistemik Lupus (SLE)", "Romatoid Artrit"])
        res["tetkikler"].extend(["ANA", "Anti-dsDNA", "RF", "Sedimantasyon"])

    # Sepsis
    if a > 38.5 and ts < 100:
        res["tanilar"].append("Sepsis / Septik Şok")
        res["kirmizi"] = "Sepsis Riski! IV Antibiyotik ve Laktat takibi önerilir."
        
    return res

# 8. Analiz ve Yan Yana Düzen
st.markdown("<br>", unsafe_allow_html=True)
if st.button("TÜM SİSTEMLERİ ÇALIŞTIR VE ANALİZ ET"):
    if not secilen:
        st.warning("Lütfen bulgu seçin.")
    else:
        sonuc = analiz_algoritmasi(secilen, ates, ta_sistolik)
        
        if sonuc["kirmizi"]:
            st.error(f"🚨 KRİTİK: {sonuc['kirmizi']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Diferansiyel Tanı ve Tetkikler")
            st.write("**Olası Tanılar:**")
            t_liste = set(sonuc["tanilar"] if sonuc["tanilar"] else ["Genel Değerlendirme"])
            for t in t_liste: st.write(f"✅ {t}")
            
            st.write("**İstenmesi Gereken Tetkikler:**")
            # - Hatalı liste döngüsü düzeltildi
            nihai_liste = set(sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "CRP", "Biyokimya"])
            for kalem in nihai_liste:
                st.write(f"🧪 {kalem}")
        
        with col2:
            st.subheader("🤖 Gemini AI Derin Analiz")
            try:
                # - API bağlantısı güvenli hale getirildi
                v_text = f"Yaş:{yas}, Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                p = f"Doktor asistanı olarak şu hastayı analiz et: {v_text}. Bulgular: {', '.join(secilen)}. Ayırıcı tanı ve tetkik öner."
                r = model.generate_content(p)
                st.markdown(f"<div class='result-card ai-box'>{r.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Hatası: {e}. Lütfen API anahtarını kontrol edin.")

st.markdown("<p style='text-align: center; color: gray; font-size: 10px;'>Dahiliye CDSS v3.8 | Profesyonel Kullanım İçindir</p>", unsafe_allow_html=True)
