import streamlit as st
import time
import google.generativeai as genai

# 1. Sayfa Ayarları (Senin orijinal ayarların)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# Gemini API Yapılandırması (404 hatasını çözen stabil versiyon)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Model ismi güncellendi: 'gemini-1.5-flash' en stabil olanıdır.
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ API Anahtarı eksik! Streamlit Secrets kısmına GEMINI_API_KEY ekleyin.")

# CSS: Senin orijinal tıbbi teman
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

# 2. Üst Bilgi Alanı
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("<h1 style='text-align: center; font-size: 50px; border: none;'>⚕️</h1>", unsafe_allow_html=True)
with col2:
    st.title("Gelişmiş Klinik Karar Destek Sistemi (CDSS)")
    st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.0 (Gemini Entegre)")

st.divider()

# 3. Sol Menü: Vital Bulgular ve Hasta Profili
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

# 4. Ana Ekran: Tüm orijinal kategorilerin
st.subheader("🔍 Klinik Semptom Seçimi")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Sistemik/Genel", "Kardiyovasküler", "Solunum", "Gastrointestinal", "Nörolojik", "Üriner/Renal"
])

secilen_belirtiler = []

with tab1:
    sistemik = st.multiselect("Sistemik Belirtiler", ["Yüksek Ateş", "Halsizlik/Yorgunluk", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Yaygın Kas Ağrısı (Miyalji)", "Eklem Ağrısı (Artralji)", "Titreme", "İştahsızlık"])
    secilen_belirtiler.extend(sistemik)
with tab2:
    kardiyo = st.multiselect("Kardiyovasküler Belirtiler", ["Göğüs Ağrısı (Baskı tarzı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop (Bayılma)", "Bilateral Alt Ekstremite Ödemi", "Eforla Gelen Nefes Darlığı", "Ortopne", "Boyun Venöz Dolgunluğu"])
    secilen_belirtiler.extend(kardiyo)
with tab3:
    solunum = st.multiselect("Solunum Sistemi Belirtileri", ["Nefes Darlığı (Dispne)", "Kuru Öksürük", "Balgamlı Öksürük", "Hemoptizi (Kanlı Balgam)", "Hışıltılı Solunum (Wheezing)", "Plöretik Göğüs Ağrısı", "Siyanoz"])
    secilen_belirtiler.extend(solunum)
with tab4:
    gastro = st.multiselect("Gastrointestinal Belirtiler", ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Sağ Alt Kadran)", "Karın Ağrısı (Epigastrik)", "Bulantı", "Kusma", "Diyare (İshal)", "Melena (Siyah Dışkı)", "Hematemez (Kanlı Kusma)", "Sarılık (İkter)", "Asit", "Kabızlık"])
    secilen_belirtiler.extend(gastro)
with tab5:
    noro = st.multiselect("Nörolojik Belirtiler", ["Baş Ağrısı", "Baş Dönmesi (Vertigo)", "Bilinç Bulanıklığı/Konfüzyon", "Tek Taraflı Güç Kaybı", "Konuşma Bozukluğu (Dizartri/Afazi)", "Nöbet (Konvülziyon)", "Ense Sertliği", "Görme Kaybı/Çift Görme"])
    secilen_belirtiler.extend(noro)
with tab6:
    uriner = st.multiselect("Üriner Sistem Belirtileri", ["Dizüri (İdrarda Yanma)", "Hematüri (Kanlı İdrar)", "Sık İdrara Çıkma (Pollaküri)", "Poliüri (Çok idrar)", "Oligüri (Az idrar)", "Yan Ağrısı (Flank Ağrı)", "İdrar Kaçırma"])
    secilen_belirtiler.extend(uriner)

# 5. Senin Orijinal Karar Algoritman (Dokunulmadı)
def gelismis_analiz(belirtiler, yas, ates, ta_sistolik, spo2):
    rapor = {"teshisler": [], "kan_tetkikleri": [], "goruntuleme": [], "kirmizi_bayrak": ""}
    belirti_seti = set(belirtiler)

    if {"Göğüs Ağrısı (Baskı tarzı)", "Nefes Darlığı (Dispne)"}.intersection(belirti_seti):
        rapor["teshisler"].extend(["Akut Miyokard Enfarktüsü (STEMI/NSTEMI)", "Kararsız Anjina", "Pulmoner Emboli"])
        rapor["kan_tetkikleri"].extend(["High-Sensitive Troponin", "CK-MB", "D-Dimer", "Pro-BNP", "Arter Kan Gazı"])
        rapor["goruntuleme"].extend(["12 Derivasyonlu EKG (Acil)", "Ekokardiyografi", "Akciğer Grafisi"])
        rapor["kirmizi_bayrak"] = "Kardiyak acil şüphesi! EKG ilk 10 dk içinde çekilmeli ve kardiyoloji konsültasyonu istenmelidir."

    if {"Karın Ağrısı (Sağ Alt Kadran)", "Bulantı", "Yüksek Ateş"}.intersection(belirti_seti) or "Melena (Siyah Dışkı)" in belirti_seti:
        rapor["teshisler"].extend(["Akut Apandisit", "Üst GİS Kanaması", "Peptik Ülser Perforasyonu", "Akut Kolesistit"])
        rapor["kan_tetkikleri"].extend(["Hemogram", "CRP", "Geniş Biyokimya (AST, ALT, Bilirubinler)", "Amilaz/Lipaz", "Koagülasyon (PT, aPTT, INR)", "Kan Grubu"])
        rapor["goruntuleme"].extend(["Tüm Batın USG", "Ayakta Direkt Batın Grafisi (ADBG)", "Batın BT"])
        if "Melena (Siyah Dışkı)" in belirti_seti:
            rapor["kirmizi_bayrak"] = "Aktif kanama şüphesi! Çift damar yolu açılmalı ve konsültasyon istenmelidir."

    if ({"Yüksek Ateş", "Balgamlı Öksürük", "Nefes Darlığı (Dispne)"}.intersection(belirti_seti)) or (ates > 38.5 and spo2 < 92):
        rapor["teshisler"].extend(["Pnömoni", "Sepsis", "KOAH Alevlenmesi"])
        rapor["kan_tetkikleri"].extend(["Hemogram", "CRP, Prokalsitonin", "Arter Kan Gazı", "Kültürler"])
        rapor["goruntuleme"].extend(["Akciğer Grafisi (PAAC)", "Toraks BT"])

    # Listeleri temizle
    rapor["teshisler"] = list(set(rapor["teshisler"])) if rapor["teshisler"] else ["Spesifik bir sendrom eşleşmedi."]
    rapor["kan_tetkikleri"] = list(set(rapor["kan_tetkikleri"])) if rapor["kan_tetkikleri"] else ["Rutin Biyokimya", "Hemogram"]
    rapor["goruntuleme"] = list(set(rapor["goruntuleme"])) if rapor["goruntuleme"] else ["Fizik muayeneye göre karar verilmeli."]
    return rapor

# Gemini AI Analiz Fonksiyonu
def gemini_ai_analiz(yas, cinsiyet, vitals, belirtiler):
    if "GEMINI_API_KEY" not in st.secrets:
        return "API Anahtarı bulunamadı."
    prompt = f"""
    Sen uzman bir dahiliye klinik destek sistemisin.
    Hasta Bilgileri: {yas} yaşında, {cinsiyet}.
    Vitals: {vitals}.
    Semptomlar: {', '.join(belirtiler)}.
    
    Lütfen bu verileri sentezleyerek; olası ayırıcı tanıları, istenmesi gereken ileri tetkikleri ve güncel tıp literatürüne uygun kısa klinik önerileri profesyonelce açıkla.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Analiz Hatası: {str(e)}"

# 6. Sonuç Ekranı
if st.button("TIBBİ ALGORİTMAYI ÇALIŞTIR VE ANALİZ ET"):
    if not secilen_belirtiler:
        st.error("⚠️ Lütfen belirti seçiniz.")
    else:
        with st.spinner("Analiz ediliyor..."):
            sonuc = gelismis_analiz(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            time.sleep(1)
            
            if sonuc["kirmizi_bayrak"]:
                st.markdown(f"<div class='alert-box critical'>🚨 KIRMIZI BAYRAK: {sonuc['kirmizi_bayrak']}</div>", unsafe_allow_html=True)
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("### 📋 Diferansiyel Tanı ve Tetkikler")
                st.write("**Olası Teşhisler:**")
                for t in sonuc["teshisler"]: st.write(f"- {t}")
                st.write("**Önerilen Laboratuvar:**")
                for k in sonuc["kan_tetkikleri"]: st.write(f"- {k}")
                st.write("**Görüntüleme:**")
                for g in sonuc["goruntuleme"]: st.write(f"- {g}")
                    
            with res_col2:
                st.markdown("### 🤖 Yapay Zeka (Gemini) İleri Analizi")
                v_str = f"Ateş:{ates}, TA:{ta_sistolik}/{ta_diastolik}, Nabız:{nabiz}, SpO2:{spo2}"
                ai_cevap = gemini_ai_analiz(yas, cinsiyet, v_str, secilen_belirtiler)
                st.markdown(f"<div class='alert-box info-box'>{ai_cevap}</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #6c757d; font-size: 14px;'>© 2026 Dahiliye Klinik Destek Sistemleri</p>", unsafe_allow_html=True)
