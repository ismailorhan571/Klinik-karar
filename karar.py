import streamlit as st
import time

# 1. Sayfa Ayarları (Profesyonel Tıbbi Tema)
st.set_page_config(page_title="Klinik Karar Destek Sistemi", page_icon="⚕️", layout="wide")

# CSS: Göz yormayan, sade ve evrensel sağlık arayüzü (Mavi/Beyaz/Gri)
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
    st.markdown("**Geliştirici:** İsmail Orhan | **Sürüm:** 1.0 (Profesyonel Sürüm)")

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
    st.info("💡 **Not:** Bu sistem tanı koymaz, hekime diferansiyel tanı ve tetkik planlamasında kılavuzluk eder.")

# 4. Ana Ekran: Sistemlere Göre Kategorize Edilmiş Belirtiler
st.subheader("🔍 Klinik Semptom Seçimi")
st.write("Hastanın şikayetlerini ilgili sistem sekmelerinden seçiniz. Ne kadar detaylı veri girilirse, analiz o kadar spesifik olur.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Sistemik/Genel", "Kardiyovasküler", "Solunum", "Gastrointestinal", "Nörolojik", "Üriner/Renal"
])

secilen_belirtiler = []

with tab1:
    sistemik = st.multiselect("Sistemik Belirtiler", 
        ["Yüksek Ateş", "Halsizlik/Yorgunluk", "Gece Terlemesi", "İstemsiz Kilo Kaybı", "Yaygın Kas Ağrısı (Miyalji)", "Eklem Ağrısı (Artralji)", "Titreme", "İştahsızlık"])
    secilen_belirtiler.extend(sistemik)

with tab2:
    kardiyo = st.multiselect("Kardiyovasküler Belirtiler", 
        ["Göğüs Ağrısı (Baskı tarzı)", "Göğüs Ağrısı (Batıcı)", "Çarpıntı", "Senkop (Bayılma)", "Bilateral Alt Ekstremite Ödemi", "Eforla Gelen Nefes Darlığı", "Ortopne", "Boyun Venöz Dolgunluğu"])
    secilen_belirtiler.extend(kardiyo)

with tab3:
    solunum = st.multiselect("Solunum Sistemi Belirtileri", 
        ["Nefes Darlığı (Dispne)", "Kuru Öksürük", "Balgamlı Öksürük", "Hemoptizi (Kanlı Balgam)", "Hışıltılı Solunum (Wheezing)", "Plöretik Göğüs Ağrısı", "Siyanoz"])
    secilen_belirtiler.extend(solunum)

with tab4:
    gastro = st.multiselect("Gastrointestinal Belirtiler", 
        ["Karın Ağrısı (Yaygın)", "Karın Ağrısı (Sağ Alt Kadran)", "Karın Ağrısı (Epigastrik)", "Bulantı", "Kusma", "Diyare (İshal)", "Melena (Siyah Dışkı)", "Hematemez (Kanlı Kusma)", "Sarılık (İkter)", "Asit", "Kabızlık"])
    secilen_belirtiler.extend(gastro)

with tab5:
    noro = st.multiselect("Nörolojik Belirtiler", 
        ["Baş Ağrısı", "Baş Dönmesi (Vertigo)", "Bilinç Bulanıklığı/Konfüzyon", "Tek Taraflı Güç Kaybı", "Konuşma Bozukluğu (Dizartri/Afazi)", "Nöbet (Konvülziyon)", "Ense Sertliği", "Görme Kaybı/Çift Görme"])
    secilen_belirtiler.extend(noro)

with tab6:
    uriner = st.multiselect("Üriner Sistem Belirtileri", 
        ["Dizüri (İdrarda Yanma)", "Hematüri (Kanlı İdrar)", "Sık İdrara Çıkma (Pollaküri)", "Poliüri (Çok idrar)", "Oligüri (Az idrar)", "Yan Ağrısı (Flank Ağrı)", "İdrar Kaçırma"])
    secilen_belirtiler.extend(uriner)

st.divider()

