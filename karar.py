import streamlit as st

# 1. Sayfa Ayarları ve Ultra Modern Görünüm (Geri Getirildi ve Geliştirildi)
st.set_page_config(page_title="Dahiliye CDSS", page_icon="⚕️", layout="wide")

st.markdown("""
    <style>
    /* Genel Arka Plan ve Yazı Tipi */
    .stApp { background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Sekme (Tab) Tasarımı */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        font-size: 15px; font-weight: 700; padding: 12px 20px; 
        border-radius: 12px 12px 0 0; background-color: #e2e8f0; color: #475569; border: none;
    }
    .stTabs [aria-selected="true"] { background-color: #1e3a8a !important; color: white !important; box-shadow: 0 -4px 10px rgba(0,0,0,0.1); }
    
    /* Kart Tasarımları (Ön Tanı ve Tetkikler İçin) */
    .diagnose-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-left: 8px solid #dc2626; box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        height: 100%; transition: transform 0.3s ease;
    }
    .diagnose-card:hover { transform: translateY(-5px); }
    
    .test-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-left: 8px solid #059669; box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        height: 100%; transition: transform 0.3s ease;
    }
    .test-card:hover { transform: translateY(-5px); }
    
    /* Buton Tasarımı */
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; border: none; border-radius: 12px; height: 3.5em;
        font-weight: 800; font-size: 16px; width: 100%; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { box-shadow: 0 8px 25px rgba(59,130,246,0.5); transform: translateY(-2px); }
    
    /* Başlık */
    h1 { color: #1e3a8a; text-align: center; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Dahiliye Klinik Karar Destek Asistanı")
st.markdown("<p style='text-align: center; font-size: 1.3em; color: #475569;'><b>Sürüm: 8.0 (Geliştirici: İSMAİL ORHAN)</b></p>", unsafe_allow_html=True)
st.divider()

# 3. Sidebar: Vital Bulgular (Diyabet ve Detaylı Vitaller)
with st.sidebar:
    st.header("📋 Hasta Vitalleri")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    st.divider()
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    nabiz = st.number_input("Nabız (atım/dk)", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 40, 100, 98)
    kan_sekeri = st.number_input("Açlık/Anlık Kan Şekeri (mg/dL)", 20, 1000, 100)
    
    if kan_sekeri > 250: st.error("🚨 Kritik Hiperglisemi!")
    elif kan_sekeri < 60: st.error("🚨 Kritik Hipoglisemi!")
    if ta_sis > 180 or ta_dia > 120: st.error("🚨 Hipertansif Acil Şüphesi!")
    if spo2 < 90: st.warning("⚠️ Hipoksi!")

# 4. Devasa Semptom Paneli (Kitaplık Gibi Genişletildi)
st.subheader("🔍 Kapsamlı Klinik Bulgular (Dahiliye Tüm Branşlar)")
t_gis, t_kardiyo, t_noroloji, t_romatoloji, t_endokrin, t_enfeksiyon = st.tabs([
    "🩺 GİS & Hepatobilier", "🫁 Kardiyoloji & Göğüs", "🧠 Nöroloji", "🦋 Romatoloji", "🧪 Endokrin & Nefroloji", "🧬 Hematoloji & Enfeksiyon"
])

secilen = []
with t_gis:
    c1, c2, c3 = st.columns(3)
    with c1: secilen.extend(st.multiselect("Üst GİS", ["Hematemez", "Melena", "Disfaji", "Epigastrik Ağrı", "Pirozis (Mide Yanması)", "İnatçı Hıçkırık", "Erken Doyma"]))
    with c2: secilen.extend(st.multiselect("Alt GİS", ["Sağ Alt Kadran Ağrısı", "Hematokezya", "Tenezm", "Steatore (Yağlı Dışkı)", "Sol Alt Kadran Ağrısı", "Kupür/Rebound"]))
    with c3: secilen.extend(st.multiselect("Hepatobilier", ["Sarılık", "Asit", "Biliyer Kolik Ağrısı", "Akoli (Renksiz Dışkı)", "Safra Kusma", "Hepatomegali"]))

with t_kardiyo:
    c4, c5 = st.columns(2)
    with c4: secilen.extend(st.multiselect("Kardiyovasküler", ["Baskı Tarzı Göğüs Ağrısı", "Çarpıntı", "Senkop", "PND (Gece Nefes Darlığı)", "Kardiyak Üfürüm", "S3/S4 Galo Ritmi", "Pulsus Paradoksus", "Boyun Ven Dolgunluğu"]))
    with c5: secilen.extend(st.multiselect("Pulmoner", ["Efor Dispnesi", "Hemoptizi", "Plevritik Ağrı", "Wheezing (Hışıltı)", "Stridor", "Çomak Parmak", "Prodüktif Öksürük", "Siyanoz"]))

with t_noroloji:
    c6, c7 = st.columns(2)
    with c6: secilen.extend(st.multiselect("Santral", ["Ani ve Çok Şiddetli Baş Ağrısı", "Konfüzyon/Deliryum", "Ense Sertliği", "Fokal Güç Kaybı", "Afazi (Konuşma Bozukluğu)"]))
    with c7: secilen.extend(st.multiselect("Kranial & Periferik", ["Fasiyal Asimetri (Yüz Kayması)", "Dizartri", "Diplopi (Çift Görme)", "Nistagmus", "Ataksi", "Eldiven-Çorap Tarzı Uyuşma"]))

with t_romatoloji:
    c8, c9 = st.columns(2)
    with c8: secilen.extend(st.multiselect("Artrit & Bağ Doku", ["Sabah Sertliği (>1 Saat)", "Poliartrit (Simetrik)", "Monoartrit (Akut Şişlik)", "Kelebek Döküntü", "Raynaud Fenomeni"]))
    with c9: secilen.extend(st.multiselect("Özel Romatolojik Bulgular", ["Helitrop Raş / Gottron Papülleri", "Bambu Kamışı Omurga (Sertlik)", "Oral/Genital Aft", "Kuru Göz / Kuru Ağız (Sikca)", "Eritema Nodosum"]))

with t_endokrin:
    c10, c11 = st.columns(2)
    with c10: secilen.extend(st.multiselect("Endokrinoloji", ["Poliüri/Polidipsi", "Aseton Kokusu", "Aydede Yüzü / Buffalo Hörgücü", "Mor Stria", "Mukozal Hiperpigmentasyon", "Makroglosi", "Ekzoftalmi", "Sıcak/Soğuk İntoleransı"]))
    with c11: secilen.extend(st.multiselect("Nefroloji", ["Oligüri / Anüri", "Hematüri (Makroskopik)", "Köpüklü İdrar (Proteinüri)", "Kostavertebral Açı Hassasiyeti", "Flank Ağrısı (Böğür)", "Pretibial Ödem"]))

with t_enfeksiyon:
    c12, c13 = st.columns(2)
    with c12: secilen.extend(st.multiselect("Enfeksiyon & Sistemik", ["Gece Terlemesi (Sırılsıklam)", "İstemsiz Kilo Kaybı", "Pel-Ebstein Ateşi", "Jeneralize Lenfadenopati"]))
    with c13: secilen.extend(st.multiselect("Hematoloji", ["Peteşi / Ekimoz / Purpura", "Splenomegali", "Sürekli Enfeksiyon (Nötropeni)", "Pika (Toprak Yeme İsteği)", "Koilonişi (Kaşık Tırnak)"]))

# 5. DEVASA İÇ MOTOR (Algoritma)
def tam_kapsamli_motor(bulgular, vitaller):
    t_list, tet_list = set(), set(["Tam Kan Sayımı (Hemogram)", "Biyokimya (AST, ALT, BUN, Cre, Na, K)", "CRP"])
    b = set(bulgular)
    ates, ta_sis, spo2, seker = vitaller

    # --- ENDOKRİNOLOJİ ---
    if seker > 250 and "Aseton Kokusu" in b:
        t_list.add("Diyabetik Ketoasidoz (DKA)")
        tet_list.update(["Arteriyel/Venöz Kan Gazı", "İdrarda Keton", "Serum Osmolalitesi"])
    if "Mor Stria" in b or "Aydede Yüzü / Buffalo Hörgücü" in b:
        t_list.add("Cushing Sendromu")
        tet_list.update(["1 mg Deksametazon Süpresyon Testi", "24 Saatlik İdrarda Serbest Kortizol", "ACTH Düzeyi"])
    if "Mukozal Hiperpigmentasyon" in b:
        t_list.add("Addison Hastalığı (Primer Adrenal Yetmezlik)")
        tet_list.update(["Sabah Kortizolü", "ACTH Stimülasyon Testi"])
    if "Ekzoftalmi" in b and "Sıcak/Soğuk İntoleransı" in b:
        t_list.add("Hipertiroidi / Graves Hastalığı")
        tet_list.update(["TSH, sT3, sT4", "TSH Reseptör Antikoru (TRAb)", "Tiroid USG"])

    # --- KARDİYOLOJİ & GÖĞÜS ---
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        t_list.add("Akut Koroner Sendrom (STEMI / NSTEMI)")
        tet_list.update(["12 Derivasyonlu EKG", "Seri Troponin I/T", "Ekokardiyografi"])
    if "Efor Dispnesi" in b and ("PND (Gece Nefes Darlığı)" in b or "S3/S4 Galo Ritmi" in b):
        t_list.add("Kalp Yetmezliği (KKY)")
        tet_list.update(["NT-proBNP", "Telekardiyogram", "Ekokardiyografi"])
    if "Plevritik Ağrı" in b and "Hemoptizi" in b and spo2 < 94:
        t_list.add("Pulmoner Emboli")
        tet_list.update(["D-Dimer", "Toraks BT Anjiografi (CTPA)", "Venöz Doppler USG"])
    
    # --- GİS & HEPATOBİLİER ---
    if "Biliyer Kolik Ağrısı" in b and "Sarılık" in b and ates > 38.0:
        t_list.add("Akut Kolanjit (Charcot Triadı)")
        tet_list.update(["Tüm Batın USG", "Bilirubin (Direkt/Total)", "ERCP / MRCP"])
    if "Hematemez" in b or "Melena" in b:
        t_list.add("Üst GİS Kanama (Ülser veya Varis)")
        tet_list.update(["Acil Üst GİS Endoskopisi", "Kan Grubu ve Cross-Match", "INR/PTT"])
    if "Sol Alt Kadran Ağrısı" in b and ates > 37.5:
        t_list.add("Akut Divertikülit")
        tet_list.update(["Kontrastlı Batın BT"])

    # --- ROMATOLOJİ ---
    if "Kelebek Döküntü" in b:
        t_list.add("Sistemik Lupus Eritematozus (SLE)")
        tet_list.update(["ANA, Anti-dsDNA, Anti-Sm", "Kompleman (C3, C4)", "Tam İdrar Tetkiki (Lupus Nefriti İçin)"])
    if "Helitrop Raş / Gottron Papülleri" in b:
        t_list.add("Dermatomiyozit")
        tet_list.update(["Kreatin Kinaz (CK)", "LDH", "Kas Biyopsisi", "EMG"])
    if "Bambu Kamışı Omurga (Sertlik)" in b:
        t_list.add("Ankilozan Spondilit")
        tet_list.update(["HLA-B27", "Sakroiliak Eklem MR", "AP Pelvis Grafisi"])

    # --- NÖROLOJİ ---
    if "Fasiyal Asimetri (Yüz Kayması)" in b and ("Fokal Güç Kaybı" in b or "Afazi (Konuşma Bozukluğu)" in b):
        t_list.add("Akut İskemik İnme / SVO")
        tet_list.update(["Acil Kontrastsız Beyin BT", "Difüzyon MR", "Karotis Doppler USG"])
    if "Ani ve Çok Şiddetli Baş Ağrısı" in b and "Ense Sertliği" in b:
        t_list.add("Subaraknoid Kanama (SAK) veya Menenjit")
        tet_list.update(["Beyin BT", "Lomber Ponksiyon (BOS Analizi)"])

    # --- NEFROLOJİ & HEMATOLOJİ ---
    if "Köpüklü İdrar (Proteinüri)" in b and "Pretibial Ödem" in b:
        t_list.add("Nefrotik Sendrom")
        tet_list.update(["24 Saatlik İdrarda Protein", "Serum Albümin", "Lipid Profili"])
    if "Kostavertebral Açı Hassasiyeti" in b and ates > 38.0:
        t_list.add("Akut Piyelonefrit")
        tet_list.update(["Tam İdrar Tetkiki", "İdrar Kültürü", "Üriner Sistem USG"])
    if "Peteşi / Ekimoz / Purpura" in b:
        t_list.add("Trombositopeni / Kanama Diatezi / Lösemi Şüphesi")
        tet_list.update(["Periferik Yayma (Formül Lökosit)", "PT/aPTT/INR", "Kemik İliği Biyopsisi Düşün"])

    return sorted(list(t_list)), sorted(list(tet_list))

# 6. Analiz Tetikleme ve Modern Rapor
st.markdown("<br>", unsafe_allow_html=True)
if st.button("TIBBİ ALGORİTMAYI ÇALIŞTIR VE RAPORLA"):
    if not secilen and kan_sekeri == 100 and ates == 36.6 and ta_sis == 120:
        st.warning("⚠️ Lütfen en az bir klinik bulgu seçiniz veya vitalleri anormal değerlere ayarlayınız.")
    else:
        vitaller = (ates, ta_sis, spo2, kan_sekeri)
        tanilar, tetkikler = tam_kapsamli_motor(secilen, vitaller)
        
        st.markdown("### 🏥 Kapsamlı Klinik Karar Raporu")
        r1, r2 = st.columns(2)
        
        with r1:
            st.markdown("<div class='diagnose-card'>", unsafe_allow_html=True)
            st.subheader("📋 Diferansiyel Tanılar (Düşünülmesi Gerekenler)")
            if tanilar:
                for t in tanilar: st.markdown(f"**🚨 {t}**")
            else: 
                st.info("💡 Seçilen bulgular spesifik bir sendroma işaret etmedi. Rutin dahiliye poliklinik değerlendirmesi önerilir.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with r2:
            st.markdown("<div class='test-card'>", unsafe_allow_html=True)
            st.subheader("🧪 İstenmesi Gereken Klinik Tetkikler")
            for tet in tetkikler: st.markdown(f"**🔬 {tet}**")
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Alt Bilgi
st.markdown("---")
st.caption("Dahiliye Klinik Karar Destek Sistemi © 2026 | Tasarım ve Geliştirme: İSMAİL ORHAN | Sadece Profesyonel Tıbbi Kullanım İçindir.")
