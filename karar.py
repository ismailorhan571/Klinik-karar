import streamlit as st
import google.generativeai as genai

# 1. Sayfa Konfigürasyonu (Eski Geniş Düzen)
st.set_page_config(page_title="Dahiliye Karar Destek", page_icon="⚕️", layout="wide")

# 2. API ANAHTARI (Doğrudan Koda Gömüldü - En Sağlam Yol)
API_KEY = "AIzaSyD2DTlEW1mcv07-C3P1LsMHsCkV_XevkBo"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Bağlantı Hatası: {e}")

# 3. Zengin Görsel Tasarım (v3.7 Stili)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { background-color: #004a99; color: white; font-weight: bold; border-radius: 12px; height: 3.5em; width: 100%; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: 700; color: #004a99; }
    .ai-box { background-color: #ffffff; padding: 25px; border-radius: 15px; border-left: 8px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 4. Header
st.title("⚕️ Dahiliye Klinik Karar Destek Sistemi (CDSS)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 3.7 (Restore Edilmiş & Stabil)")
st.divider()

# 5. Sidebar: Vital Bulgular
with st.sidebar:
    st.header("📋 Hasta Vitalleri")
    yas = st.number_input("Yaş", 0, 120, 45)
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    nabiz = st.number_input("Nabız", 30, 220, 80)
    ta_sis = st.number_input("Sistolik TA", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA", 30, 150, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 6. Sekmeli Semptom Paneli (v3.7'nin Kalbi)
st.subheader("🔍 Klinik Bulgular")
t1, t2, t3, t4 = st.tabs(["🩺 Genel & Gastro", "🫁 Kardiyo & Solunum", "🧠 Nöroloji", "🦋 Romatoloji & Endokrin"])

secilen = []
with t1:
    secilen.extend(st.multiselect("Gastrointestinal", ["Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez", "Sarılık", "Kilo Kaybı", "Diyare"]))
with t2:
    secilen.extend(st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı)", "Nefes Darlığı", "Çarpıntı", "Hemoptizi", "Öksürük"]))
with t3:
    secilen.extend(st.multiselect("Nörolojik", ["Şiddetli Baş Ağrısı", "Konfüzyon", "Güç Kaybı", "Dizartri", "Ense Sertliği"]))
with t4:
    secilen.extend(st.multiselect("Özel Alanlar", ["Kelebek Döküntü", "Sabah Sertliği", "Eklem Şişliği", "Dizüri", "Oligüri"]))

# 7. Manuel Analiz Motoru
def analiz(s, a):
    t, tet = [], []
    ss = set(s)
    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(ss):
        t.extend(["Akut Apandisit", "GİS Kanama"])
        tet.extend(["Batın BT", "Endoskopi", "Hemogram"])
    if "Kelebek Döküntü" in ss:
        t.append("Sistemik Lupus (SLE)")
        tet.extend(["ANA", "Anti-dsDNA", "Sedim"])
    if a > 38.5:
        t.append("Sistemik Enfeksiyon / Sepsis")
        tet.extend(["CRP", "Prokalsitonin", "Kültür"])
    return t, tet

# 8. Sonuç Bölümü
if st.button("SİSTEMİ ÇALIŞTIR VE ANALİZ ET"):
    if not secilen:
        st.warning("Lütfen bulgu seçin.")
    else:
        tanilar, tetkikler = analiz(secilen, ates)
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📋 Diferansiyel Tanı")
            for h in (tanilar if tanilar else ["İleri Tetkik Gerekiyor"]):
                st.write(f"✅ {h}")
            
            st.divider()
            st.subheader("🧪 Önerilen Tetkikler")
            # Değişken adı hatası giderildi
            nihai_tetkikler = set(tetkikler if tetkikler else ["Tam Kan", "Biyokimya", "TİT"])
            for kalem in nihai_tetkikler:
                st.
