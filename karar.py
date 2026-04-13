import streamlit as st

# 1. Sayfa Konfigürasyonu ve Premium CSS
st.set_page_config(page_title="Dahiliye CDSS Premium", page_icon="💎", layout="wide")

# Gösterişli Web Sitesi Tasarımı (Glassmorphism & Gradients)
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Header Tasarımı */
    .header-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    /* Sekme Tasarımı */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px 25px;
        color: #cbd5e1;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(90deg, #3b82f6, #2dd4bf) !important;
        color: white !important;
        transform: translateY(-3px);
    }
    
    /* Kart Tasarımları */
    .diagnose-card {
        background: rgba(220, 38, 38, 0.1);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(220, 38, 38, 0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .test-card {
        background: rgba(16, 185, 129, 0.1);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Modern Buton */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2dd4bf 100%);
        color: white;
        border: none;
        border-radius: 15px;
        height: 4em;
        font-weight: 800;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
        transition: all 0.4s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02) translateY(-5px);
        box-shadow: 0 15px 30px rgba(59, 130, 246, 0.5);
    }
    
    /* Yazı Renkleri Ayarı */
    h1, h2, h3, p, span, label { color: #f8fafc !important; }
    .stMultiSelect label { font-weight: bold; color: #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bölüm
st.markdown("""
    <div class='header-box'>
        <h1>⚕️ Dahiliye Klinik Karar Destek Portalı</h1>
        <p style='font-size: 1.2em; opacity: 0.8;'><b>Sürüm: 10.0 (Geliştirici: İSMAİL ORHAN)</b></p>
    </div>
    """, unsafe_allow_html=True)

# 3. Sidebar: Vital Veri Merkezi
with st.sidebar:
    st.markdown("### 📊 Vital Parametreler")
    yas = st.number_input("Hasta Yaşı", 0, 120, 45)
    st.divider()
    ates = st.slider("Vücut Isısı (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 40, 100, 98)
    kan_sekeri = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 100)
    
    # Akıllı Renkli Uyarılar
    if kan_sekeri > 300: st.error("🚨 KRİTİK HİPERGLİSEMİ")
    if ta_sis > 200: st.error("🚨 HİPERTANSİF KRİZ")
    if spo2 < 88: st.warning("⚠️ SOLUNUM YETMEZLİĞİ RİSKİ")

# 4. DEVAŞA SEMPTOM VERİ TABANI (Branş Branş Sekmeli)
st.markdown("### 🔍 Klinik Belirti ve Bulgular")
t1, t2, t3, t4, t5, t6 = st.tabs(["GİS & Karaciğer", "Kardiyo & Akciğer", "Nöro & Psikiyatri", "Romatoloji & Deri", "Endokrin & Nefroloji", "Hemato & Onkoloji"])

secilen = []
with t1:
    c1, c2 = st.columns(2)
    with c1: secilen.extend(st.multiselect("Üst GİS & Özofagus", ["Hematemez", "Melena", "Odinofaji", "Disfaji", "Epigastrik Hassasiyet", "Grey Turner Belirtisi", "Cullen Belirtisi"]))
    with c2: secilen.extend(st.multiselect("Hepatobilier", ["Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Caput Medusae", "Palmar Eritem", "Asteriksis (Flapping Tremor)"]))

with t2:
    c3, c4 = st.columns(2)
    with c3: secilen.extend(st.multiselect("Kardiyoloji", ["Baskı Tarzı Göğüs Ağrısı", "PND / Ortopne", "S3 Galo Ritmi", "Janeway Lezyonları", "Osler Nodülleri", "Roth Lekeleri"]))
    with c4: secilen.extend(st.multiselect("Göğüs Hastalıkları", ["Hemoptizi", "Efor Dispnesi", "Plevritik Ağrı", "Çomak Parmak", "Stridor", "Wheezing", "Frotman"]))

with t3:
    secilen.extend(st.multiselect("Nörolojik & Toksikolojik", ["Ani Şiddetli Baş Ağrısı", "Ense Sertliği", "Fokal Nörolojik Defisit", "Ataksi", "Miyozis", "Midriyazis", "Hipersalivasyon", "Konfüzyon"]))

with t4:
    c5, c6 = st.columns(2)
    with c5: secilen.extend(st.multiselect("Bağ Dokusu", ["Sabah Sertliği", "Poliartrit", "Kelebek Döküntü (Malar Raş)", "Raynaud Fenomeni", "Güneş Hassasiyeti"]))
    with c6: secilen.extend(st.multiselect("Vaskülit & Özel", ["Oral/Genital Aft", "Eritema Nodosum", "Paterji Pozitifliği", "Gottron Papülleri", "Bambu Kamışı Omurga"]))

with t5:
    c7, c8 = st.columns(2)
    with c7: secilen.extend(st.multiselect("Endokrinoloji", ["Poliüri/Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Ekzoftalmi", "Pretibial Miksödem", "Galaktore"]))
    with c8: secilen.extend(st.multiselect("Nefroloji", ["Oligüri/Anüri", "Hematüri", "Köpüklü İdrar", "Üremik Koku", "Kostavertebral Açı Hassasiyeti", "Periorbital Ödem"]))

with t6:
    secilen.extend(st.multiselect("Hematoloji & Onkoloji", ["Solukluk", "Diş Eti Kanaması", "Peteşi/Purpura", "B-Semptomları (Kilo Kaybı, Gece Terlemesi, Ateş)", "Lenfadenopati", "Vena Cava Superior Sendromu (Yüzde Şişlik)"]))

# 5. AKILLI ANALİZ MOTORU (Full Offline Logic)
def v10_engine(bulgular, vitaller):
    t_set, tet_set = set(), {"Hemogram", "CRP", "Geniş Biyokimya", "TİT", "EKG"}
    b = set(bulgular)
    ates, ta_sis, spo2, seker, yas = vitaller

    # --- KRİTİK VE ÖZEL EŞLEŞMELER ---
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        t_set.add("Akut Koroner Sendrom (MI)"); tet_set.update(["Seri Troponin", "EKO", "Koroner Anjiografi"])
    if "Ani Şiddetli Baş Ağrısı" in b and "Ense Sertliği" in b:
        t_set.add("Subaraknoid Kanama / Menenjit"); tet_set.update(["Beyin BT", "BOS Analizi (LP)"])
    if "Janeway Lezyonları" in b or "Osler Nodülleri" in b:
        t_set.add("İnfektif Endokardit"); tet_set.update(["3 Set Kan Kültürü", "Transözofageal EKO"])
    if "Grey Turner Belirtisi" in b or "Cullen Belirtisi" in b:
        t_set.add("Nekrotizan Pankreatit"); tet_set.update(["Amilaz/Lipaz", "Kontrastlı Batın BT"])
    if "Aseton Kokusu" in b and seker > 250:
        t_set.add("Diyabetik Ketoasidoz (DKA)"); tet_set.update(["Kan Gazı", "İdrar Ketonu"])
    if "Vena Cava Superior Sendromu (Yüzde Şişlik)" in b:
        t_set.add("Onkolojik Acil: VCS Sendromu (Akciğer/Lenfoma?)"); tet_set.update(["Toraks BT Anjiyo", "Biyopsi Planı"])
    if "Kelebek Döküntü (Malar Raş)" in b:
        t_set.add("Sistemik Lupus Eritematozus (SLE)"); tet_set.update(["ANA, Anti-dsDNA", "Kompleman Düzeyleri"])
    if "Asteriksis (Flapping Tremor)" in b and "Sarılık" in b:
        t_set.add("Hepatik Ensefalopati / KBY"); tet_set.update(["Amonyak", "Karaciğer USG", "PT/INR"])
    if "Raynaud Fenomeni" in b and "Disfaji" in b:
        t_set.add("Sistemik Skleroz (Scleroderma)"); tet_set.update(["Anti-Scl-70", "Özofagus Manometrisi"])
    if "Oral/Genital Aft" in b and "Eritema Nodosum" in b:
        t_set.add("Behçet Hastalığı"); tet_set.update(["Paterji Testi", "Göz Muayenesi"])
    if "Poliüri/Polidipsi" in b and seker < 110:
        t_set.add("Diyabetes İnsipitus"); tet_set.update(["Serum/İdrar Osmolalitesi", "ADH Düzeyi"])

    return sorted(list(t_set)), sorted(list(tet_set))

# 6. Sonuç Ekranı
st.markdown("<br>", unsafe_allow_html=True)
if st.button("KLİNİK ANALİZİ BAŞLAT (PREMIUM)"):
    if not secilen and ates == 36.6 and kan_sekeri == 100:
        st.warning("⚠️ Analiz için lütfen veri girişi yapınız.")
    else:
        v_data = (ates, ta_sis, spo2, kan_sekeri, yas)
        tanilar, tetkikler = v10_engine(secilen, v_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='diagnose-card'><h3>🚨 Olası Ön Tanılar</h3>", unsafe_allow_html=True)
            if tanilar:
                for t in tanilar: st.write(f"🔥 **{t}**")
            else: st.info("Spesifik bir sendrom saptanmadı.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='test-card'><h3>🧪 Önerilen Tetkikler</h3>", unsafe_allow_html=True)
            for tet in tetkikler: st.write(f"🔬 {tet}")
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Footer
st.markdown("---")
st.markdown("<p style='text-align: center; opacity: 0.5;'>Dahiliye Klinik Karar Destek Sistemi v10.0 | Tasarım: İSMAİL ORHAN | © 2026</p>", unsafe_allow_html=True)
