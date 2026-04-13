import streamlit as st

# 1. Sayfa Ayarları ve "Görkemli" Web Tasarımı
st.set_page_config(page_title="Dahiliye CDSS Ultimate", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    /* Ana Tema: Deep Dark & Neon */
    .stApp { background: linear-gradient(160deg, #020617 0%, #0f172a 100%); color: #f8fafc; }
    
    /* Header: Glassmorphism Effect */
    .header-container {
        background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(20px);
        padding: 50px; border-radius: 30px; border: 1px solid rgba(56, 189, 248, 0.3);
        text-align: center; margin-bottom: 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.6);
    }
    
    /* Tabs: Gelişmiş Tasarım */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 15px 25px; color: #94a3b8; font-weight: 700;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important; color: white !important;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    
    /* Tanı ve Tetkik Kartları */
    .diagnose-box {
        background: rgba(239, 68, 68, 0.08); padding: 30px; border-radius: 25px;
        border: 2px solid rgba(239, 68, 68, 0.3); margin-bottom: 25px;
    }
    .test-box {
        background: rgba(16, 185, 129, 0.08); padding: 30px; border-radius: 25px;
        border: 2px solid rgba(16, 185, 129, 0.3);
    }
    
    /* Ultra Buton */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #d946ef 100%);
        color: white; border: none; border-radius: 20px; height: 5em;
        font-weight: 900; font-size: 20px; text-transform: uppercase;
        letter-spacing: 3px; box-shadow: 0 15px 40px rgba(59, 130, 246, 0.5);
        transition: all 0.5s ease;
    }
    .stButton>button:hover { transform: translateY(-7px) scale(1.02); box-shadow: 0 20px 50px rgba(139, 92, 246, 0.7); }
    </style>
    """, unsafe_allow_html=True)

# 2. Header Bölümü
st.markdown("""
    <div class='header-container'>
        <h1 style='font-size: 3em; margin: 0; background: -webkit-linear-gradient(#38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            DAHİLİYE CDSS ULTIMATE
        </h1>
        <p style='font-size: 1.4em; color: #94a3b8;'><b>İSMAİL ORHAN | Global Klinik Karar Destek Sistemi (v12.0)</b></p>
    </div>
    """, unsafe_allow_html=True)

# 3. Sidebar: Vital Veri Terminali
with st.sidebar:
    st.markdown("### 📊 VİTAL PARAMETRELER")
    yas = st.number_input("Yaş", 0, 120, 45)
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    nabiz = st.number_input("Nabız (atım/dk)", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 40, 100, 98)
    kan_sekeri = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 100)
    st.divider()
    if kan_sekeri > 250: st.error("🚨 HİPERGLİSEMİ!")
    if ta_sis > 180: st.error("🚨 HİPERTANSİF ACİL!")

# 4. DEVAŞA SEMPTOM VE KLİNİK BULGU PANELİ (En Geniş Kapsam)
st.subheader("🔍 Kapsamlı Klinik Bulgular")
t1, t2, t3, t4, t5, t6, t7 = st.tabs([
    "🩺 GİS & Hepatoloji", "🫁 Kardiyo & Solunum", "🧠 Nöroloji", 
    "🦋 Romatoloji", "🧪 Endokrin & Nefro", "🧬 Hemato & Onko", "🐍 Toksikoloji & Enfeksiyon"
])

secilen = []
with t1:
    c1, c2 = st.columns(2)
    with c1: secilen.extend(st.multiselect("Üst GİS", ["Hematemez", "Melena", "Disfaji (Katı/Sıvı)", "Odinofaji", "Epigastrik Hassasiyet", "Grey Turner Belirtisi", "Cullen Belirtisi", "Erken Doyma"]))
    with c2: secilen.extend(st.multiselect("Alt GİS & Karaciğer", ["Hematokezya", "Sarılık", "Asit", "Caput Medusae", "Asteriksis", "Murphy Belirtisi (+)", "Sağ Alt Kadran Ağrısı", "McBurney Hassasiyeti"]))

with t2:
    c3, c4 = st.columns(2)
    with c3: secilen.extend(st.multiselect("Kardiyoloji", ["Baskı Tarzı Göğüs Ağrısı", "Çarpıntı", "Senkop", "S3 Galo", "Janeway Lezyonları", "Osler Nodülleri", "Roth Lekeleri", "Boyun Ven Dolgunluğu", "Tek Taraflı Bacak Şişliği"]))
    with c4: secilen.extend(st.multiselect("Göğüs Hastalıkları", ["Efor Dispnesi", "Hemoptizi", "Plevritik Ağrı", "Wheezing", "Stridor", "Çomak Parmak", "Vena Cava Superior Sendromu (Yüzde Ödem)"]))

with t3:
    secilen.extend(st.multiselect("Nöroloji & Psikiyatri", ["Ani Şiddetli Baş Ağrısı", "Ense Sertliği", "Fokal Güç Kaybı", "Fasiyal Asimetri", "Konfüzyon", "Ataksi", "Dizartri", "Miyozis", "Midriyazis"]))

with t4:
    c5, c6 = st.columns(2)
    with c5: secilen.extend(st.multiselect("Romatoloji (Deri/Eklem)", ["Kelebek Döküntü", "Raynaud Fenomeni", "Güneş Hassasiyeti", "Sabah Sertliği (>1 saat)", "Poliartrit (Simetrik)", "Monoartrit (Akut Şişlik)"]))
    with c6: secilen.extend(st.multiselect("Vaskülit & Özel", ["Oral Aft", "Genital Ülser", "Üveit", "Gottron Papülleri", "Helitrop Raş", "Paterji (+)", "Bambu Kamışı Omurga"]))

with t5:
    c7, c8 = st.columns(2)
    with c7: secilen.extend(st.multiselect("Endokrinoloji", ["Poliüri/Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Buffalo Hörgücü", "Mor Stria", "Ekzoftalmi", "Hiperpigmentasyon", "Tremor (İnce)"]))
    with c8: secilen.extend(st.multiselect("Nefroloji", ["Oligüri", "Anüri", "Hematüri", "Köpüklü İdrar", "Üremik Koku", "Pretibial Ödem", "Kostavertebral Açı Hassasiyeti"]))

with t6:
    secilen.extend(st.multiselect("Hematoloji & Onkoloji", ["Solukluk", "İstemsiz Kilo Kaybı", "Gece Terlemesi", "Splenomegali", "Jeneralize Lenfadenopati", "Peteşi/Purpura", "Kemik Ağrısı (Yaygın)"]))

with t7:
    secilen.extend(st.multiselect("Toksikoloji & Enfeksiyon", ["Hipersalivasyon (Tükürük Artışı)", "Pel-Ebstein Ateşi", "Kene Isırması Öyküsü", "Madde Kullanımı Şüphesi", "Konjuktival Şiddetli Kızarıklık"]))

# 5. DEV TIBBİ ANALİZ MOTORU (Full Logic)
def ultimate_engine(bulgular, vitaller):
    t_set, tet_set = set(), {"Hemogram", "CRP", "Geniş Biyokimya (AST, ALT, Cre, Na, K, Ca, Mg)", "TİT", "EKG"}
    b = set(bulgular)
    ates, ta_s, spo2, seker, yas = vitaller

    # --- KRİTİK ACİLLER ---
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        t_set.add("Akut Koroner Sendrom (STEMI/NSTEMI)"); tet_set.update(["Seri Troponin", "EKO", "Koroner Anjiyo"])
    if "Vena Cava Superior Sendromu (Yüzde Ödem)" in b:
        t_set.add("Onkolojik Acil: VCS Sendromu (Malignite?)"); tet_set.update(["Toraks BT Anjiyo", "Biyopsi"])
    if "Ani Şiddetli Baş Ağrısı" in b and "Ense Sertliği" in b:
        t_set.add("Subaraknoid Kanama / Menenjit"); tet_set.update(["Beyin BT", "BOS Analizi (LP)"])
    if "Aseton Kokusu" in b and seker > 250:
        t_set.add("Diyabetik Ketoasidoz (DKA)"); tet_set.update(["Arteriyel Kan Gazı", "İdrar/Kan Ketonu"])
    if "Hipersalivasyon (Tükürük Artışı)" in b and "Miyozis" in b:
        t_set.add("Kolinerjik Kriz (Organofosfat Zehirlenmesi?)"); tet_set.update(["Kolinesteraz Düzeyi", "Atropin Yanıtı İzlemi"])

    # --- ÖZEL SENDROMLAR ---
    if "Janeway Lezyonları" in b or "Osler Nodülleri" in b:
        t_set.add("İnfektif Endokardit"); tet_set.update(["Kan Kültürü (3 Set)", "TEE (Eko)"])
    if "Grey Turner Belirtisi" in b or "Cullen Belirtisi" in b:
        t_set.add("Nekrotizan Pankreatit"); tet_set.update(["Amilaz/Lipaz", "Kontrastlı Batın BT"])
    if "Asteriksis" in b and "Sarılık" in b:
        t_set.add("Hepatik Ensefalopati"); tet_set.update(["Amonyak", "Karaciğer USG", "PT/INR"])
    if "Kelebek Döküntü" in b:
        t_set.add("Sistemik Lupus Eritematozus (SLE)"); tet_set.update(["ANA", "Anti-dsDNA", "Kompleman (C3, C4)"])
    if "Oral Aft" in b and "Genital Ülser" in b:
        t_set.add("Behçet Hastalığı"); tet_set.update(["Paterji Testi", "Göz Muayenesi", "HLA-B51"])
    if "Hiperpigmentasyon" in b and ta_s < 90:
        t_set.add("Addison Hastalığı / Adrenal Yetmezlik"); tet_set.update(["Sabah Kortizolü", "ACTH", "Serum Na/K Oranı"])
    if "Poliüri/Polidipsi" in b and seker < 110:
        t_set.add("Diyabetes İnsipitus"); tet_set.update(["İdrar/Serum Osmolalitesi", "ADH Düzeyi"])
    if "Ekzoftalmi" in b and "Sıcak İntoleransı" in b:
        t_set.add("Graves Hastalığı (Hipertiroidi)"); tet_set.update(["TSH, sT3, sT4", "TRAb"])
    if "Yaygın Kemik Ağrısı" in b and yas > 50:
        t_set.add("Multipl Myelom"); tet_set.update(["Serum Protein Elektroforezi", "24s İdrarda Bence-Jones", "Kalsiyum"])
    if "Raynaud Fenomeni" in b and "Disfaji (Katı/Sıvı)" in b:
        t_set.add("Sistemik Skleroz (Scleroderma)"); tet_set.update(["Anti-Scl-70", "Antisentromer Antikoru"])
    if "Helitrop Raş" in b or "Gottron Papülleri" in b:
        t_set.add("Dermatomiyozit"); tet_set.update(["CK", "Aldolaz", "Kas Biyopsisi"])

    return sorted(list(t_set)), sorted(list(tet_set))

# 6. Sonuç Ekranı
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 ULTIMATE ANALİZİ ÇALIŞTIR"):
    if not secilen and ates == 36.6 and kan_sekeri == 100:
        st.warning("⚠️ Lütfen veri girişi yapınız.")
    else:
        v_data = (ates, ta_sis, spo2, kan_sekeri, yas)
        tanilar, tetkikler = ultimate_engine(secilen, v_data)
        
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("<div class='diagnose-box'><h2>🚨 OLASI ÖN TANILAR</h2>", unsafe_allow_html=True)
            if tanilar:
                for t in tanilar: st.markdown(f"🔥 **{t}**")
            else: st.info("Semptom kombinasyonları spesifik bir tablo oluşturmadı.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with r2:
            st.markdown("<div class='test-box'><h2>🧪 ÖNERİLEN TETKİKLER</h2>", unsafe_allow_html=True)
            for tet in tetkikler: st.markdown(f"🔬 **{tet}**")
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Alt Bilgi
st.markdown("---")
st.markdown("<p style='text-align: center; opacity: 0.6;'>Dahiliye Ultimate CDSS v12.0 | İSMAİL ORHAN tarafından geliştirilmiştir.</p>", unsafe_allow_html=True)
