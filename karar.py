import streamlit as st
import google.generativeai as genai

# 1. Sayfa Konfigürasyonu (Geniş Ekran)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# 2. API Yapılandırması (Çift Katmanlı Koruma)
# Secrets'ta varsa oradan alır, yoksa senin verdiğin anahtarı kullanır.
MY_API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyD2DTlEW1mcv07-C3P1LsMHsCkV_XevkBo")

try:
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

# 3. Görsel Tasarım (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e9ecef; border-radius: 5px; padding: 10px; }
    .stButton>button { background-color: #0d6efd; color: white; border-radius: 8px; height: 3.5em; width: 100%; font-weight: bold; }
    .status-box { padding: 15px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #dee2e6; }
    .critical-alert { background-color: #fff3f3; border-left: 5px solid #dc3545; color: #a94442; }
    .ai-box { background-color: #f0f7ff; border-left: 5px solid #007bff; color: #0c5460; }
    </style>
    """, unsafe_allow_html=True)

# 4. Başlık ve Geliştirici Bilgisi
st.title("⚕️ Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
st.markdown(f"**Geliştirici:** İsmail Orhan | **Sürüm:** 3.7 (Tam Kapsamlı & Stabil)")
st.divider()

# 5. Sidebar: Hasta Vitalleri
with st.sidebar:
    st.header("📋 Hasta Profili & Vitaller")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtilmemiş"])
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_s = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_d = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    nabiz = st.number_input("Nabız (vuru/dk)", 30, 220, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)
    st.info("Kırmızı Bayraklar: Ateş > 38.5 veya Sistolik TA < 90 ise sepsis riski artar.")

# 6. Ultra Geniş Semptom Paneli (Hiçbir Branş Çıkarılmadı)
st.subheader("🔍 Klinik Semptom ve Belirti Seçimi")
tabs = st.tabs(["Sistemik/Genel", "Kardiyo/Pulmoner", "Gastrointestinal", "Nörolojik", "Endokrin/Nefro", "Romatoloji/Hematoloji"])

secilen = []
with tabs[0]:
    secilen.extend(st.multiselect("Sistemik Bulgular", ["Yüksek Ateş", "Halsizlik", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Lenfadenopati", "Yaygın Kaşıntı", "Titreme", "Anoreksiya"]))
with tabs[1]:
    secilen.extend(st.multiselect("Torasik Bulgular", ["Göğüs Ağrısı (Baskı Tarzı)", "Göğüs Ağrısı (Batıcı)", "Nefes Darlığı (Dispne)", "Çarpıntı", "Senkop (Bayılma)", "Hemoptizi", "Öksürük", "Ortopne"]))
with tabs[2]:
    secilen.extend(st.multiselect("GİS Bulguları", ["Karın Ağrısı (Sağ Alt Kadran)", "Epigastrik Ağrı", "Melena (Siyah Dışkı)", "Hematemez (Kanlı Kusma)", "Sarılık (İkter)", "Diyare", "Kusma", "Karında Şişkinlik"]))
with tabs[3]:
    secilen.extend(st.multiselect("Nörolojik Bulgular", ["Şiddetli Baş Ağrısı", "Baş Dönmesi (Vertigo)", "Konfüzyon/Bilinç Bulanıklığı", "Fokal Güç Kaybı", "Dizartri (Peltak Konuşma)", "Nöbet (Seizure)", "Ense Sertliği"]))
with tabs[4]:
    secilen.extend(st.multiselect("Endokrin ve Üriner", ["Dizüri (Yanmalı İdrar)", "Hematüri (Kanlı İdrar)", "Oligüri (Az İdrar)", "Poliüri/Polidipsi", "Aseton Kokusu", "Flank (Böğür) Ağrısı"]))
with tabs[5]:
    secilen.extend(st.multiselect("Özel Klinik Bulgular", ["Kelebek Döküntü (Malar Rash)", "Sabah Sertliği (>30 dk)", "Eklem Şişliği", "Peteşi/Purpura", "Splenomegali", "Konjonktival Solukluk", "Raynaud Fenomeni"]))

# 7. Gelişmiş Karar Algoritması
def analiz_et(s, a, ts, n):
    res = {"tanilar": [], "tetkikler": [], "acil": ""}
    ss = set(s)
    
    # Kardiyak & Pulmoner Aciller
    if {"Göğüs Ağrısı (Baskı Tarzı)", "Nefes Darlığı (Dispne)", "Senkop (Bayılma)"}.intersection(ss):
        res["tanilar"].extend(["Akut Koroner Sendrom", "Pulmoner Emboli", "Aort Diseksiyonu"])
        res["tetkikler"].extend(["EKG (12 Derivasyonlu)", "Kardiyak Troponin I/T", "D-Dimer", "PAAC Grafisi", "Ekokardiyografi"])
        res["acil"] = "Kardiyak Acil Şüphesi! Derhal monitörize edilmelidir."

    # Akut Batın & GİS Kanama
    if {"Karın Ağrısı (Sağ Alt Kadran)", "Melena (Siyah Dışkı)", "Hematemez (Kanlı Kusma)"}.intersection(ss):
        res["tanilar"].extend(["Akut Apandisit", "GİS Kanama", "Mezenter İskemi", "Perforasyon"])
        res["tetkikler"].extend(["Kontrastlı Batın BT", "Hemogram (Seri Takip)", "Üst/Alt GİS Endoskopisi", "ADBG", "Laktat"])
        if "Melena (Siyah Dışkı)" in ss or "Hematemez (Kanlı Kusma)" in ss:
            res["acil"] = "Aktif GİS Kanaması! Acil cerrahi/gastroenteroloji konsültasyonu ve IV sıvı desteği."

    # Sepsis Taraması (qSOFA benzeri)
    if a > 38.5 and ts < 100:
        res["tanilar"].append("Sepsis / Septik Şok")
        res["tetkikler"].extend(["Kan Kültürü (x2)", "Prokalsitonin", "Laktat", "İdrar Kültürü"])
        res["acil"] = "Sepsis Riski! Erken antibiyoterapi ve laktat takibi hayati önem taşır."

    # Romatoloji - Lupus/RA
    if {"Kelebek Döküntü (Malar Rash)", "Sabah Sertliği (>30 dk)", "Eklem Şişliği"}.intersection(ss):
        res["tanilar"].extend(["Sistemik Lupus Eritematozus (SLE)", "Romatoid Artrit"])
        res["tetkikler"].extend(["ANA Paneli", "Anti-dsDNA", "RF", "Anti-CCP", "Sedimantasyon/CRP"])

    # Diyabetik Aciller
    if "Aseton Kokusu" in ss or (ts > 250 and "Poliüri/Polidipsi" in ss):
        res["tanilar"].append("Diyabetik Ketoasidoz (DKA) / HHS")
        res["tetkikler"].extend(["Venöz Kan Gazı", "Kan Şekeri Takibi", "İdrar Ketonu", "Elektrolit Paneli"])

    return res

# 8. Analiz ve Yan Yana Görüntüleme
st.markdown("<br>", unsafe_allow_html=True)
if st.button("KLİNİK ANALİZİ BAŞLAT VE GEMINI'YE SORGULA"):
    if not secilen:
        st.error("⚠️ Analiz için lütfen en az bir belirti seçiniz.")
    else:
        # Manuel Algoritma Çalıştırma
        sonuc = analiz_et(secilen, ates, ta_s, nabiz)
        
        # Acil Durum Mesajı
        if sonuc["acil"]:
            st.markdown(f"<div class='status-box critical-alert'>🚨 **KRİTİK UYARI:** {sonuc['acil']}</div>", unsafe_allow_html=True)
        
        # Yan Yana Sütunlar
        col_sol, col_sag = st.columns(2)
        
        with col_sol:
            st.subheader("📋 Diferansiyel Tanılar & Önerilen Tetkikler")
            st.write("**Olası Ön Tanılar:**")
            t_set = set(sonuc["tanilar"] if sonuc["tanilar"] else ["Genel Dahili Değerlendirme"])
            for t in t_set: st.write(f"- {t}")
            
            st.write("**İstenmesi Gereken İleri Tetkikler:**")
            # Hata çözümü: Değişken adı çakışmasını önlemek için 'nihai_tetkikler' kullanıldı
            nihai_tetkikler = set(sonuc["tetkikler"] if sonuc["tetkikler"] else ["Hemogram", "CRP", "Geniş Biyokimya Paneli", "TİT"])
            for tetkik in nihai_tetkikler:
                st.write(f"🧪 {tetkik}")
        
        with col_sag:
            st.subheader("🤖 Gemini AI Klinik Akıl Yürütme")
            try:
                # Prompt Zenginleştirme
                v_ozet = f"Yaş:{yas}, Cinsiyet:{cinsiyet}, Ateş:{ates}, TA:{ta_s}/{ta_d}, Nabız:{nabiz}, SpO2:{spo2}"
                prompt =