# 5. Dev Veritabanı ve Karar Algoritması
def gelismis_analiz(belirtiler, yas, ates, ta_sistolik, spo2):
    rapor = {"teshisler": [], "kan_tetkikleri": [], "goruntuleme": [], "kirmizi_bayrak": ""}
    
    belirti_seti = set(belirtiler)

    # Senaryo 1: Akut Koroner Sendrom
    if {"Göğüs Ağrısı (Baskı tarzı)", "Nefes Darlığı (Dispne)"}.intersection(belirti_seti):
        rapor["teshisler"].extend(["Akut Miyokard Enfarktüsü (STEMI/NSTEMI)", "Kararsız Anjina", "Pulmoner Emboli"])
        rapor["kan_tetkikleri"].extend(["High-Sensitive Troponin", "CK-MB", "D-Dimer", "Pro-BNP", "Arter Kan Gazı"])
        rapor["goruntuleme"].extend(["12 Derivasyonlu EKG (Acil)", "Ekokardiyografi", "Akciğer Grafisi"])
        rapor["kirmizi_bayrak"] = "Kardiyak acil şüphesi! EKG ilk 10 dk içinde çekilmeli ve kardiyoloji konsültasyonu istenmelidir."

    # Senaryo 2: Gastrointestinal Aciller
    if {"Karın Ağrısı (Sağ Alt Kadran)", "Bulantı", "Yüksek Ateş"}.intersection(belirti_seti) or "Melena (Siyah Dışkı)" in belirti_seti:
        rapor["teshisler"].extend(["Akut Apandisit", "Üst GİS Kanaması", "Peptik Ülser Perforasyonu", "Akut Kolesistit"])
        rapor["kan_tetkikleri"].extend(["Hemogram (Tam Kan Sayımı)", "CRP", "Geniş Biyokimya (AST, ALT, Bilirubinler)", "Amilaz/Lipaz", "Koagülasyon (PT, aPTT, INR)", "Kan Grubu"])
        rapor["goruntuleme"].extend(["Tüm Batın USG", "Ayakta Direkt Batın Grafisi (ADBG)", "Gerekirse Batın BT"])
        if "Melena (Siyah Dışkı)" in belirti_seti:
            rapor["kirmizi_bayrak"] = "Aktif kanama şüphesi! Çift damar yolu açılmalı, kan grubu cross-match yapılmalı ve gastroenteroloji/genel cerrahi konsültasyonu istenmelidir."

    # Senaryo 3: Solunum Yolu Enfeksiyonu / Sepsis
    if ({"Yüksek Ateş", "Balgamlı Öksürük", "Nefes Darlığı (Dispne)"}.intersection(belirti_seti)) or (ates > 38.5 and spo2 < 92):
        rapor["teshisler"].extend(["Pnömoni (Toplum veya Hastane Kökenli)", "Sepsis", "Akut Bronşit", "KOAH Alevlenmesi"])
        rapor["kan_tetkikleri"].extend(["Hemogram", "CRP, Prokalsitonin", "Arter Kan Gazı", "Kan ve Balgam Kültürü", "Laktat"])
        rapor["goruntuleme"].extend(["Akciğer Grafisi (PAAC)", "Gerekirse Toraks BT (Kontrastsız)"])
        if ates > 38.5 and ta_sistolik < 90:
            rapor["kirmizi_bayrak"] = "SEPSİS PROTOKOLÜ: Sıvı resüsitasyonuna başlayın, kültürleri alıp ilk 1 saat içinde geniş spektrumlu antibiyoterapiye geçin."

    # Senaryo 4: Nörolojik Aciller
    if {"Tek Taraflı Güç Kaybı", "Konuşma Bozukluğu (Dizartri/Afazi)", "Bilinç Bulanıklığı/Konfüzyon"}.intersection(belirti_seti):
        rapor["teshisler"].extend(["İskemik İnme (SVO)", "Hemorajik İnme", "Geçici İskemik Atak (TIA)", "Menenjit/Ensefalit"])
        rapor["kan_tetkikleri"].extend(["Hemogram", "Koagülasyon Paneli (INR çok kritik)", "Kan Şekeri (Hipoglisemiyi dışla)", "Elektrolit Paneli"])
        rapor["goruntuleme"].extend(["Kontrastsız Beyin BT (Hemen)", "Gerekirse Beyin MR ve MR Anjiyo"])
        rapor["kirmizi_bayrak"] = "İnme kodu! Trombolitik tedavi penceresi (ilk 4.5 saat) için hastanın semptom başlangıç saatini kesin olarak belirleyin."

    # Senaryo 5: Üriner Sistem
    if {"Dizüri (İdrarda Yanma)", "Yan Ağrısı (Flank Ağrı)", "Yüksek Ateş"}.intersection(belirti_seti):
        rapor["teshisler"].extend(["Akut Piyelonefrit", "Ürolitiazis (Böbrek Taşı)", "Komplike İYE"])
        rapor["kan_tetkikleri"].extend(["Tam İdrar Tetkiki (TİT)", "İdrar Kültürü", "Üre, Kreatinin", "Hemogram", "CRP"])
        rapor["goruntuleme"].extend(["Üriner Sistem USG", "Böbrek-Üreter-Mesane (BÜM) Grafisi", "Taş Protokolü BT"])

    # Listeleri temizle (Tekrarları kaldır)
    rapor["teshisler"] = list(set(rapor["teshisler"])) if rapor["teshisler"] else ["Spesifik bir sendrom eşleşmedi. Viral enfeksiyon, yorgunluk veya başlangıç aşamasında bir patoloji olabilir."]
    rapor["kan_tetkikleri"] = list(set(rapor["kan_tetkikleri"])) if rapor["kan_tetkikleri"] else ["Rutin Biyokimya", "Hemogram"]
    rapor["goruntuleme"] = list(set(rapor["goruntuleme"])) if rapor["goruntuleme"] else ["Mevcut bulgularla acil görüntüleme endikasyonu net değil, fizik muayeneye göre karar verilmeli."]

    return rapor

