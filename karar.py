import streamlit as st

# 1. Sayfa Ayarları ve Temiz Klinik Tasarım
st.set_page_config(page_title="Dahiliye CDSS", page_icon="⚕️", layout="wide")

st.markdown("""
    <style>
    /* Temiz, Beyaz, Göz Yormayan Klinik Tema */
    .stApp { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, sans-serif; }
    
    /* Sekmelerin (Tabs) Sadeleşmesi */
    .stTabs [data-baseweb="tab"] { 
        font-size: 15px; font-weight: 600; color: #495057; border: 1px solid #dee2e6; border-bottom: none; border-radius: 8px 8px 0 0; background-color: #e9ecef; margin-right: 2px;
    }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; color: #0d6efd !important; border-top: 3px solid #0d6efd; }
    
    /* Kartların Net ve Ciddi Görünümü */
    .diagnose-card { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; border-left: 6px solid #dc3545; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .test-card { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; border-left: 6px solid #198754; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    
    /* Butonun Profesyonel Hali */
    .stButton>button { background-color: #0d6efd; color: white; border-radius: 6px; font-weight: bold; height: 3em; width: 100%; border: none; font-size: 16px; }
    .stButton>button:hover { background-color: #0b5ed7; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Dahiliye Klinik Karar Destek Asistanı")
st.markdown("<h4 style='text-align: center; color: #6c757d;'>Sürüm: 9.0 (Geliştirici: İSMAİL ORHAN)</h4>", unsafe_allow_html=True)
st.divider()

# 3. Sidebar: Vital Bulgular
with st.sidebar:
    st.header("📋 Vitaller & Profil")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    st.divider()
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    nabiz = st.number_input("Nabız (/dk)", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 40, 100, 98)
    kan_sekeri = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 100)
    
    # Otomatik Uyarılar
    if kan_sekeri > 250: st.error("🚨 Hiperglisemi!")
    elif kan_sekeri < 60: st.error("🚨 Hipoglisemi!")
    if ta_sis > 180 or ta_dia > 120: st.error("🚨 Hipertansif Acil!")

# 4. Devasa Semptom Paneli (Sınırlar Zorlandı)
st.subheader("🔍 Klinik Bulgular (Genişletilmiş Veritabanı)")
t_gis, t_kardiyo, t_noroloji, t_romatoloji, t_endokrin, t_hemato = st.tabs([
    "🩺 GİS", "🫁 Kardiyo & Solunum", "🧠 Nöro & Toksik", "🦋 Romatoloji", "🧪 Endokrin & Nefro", "🧬 Hemato & Onko"
])

secilen = []
with t_gis:
    c1, c2, c3 = st.columns(3)
    with c1: secilen.extend(st.multiselect("Üst GİS", ["Hematemez", "Melena", "Disfaji", "Odinofaji (Yutma Ağrısı)", "Epigastrik Ağrı", "Pirozis", "Erken Doyma"]))
    with c2: secilen.extend(st.multiselect("Alt GİS", ["Sağ Alt Kadran Ağrısı", "Sol Alt Kadran Ağrısı", "Hematokezya", "Tenezm", "Steatore", "Kupür/Rebound"]))
    with c3: secilen.extend(st.multiselect("Hepatobilier", ["Sarılık", "Asit", "Biliyer Kolik", "Akoli (Renksiz Dışkı)", "Safra Kusma", "Hepatomegali"]))

with t_kardiyo:
    c4, c5 = st.columns(2)
    with c4: secilen.extend(st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı (Baskı)", "Çarpıntı", "Senkop", "Tek Taraflı Bacak Şişliği", "Kladikasyo (Yürürken Bacak Ağrısı)", "PND/Ortopne", "Boyun Ven Dolgunluğu"]))
    with c5: secilen.extend(st.multiselect("Pulmoner", ["Efor Dispnesi", "Hemoptizi", "Plevritik Ağrı", "Wheezing (Hışıltı)", "Stridor", "Çomak Parmak", "Prodüktif Öksürük"]))

with t_noroloji:
    c6, c7 = st.columns(2)
    with c6: secilen.extend(st.multiselect("Santral & Periferik", ["Ani Şiddetli Baş Ağrısı", "Konfüzyon", "Ense Sertliği", "Fasiyal Asimetri", "Fokal Güç Kaybı", "Dizartri", "Eldiven-Çorap Uyuşma", "Tremor"]))
    with c7: secilen.extend(st.multiselect("Göz & Toksikoloji", ["Miyozis (İğne Ucu Pupil)", "Midriyazis", "Diplopi", "Nistagmus", "Tükürük Artışı (Hipersalivasyon)"]))

with t_romatoloji:
    c8, c9 = st.columns(2)
    with c8: secilen.extend(st.multiselect("Eklem & Deri", ["Sabah Sertliği (>1 Saat)", "Poliartrit (Simetrik)", "Monoartrit (Akut Şişlik)", "Kelebek Döküntü", "Raynaud Fenomeni"]))
    with c9: secilen.extend(st.multiselect("Sistemik & Özel", ["Oral Aft", "Genital Ülser", "Üveit (Göz Kızarıklığı)", "Gottron Papülleri", "Bambu Omurga", "Kuru Göz/Ağız"]))

with t_endokrin:
    c10, c11 = st.columns(2)
    with c10: secilen.extend(st.multiselect("Endokrin", ["Poliüri/Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Mukozal Hiperpigmentasyon", "Ekzoftalmi", "Galaktore", "Hirsutizm"]))
    with c11: secilen.extend(st.multiselect("Nefroloji", ["Oligüri", "Dizüri/Pollaküri", "Hematüri (Makroskopik)", "Köpüklü İdrar", "Flank Ağrısı (Böğür)", "Üremik Koku"]))

with t_hemato:
    c12, c13 = st.columns(2)
    with c12: secilen.extend(st.multiselect("Hematoloji", ["Solukluk/Derin Anemi", "Pika (Toprak Yeme İsteği)", "Diş Eti Kanaması", "Peteşi/Purpura", "Lenfadenopati", "Splenomegali"]))
    with c13: secilen.extend(st.multiselect("Onkoloji & Genel", ["Yaygın Kemik Ağrısı", "İstemsiz Kilo Kaybı", "Gece Terlemesi (Sırılsıklam)", "Pel-Ebstein Ateşi"]))

# 5. DEV TIBBİ ALGORİTMA MOTORU
def dev_klinik_motor(b_list, vitaller):
    t_set, tet_set = set(), set(["Hemogram", "Geniş Biyokimya (AST, ALT, BUN, Cre, Na, K, Ca)", "CRP", "TİT"])
    b = set(b_list)
    ates, ta_sis, spo2, seker, yas = vitaller

    # --- ENDOKRİN & TOKSİKOLOJİ ---
    if seker > 250 and "Aseton Kokusu" in b:
        t_set.add("Diyabetik Ketoasidoz (DKA)")
        tet_set.update(["Arteriyel Kan Gazı", "İdrar/Kan Ketonu"])
    if "Mukozal Hiperpigmentasyon" in b:
        t_set.add("Addison Hastalığı")
        tet_set.update(["Sabah Kortizolü", "ACTH"])
    if "Miyozis (İğne Ucu Pupil)" in b and "Tükürük Artışı (Hipersalivasyon)" in b:
        t_set.add("Kolinerjik Sendrom / Organofosfat Zehirlenmesi")
        tet_set.update(["Kolinesteraz Düzeyi", "Acil Toksikoloji Konsültasyonu", "EKG"])

    # --- HEMATOLOJİ & ONKOLOJİ (YENİ) ---
    if "Pika (Toprak Yeme İsteği)" in b and "Solukluk/Derin Anemi" in b:
        t_set.add("Derin Demir Eksikliği Anemisi")
        tet_set.update(["Ferritin, Demir, TİBK", "GİS Endoskopisi/Kolonoskopi (Etyoloji için)"])
    if "Yaygın Kemik Ağrısı" in b and yas > 50:
        t_set.add("Multipl Myelom Şüphesi")
        tet_set.update(["Serum Protein Elektroforezi", "24 Saatlik İdrarda Bence-Jones", "Kalsiyum"])
    if "Diş Eti Kanaması" in b and "Peteşi/Purpura" in b:
        t_set.add("Trombositopeni / Akut Lösemi Şüphesi")
        tet_set.update(["Periferik Yayma", "PT/aPTT", "Kemik İliği Biyopsisi (Gerekirse)"])

    # --- KARDİYO & NEFRO (YENİ) ---
    if "Tek Taraflı Bacak Şişliği" in b:
        t_set.add("Derin Ven Trombozu (DVT)")
        tet_set.update(["Alt Ekstremite Venöz Doppler USG", "D-Dimer"])
    if "Üremik Koku" in b and "Oligüri" in b:
        t_set.add("Akut Böbrek Hasarı (ABH) / Üremi")
        tet_set.update(["Venöz Kan Gazı (Asidoz/K için)", "Renal USG", "Spot İdrar Na"])
    if "Kladikasyo (Yürürken Bacak Ağrısı)" in b:
        t_set.add("Periferik Arter Hastalığı (PAH)")
        tet_set.update(["Ayak Bileği-Kol İndeksi (ABI)", "Arteriyel Doppler USG"])

    # --- ROMATOLOJİ (GELİŞMİŞ) ---
    if "Oral Aft" in b and "Genital Ülser" in b and "Üveit (Göz Kızarıklığı)" in b:
        t_set.add("Behçet Hastalığı")
        tet_set.update(["Paterji Testi", "Göz Dibi Muayenesi", "HLA-B51"])
    if "Monoartrit (Akut Şişlik)" in b:
        t_set.add("Akut Gut Artriti / Septik Artrit")
        tet_set.update(["Serum Ürik Asit", "Eklem Sıvısı Analizi (Hücre ve Kristal)"])

    # --- GİS & NÖRO (KLASİKLER KORUNDU) ---
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        t_set.add("Akut Koroner Sendrom")
        tet_set.update(["Seri EKG", "Troponin I/T"])
    if "Fasiyal Asimetri" in b and "Fokal Güç Kaybı" in b:
        t_set.add("Akut İskemik İnme / SVO")
        tet_set.update(["Acil Kontrastsız Beyin BT", "Difüzyon MR"])
    if "Ani Şiddetli Baş Ağrısı" in b and "Ense Sertliği" in b:
        t_set.add("Subaraknoid Kanama (SAK) / Menenjit")
        tet_set.update(["Beyin BT", "BOS Analizi (LP)"])
    if "Sağ Alt Kadran Ağrısı" in b and "Kupür/Rebound" in b:
        t_set.add("Akut Apandisit")
        tet_set.update(["Batın BT"])

    return sorted(list(t_set)), sorted(list(tet_set))

# 6. Analiz Tetikleme
st.markdown("<br>", unsafe_allow_html=True)
if st.button("TIBBİ ALGORİTMAYI ÇALIŞTIR"):
    if not secilen and kan_sekeri == 100 and ates == 36.6 and ta_sis == 120:
        st.warning("⚠️ Lütfen semptom seçiniz veya vitalleri anormal değerlere getiriniz.")
    else:
        vitaller = (ates, ta_sis, spo2, kan_sekeri, yas)
        tanilar, tetkikler = dev_klinik_motor(secilen, vitaller)
        
        st.markdown("### 🏥 Klinik Karar Raporu")
        r1, r2 = st.columns(2)
        
        with r1:
            st.markdown("<div class='diagnose-card'>", unsafe_allow_html=True)
            st.subheader("📋 Diferansiyel Tanılar")
            if tanilar:
                for t in tanilar: st.markdown(f"**🚨 {t}**")
            else: 
                st.info("Rutin muayene bulguları. İleri anamnez önerilir.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with r2:
            st.markdown("<div class='test-card'>", unsafe_allow_html=True)
            st.subheader("🧪 İstenmesi Gereken Tetkikler")
            for tet in tetkikler: st.markdown(f"**🔬 {tet}**")
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Alt Bilgi
st.markdown("---")
st.caption("Dahiliye CDSS © 2026 | Tasarım ve Geliştirme: İSMAİL ORHAN | Profesyonel Tıbbi Kullanım İçindir.")
