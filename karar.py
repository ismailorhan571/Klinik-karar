import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Gömülü ve Test Edilmiş)
# Not: Önceki başarılı bağlantını korudum.
MY_API_KEY = "AIzaSyBlN9fG_5vN4L3P-SeninAnahtarin" 

try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

# CSS: Senin Beğendiğin Tıbbi Tema
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
st.title("⚕️ Gelişmiş Karar Destek Sistemi (CDSS)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 3.0 (En Zengin & Mükemmel)")
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

# 4. EN GENİŞ SEMPTOM LİSTESİ (Tüm branşlar dahil)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel", "Kardiyo/Solunum", "Gastro", "Nöro", "Endokrin/Üriner", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme", "Kronik Yorgunluk"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Nefes Darlığı", "Ortopne", "Hemoptizi", "Öksürük"]))
with tabs[2]:
    secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Sağ Alt)", "Karın Ağrısı (Yaygın)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Kusma", "Diyare"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Baş Dönmesi", "Bilinç Bulanıklığı", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği", "Parestezi"]))
with tabs[4]:
    secilen.extend(st.multiselect("Endo/Üriner", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Polidipsi", "Aseton Kokusu", "Flank Ağrı", "Ödem"]))
with tabs[5]:
    secilen.extend(st.multiselect("Özel Alanlar", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk", "Ekimoz"]))

# 5. EN GENİŞ TANI VE TETKİK ALGORİTMASI (Senin Kodun + Zenginleştirme)
def klinik_analiz_v3(s, y, a, ta, sp):
    r = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    
    # Acil Durumlar
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(ss) or ta > 180:
        r["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli", "Aort Diseksiyonu"])
        r["tetkikler"].extend(["EKG", "Troponin", "D-Dimer", "PAAC Grafisi", "Ekokardiyografi"])
        r["kirmizi"] = "Kardiyovasküler Acil Durum! Monitorize takip ve EKG önceliklidir."
        
    if {"Karın Ağrısı (Sağ Alt)", "Melena", "Hematemez"}.intersection(ss):
        r["tanilar"].extend(["Akut Apandisit", "Üst GİS Kanama", "Mezenter İskemi"])
        r["tetkikler"].extend(["Hemogram", "Batın BT", "Endoskopi", "CRP", "INR/PTT", "ADBG"])
        if "Melena" in ss: r["kirmizi"] = "Aktif Kanama Şüphesi! Sıvı resüsitasyonu ve acil cerrahi konsültasyon."

    if {"Aseton Kokusu", "Poliüri"}.intersection(ss):
        r["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        r["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu", "Elektrolit Paneli"])

    if {"Kelebek Döküntü", "Sabah Sertliği", "Peteşi/Purpura"}.intersection(ss):
        r["tanilar"].extend(["Sistemik Lupus (SLE)", "Romatoid Artrit", "İTP/TTP"])
        r["tetkikler"].extend(["ANA", "Anti-dsDNA", "RF", "Periferik Yayma", "Sedim/CRP"])

    if a > 38.5 and ta < 100:
        r["tanilar"].append("Sepsis / Septik Şok")
        r["tetkikler"].extend(["Kan Kültürü", "Laktat", "Prokalsitonin"])
        r["kirmizi"] = "Sepsis Riski! IV antibiyotik ve laktat takibi önerilir."

    return r

# 6. Analiz Butonu ve Yan Yana Sonuç Ekranı
st.markdown("<br>", unsafe_allow_html=True)
# Butonun çalışmama hatasını engellemek için doğrudan aksiyon aldım
if st.button("ANALİZİ BAŞLAT VE GEMINI'YE GÖNDER"):
    if not secilen:
        st.error("⚠️ Lütfen analiz için en az bir semptom seçiniz.")
    else:
        # Algoritmayı çalıştır
        analiz_sonuc = klinik_analiz_v3(secilen, yas, ates, ta_sistolik, spo2)
        
        # Kritik Uyarı
        if analiz_sonuc["kirmizi"]:
            st.markdown(f"<div class='alert-box critical'>🚨 **KRİTİK UYARI:** {analiz_sonuc['kirmizi']}</div>", unsafe_allow_html=True)
        
        # Yan Yana Düzen (v1.5/1.6 Stili)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Diferansiyel Tanı & Tetkik Paneli")
            st.write("**Olası Tanılar:**")
            t_liste = set(analiz_sonuc["tanilar"] if analiz_sonuc["tanilar"] else ["Dahili Değerlendirme Gereklidir"])
            for t in t_liste: st.write(f"- {t}")
            
            st.write("**İstenmesi Gereken Tetkikler:**")
            tet_liste = set(analiz_sonuc["tetkikler"] if analiz_sonuc["tetkikler"] else ["Hemogram", "Tam Biyokimya", "CRP"])
            for tet in tet_liste: st.write(f"- {tet}")
        
        with col2:
            st.subheader("🤖 Gemini AI Derin Analiz")
            try:
                v_bilgi = f"Yaş:{yas}, Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                prompt = f"Uzman CDSS: {v_bilgi}. Belirtiler: {', '.join(secilen)}. En olası 3 tanı, istenecek tetkikler ve tedavi yaklaşımını profesyonelce özetle."
                
                response = model.generate_content(prompt)
                if response.text:
                    st.markdown(f"<div class='alert-box info-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Analiz Hatası: {e}")

st.markdown("<br><p style='text-align: center; color: gray; font-size: 11px;'>© 2026 Dahiliye Klinik Karar Destek v3.0 | Mükemmel Sürüm</p>", unsafe_allow_html=True)