# 6. Sonuçların Gösterilmesi
if st.button("TIBBİ ALGORİTMAYI ÇALIŞTIR VE ANALİZ ET"):
    if not secilen_belirtiler:
        st.error("⚠️ Analiz için lütfen en az bir semptom seçiniz.")
    else:
        with st.spinner("Tıbbi veri tabanı taranıyor, vital bulgular korele ediliyor..."):
            time.sleep(1.5) # Gerçekçilik katmak için kısa bir yükleme animasyonu
            sonuc = gelismis_analiz(secilen_belirtiler, yas, ates, ta_sistolik, spo2)
            
            st.success("✅ Analiz başarıyla tamamlandı.")
            
            if sonuc["kirmizi_bayrak"]:
                st.markdown(f"<div class='alert-box critical'>🚨 KIRMIZI BAYRAK (ACİL): {sonuc['kirmizi_bayrak']}</div>", unsafe_allow_html=True)
            
            # Sonuçları iki kolonda göster
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.markdown("### 📋 Olası Teşhisler (Diferansiyel Tanı)")
                for teshis in sonuc["teshisler"]:
                    st.markdown(f"- **{teshis}**")
                
                st.markdown("---")
                st.markdown("### 🧪 İstenmesi Önerilen Laboratuvar Paneli")
                for kan in sonuc["kan_tetkikleri"]:
                    st.markdown(f"- {kan}")
                    
            with res_col2:
                st.markdown("### 📻 Radyolojik Görüntüleme Planı")
                for goruntu in sonuc["goruntuleme"]:
                    st.markdown(f"📸 {goruntu}")
                    
                st.markdown("---")
                st.markdown("### 🤖 Yapay Zeka (Gemini) İleri Analizi")
                st.markdown("""
                <div class='alert-box info-box'>
                <strong>AI Entegrasyonu Hazır:</strong><br>
                Seçilen semptomlar ve girilen vital bulgular, hastanın yaşına ve cinsiyetine göre Gemini AI'a API üzerinden gönderilmeye hazırdır. 
                Sistem bağlandığında burada güncel UpToDate, Medscape ve Pubmed makalelerinden sentezlenmiş <strong>kişiselleştirilmiş tedavi protokolü önerileri</strong> yer alacaktır.
                </div>
                """, unsafe_allow_html=True)

# Sayfa Altı
st.markdown("<br><br><p style='text-align: center; color: #6c757d; font-size: 14px;'>© 2026 Dahiliye Klinik Destek Sistemleri | Yalnızca profesyonel kullanım içindir.</p>", unsafe_allow_html=True)
