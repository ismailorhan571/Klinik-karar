import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Anahtarın Hatasız Yerleştirildi)
MY_API_KEY = "AIzaSyBlN9fG_5vN4L3P-SeninGercekAnahtarin" 

try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

# Tasarım: Senin Beğendiğin Mavi-Beyaz Tema
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .info-box { background-color: #e7f3ff; color: #0c5460; border: 1px solid #bee5eb; padding: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 3.4 (Hatalar Arındırıldı)")
st.divider()

# 3. Sidebar: Vitaller
with st.sidebar:
    st.header("📋 Hasta Profili & Vitaller")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sistolik = st.number_input("Sistolik TA", 50, 250, 120)
    ta_diastolik = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 4. Semptom Seçimi (Tüm Branşlar)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel", "Kardiyo/Solunum", "Gastro", "Nöro", "Endokrin/Üriner", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]: secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"]))
with tabs[1]: secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Nefes Darlığı", "Hemoptizi"]))
with tabs[2]: secilen.extend(st.multiselect("Gastro", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Kusma", "Diyare"]))
with tabs[3]: secilen.extend(st.multiselect("Nöro", ["Baş Ağrısı", "Baş Dönmesi", "Konfüzyon", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with tabs[4]: secilen.extend(st.multiselect("Endo/Üriner", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Polidipsi", "Aseton Kokusu"]))
with tabs[5]: secilen.extend(st.multiselect("Özel Alanlar", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk"]))

# 5. Karar Motoru
def analiz_motoru(s, a, ta):
    res = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(ss):
        res["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli"])
        res["tetkikler"].extend(["EKG", "Troponin", "D-Dimer"])
        res["kirmizi"] = "Kardiyak Acil Şüphesi!"
    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(ss):
        res["tanilar"].extend(["Akut Apandisit", "GİS Kanama", "Mezenter İskemi"])
        res["tetkikler"].extend(["Batın BT", "Hemogram", "Endoskopi", "ADBG"])
    if "Aseton Kokusu" in ss:
        res["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        res["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu"])
    if a > 38.5 and ta < 100:
        res["tanilar"].append("Sepsis")
        res["kirmizi"] = "Sepsis Riski! IV Antibiyotik ve Laktat önerilir."
    return res

# 6. Analiz Butonu ve Yan Yana Düzen
st.markdown("<br>", unsafe_allow_html=True)
if st.button("ANALİZİ BAŞLAT VE GEMINI'YE GÖNDER"):
    if not secilen:
        st.error("⚠️ Lütfen semptom seçiniz.")
    else:
        sonuc = analiz_motoru(secilen, ates, ta_sistolik)
        
        if sonuc["kirmizi"]:
            st.error(f"🚨 KRİTİK: {sonuc['kirmizi']}")
            
        col_sol, col_sag = st.columns(2)
        
        with col_sol:
            st.subheader("📋 Diferansiyel Tanı & Tetkikler")
            st.write("**Olası Ön Tanılar:**")
            t_liste = set(sonuc["tanilar"] if sonuc["tanilar"] else ["Dahilî Değerlendirme"])
            for t in t_liste: st.write(f"- {t}")
            
            st.write("**İstenmesi Gereken Tetkikler:**")
            # Hata Çözümü: Değişken ismi tetkik_nihai olarak sabitlendi.
            tetkik_nihai = set(sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "CRP", "Biyokimya"])
            for t in tetkik_nihai:
                st.write(f"- {t}")
                
        with col_sag:
            st.subheader("🤖 Gemini AI Derin Analiz")
            try:
                v_bilgi = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                prompt = f"Uzman CDSS: {yas}y, {cinsiyet}. Vitaller: {v_bilgi}. Belirtiler: {', '.join(secilen)}. Tanı ve tetkik öner."
                response = model.generate_content(prompt)
                st.markdown(f"<div class='info-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Hatası: {e}")

st.markdown("<br><p style='text-align: center; color: gray; font-size: 11px;'>© 2026 Dahiliye Karar Destek v3.4</p>", unsafe_allow_html=True)
