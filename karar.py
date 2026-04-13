import streamlit as st
import google.generativeai as genai

# 1. Sayfa Ayarları (Senin geniş ekran düzenin)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# API Yapılandırması (Senin anahtarınla tam entegre edildi)
# Hata almamak için anahtarı buraya sabitliyorum.
MY_API_KEY = "AIzaSyBlN9fG_5vN4L3P-SeninAnahtarin" 

try:
    genai.configure(api_key=MY_API_KEY)
    # 404 hatasını önlemek için en güncel model ismi
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Bağlantı Hatası: {e}")

# Tasarım: Senin Beğendiğin Mavi-Beyaz Profesyonel Tema
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; background-color: #0d6efd; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .alert-box { padding: 15px; border-radius: 8px; margin-top: 10px; font-weight: 500; }
    .critical { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
    .info-box { background-color: #e7f3ff; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 3.2 (Tam Kapsamlı & Stabil)")
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

# 4. En Geniş Semptom Kategorileri (Branşlara Göre)
st.subheader("🔍 Klinik Semptom Seçimi")
tabs = st.tabs(["Genel", "Kardiyo/Solunum", "Gastro", "Nöro", "Endokrin/Üriner", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]:
    secilen.extend(st.multiselect("Sistemik", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "Kilo Kaybı", "Lenfadenopati", "Kaşıntı", "Titreme"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik", ["Göğüs Ağrısı (Baskı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop", "Nefes Darlığı", "Hemoptizi"]))
with tabs[2]:
    secilen.extend(st.multiselect("Gastrointestinal", ["Karın Ağrısı (Sağ Alt)", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Kusma", "Diyare"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nörolojik", ["Baş Ağrısı", "Baş Dönmesi", "Bilinç Bulanıklığı", "Güç Kaybı", "Dizartri", "Nöbet", "Ense Sertliği"]))
with tabs[4]:
    secilen.extend(st.multiselect("Endo/Üriner", ["Dizüri", "Hematüri", "Oligüri", "Poliüri", "Polidipsi", "Aseton Kokusu"]))
with tabs[5]:
    secilen.extend(st.multiselect("Özel Branşlar", ["Sabah Sertliği", "Eklem Şişliği", "Kelebek Döküntü", "Peteşi/Purpura", "Splenomegali", "Solukluk"]))

# 5. Klinik Karar Algoritması (Senin Zengin Analizlerin)
def cdss_motoru(s, y, a, ta):
    res = {"tanilar": [], "tetkikler": [], "kirmizi": ""}
    ss = set(s)
    
    if {"Göğüs Ağrısı (Baskı)", "Nefes Darlığı"}.intersection(ss):
        res["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli"])
        res["tetkikler"].extend(["EKG", "Troponin", "D-Dimer"])
        res["kirmizi"] = "Kardiyak Acil Şüphesi! Monitörizasyon önerilir."
        
    if {"Karın Ağrısı (Sağ Alt)", "Melena"}.intersection(ss):
        res["tanilar"].extend(["Akut Apandisit", "GİS Kanama"])
        res["tetkikler"].extend(["Batın BT", "Hemogram", "Endoskopi"])
        if "Melena" in ss: res["kirmizi"] = "Aktif Kanama Şüphesi! Acil konsültasyon."

    if "Aseton Kokusu" in ss:
        res["tanilar"].append("Diyabetik Ketoasidoz (DKA)")
        res["tetkikler"].extend(["Kan Şekeri", "Venöz Kan Gazı", "İdrar Ketonu"])

    if {"Kelebek Döküntü", "Sabah Sertliği"}.intersection(ss):
        res["tanilar"].append("Sistemik Lupus (SLE) / RA")
        res["tetkikler"].extend(["ANA", "Anti-dsDNA", "RF", "Sedimantasyon"])

    if a > 38.5 and ta < 100:
        res["tanilar"].append("Sepsis")
        res["kirmizi"] = "Sepsis Riski! Laktat ve Kan Kültürü planlanmalıdır."

    return res

# 6. Analiz Butonu ve İki Sütunlu Görünüm (En Beğendiğin Şekil)
if st.button("KLİNİK ANALİZİ BAŞLAT"):
    if not secilen:
        st.error("⚠️ Lütfen belirti seçiniz.")
    else:
        sonuc = cdss_motoru(secilen, yas, ates, ta_sistolik)
        
        if sonuc["kirmizi"]:
            st.markdown(f"<div class='alert-box critical'>🚨 **ACİL UYARI:** {sonuc['kirmizi']}</div>", unsafe_allow_html=True)
        
        col_sol, col_sag = st.columns(2)
        
        with col_sol:
            st.subheader("📋 Diferansiyel Tanı ve Tetkikler")
            st.write("**Olası Ön Tanılar:**")
            for t in set(sonuc["tanilar"] if sonuc["tanilar"] else ["Genel Değerlendirme"]):
                st.write(f"- {t}")
            st.write("**İstenmesi Gereken Tetkikler:**")
            # Hata Çözümü: Tetkik listesini güvenli bir sete çevirip döngüye sokuyorum
            tet_list = set(sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "CRP", "Biyokimya"])
            for tet in tet_list:
                st.write(f"- {tet}")
        
        with col_sag:
            st.subheader("🤖 Gemini AI İleri Analizi")
            try:
                v_bilgi = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                prompt = f"Uzman CDSS: {yas}y, {cinsiyet}. Vitaller: {v_bilgi}. Belirtiler: {', '.join(secilen)}. Ayırıcı tanı ve tetkik öner."
                
                response = model.generate_content(prompt)
                st.markdown(f"<div class='alert-box info-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Hatası: {e}")

st.markdown("<br><p style='text-align: center; color: gray; font-size: 11px;'>© 2026 Dahiliye Karar Destek v3.2</p>", unsafe_allow_html=True)
