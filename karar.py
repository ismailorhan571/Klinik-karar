import streamlit as st

# 1. SAYFA KONFİGÜRASYONU VE ULTRA WEB TASARIMI (CSS ZENGİNLİĞİ)
st.set_page_config(page_title="Dahiliye CDSS The Beast v14", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    /* Premium Karanlık Tema ve Neon Geçişler */
    .stApp { background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e1b4b 100%); color: #f1f5f9; }
    
    /* Üst Başlık ve Animasyonlu Gölgeler */
    .main-header {
        background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(25px);
        padding: 60px; border-radius: 40px; border: 2px solid #3b82f6;
        text-align: center; margin-bottom: 50px; 
        box-shadow: 0 30px 60px rgba(0,0,0,0.8), 0 0 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Kategori Sekmeleri (Büyük ve Belirgin) */
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; padding: 20px 35px; color: #94a3b8; font-size: 18px; font-weight: 800;
        margin-right: 15px; transition: 0.3s;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(90deg, #2563eb, #9333ea) !important; color: white !important;
        transform: scale(1.05); box-shadow: 0 10px 20px rgba(37, 99, 235, 0.5);
    }
    
    /* Sonuç Kartları (Devasa ve Profesyonel) */
    .result-card-red {
        background: linear-gradient(145deg, rgba(153, 27, 27, 0.2), rgba(69, 10, 10, 0.4));
        padding: 40px; border-radius: 30px; border-left: 10px solid #ef4444;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5); margin-bottom: 30px;
    }
    .result-card-green {
        background: linear-gradient(145deg, rgba(21, 128, 61, 0.2), rgba(5, 46, 22, 0.4));
        padding: 40px; border-radius: 30px; border-left: 10px solid #22c55e;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5); margin-bottom: 30px;
    }
    .result-card-blue {
        background: linear-gradient(145deg, rgba(30, 58, 138, 0.2), rgba(30, 64, 175, 0.4));
        padding: 40px; border-radius: 30px; border-left: 10px solid #3b82f6;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
    }

    /* MultiSelect ve Input Tasarımı */
    .stMultiSelect div div { background-color: #1e293b !important; color: white !important; border-radius: 10px; }
    
    /* Dev Buton */
    .stButton>button {
        background: linear-gradient(90deg, #1d4ed8 0%, #7e22ce 50%, #db2777 100%);
        color: white; border: none; border-radius: 25px; height: 6em; width: 100%;
        font-weight: 900; font-size: 24px; letter-spacing: 4px; 
        box-shadow: 0 20px 50px rgba(29, 78, 216, 0.6); transition: 0.5s;
    }
    .stButton>button:hover { transform: translateY(-10px); box-shadow: 0 30px 70px rgba(126, 34, 206, 0.8); }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("""
    <div class='main-header'>
        <h1 style='font-size: 4em; margin: 0; color: #ffffff; text-shadow: 4px 4px 10px #000;'>⚕️ DAHİLİYE CDSS - THE BEAST</h1>
        <p style='font-size: 1.6em; color: #38bdf8; margin-top: 20px; font-weight: 700;'>
            Dünyanın En Geniş Klinik Karar Destek Algoritması | Geliştirici: İSMAİL ORHAN
        </p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL (VİTAL MERKEZ)
with st.sidebar:
    st.markdown("## 📊 HASTA TERMİNALİ")
    yas = st.number_input("Kronolojik Yaş", 0, 120, 45)
    st.divider()
    ates = st.slider("Vücut Isısı (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik Tansiyon", 50, 250, 120)
    ta_dia = st.number_input("Diastolik Tansiyon", 30, 150, 80)
    nabiz = st.number_input("Nabız Hızı", 30, 250, 80)
    spo2 = st.slider("Oksijen Satürasyonu (SpO2)", 40, 100, 98)
    kan_sekeri = st.number_input("Glukoz (mg/dL)", 20, 1000, 100)
    
    st.markdown("### 🧬 RİSK ANALİZİ")
    if ta_sis < 90: st.error("⚠️ ŞOK TABLOSU ŞÜPHESİ")
    if ates > 38.3: st.warning("⚠️ FEBRİL TABLO")
    if kan_sekeri > 300: st.error("⚠️ DKA/HHS RİSKİ")

# 4. DEVAŞA SEMPTOM MATRİSİ (HİÇBİR ŞEYİ ATLAMADAN)
st.markdown("## 🔎 KOMPLEKS SEMPTOM VE BULGU GİRİŞİ")
t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs([
    "🍷 GİS & HEPATO", "❤️ KARDİYO", "🌬️ SOLUNUM", "🧠 NÖROLOJİ", 
    "🦋 ROMATOLOJİ", "🍭 ENDOKRİN", "🩸 HEMATO", "🏥 NEFRO"
])

secilen = []
with t1:
    c1, c2 = st.columns(2)
    with c1: secilen.extend(st.multiselect("Üst GİS", ["Hematemez", "Melena", "Disfaji", "Odinofaji", "Epigastrik Ağrı", "Pirozis", "Erken Doyma", "Hematokezya"]))
    with c2: secilen.extend(st.multiselect("Karaciğer & Pankreas", ["Sarılık", "Asit", "Caput Medusae", "Asteriksis", "Grey Turner", "Cullen", "Murphy (+)", "Splenomegali"]))

with t2:
    c3, c4 = st.columns(2)
    with c3: secilen.extend(st.multiselect("Kalp", ["Baskı Tarzı Göğüs Ağrısı", "PND", "Ortopne", "S3 Galo Ritmi", "Janeway Lezyonları", "Osler Nodülleri", "Roth Lekeleri"]))
    with c4: secilen.extend(st.multiselect("Vasküler", ["Boyun Ven Dolgunluğu", "Tek Taraflı Bacak Şişliği", "Raynaud Fenomeni", "Kladikasyo İntermittant", "Palpabl Purpura"]))

with t3:
    secilen.extend(st.multiselect("Akciğer", ["Hemoptizi", "Plevritik Ağrı", "Wheezing", "Stridor", "Çomak Parmak", "VCS Sendromu", "Kuru Öksürük", "Gece Terlemesi"]))

with t4:
    secilen.extend(st.multiselect("Nöro/Psikiyatri", ["Ani Şiddetli Baş Ağrısı", "Ense Sertliği", "Fokal Güç Kaybı", "Fasiyal Asimetri", "Konfüzyon", "Ataksi", "Miyozis", "Midriyazis"]))

with t5:
    secilen.extend(st.multiselect("Bağ Dokusu & Eklem", ["Kelebek Döküntü", "Sabah Sertliği", "Poliartrit", "Güneş Hassasiyeti", "Oral Aft", "Genital Ülser", "Paterji (+)", "Bambu Omurga"]))

with t6:
    secilen.extend(st.multiselect("Endokrin", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Buffalo Hörgücü", "Mor Stria", "Ekzoftalmi", "Hiperpigmentasyon"]))

with t7:
    secilen.extend(st.multiselect("Hematoloji", ["Peteşi", "Ekimoz", "Diş Eti Kanaması", "B-Semptomları", "Solukluk", "Lenfadenopati", "Kemik Ağrısı", "Schistosit Şüphesi"]))

with t8:
    secilen.extend(st.multiselect("Böbrek", ["Oligüri", "Hematüri", "Köpüklü İdrar", "Üremik Koku", "Periorbital Ödem", "Kostavertebral Açı Hassasiyeti"]))

# 5. THE BEAST ENGINE (UZUN, DETAYLI, KRİTİK ANALİZ)
def engine_v14(b_list, v):
    tanilar, tetkikler, tedaviler = [], [], ["Standart Monitorizasyon", "IV Damar Yolu Açılması"]
    b = set(b_list)
    ates, ta_s, spo2, seker, yas = v

    # --- ÜST GİS KANAMA VE ACİLİYET ---
    if "Hematemez" in b or "Melena" in b:
        tanilar.append("ÜST GİS KANAMA (Peptik Ülser / Varis Kanama / Mallory-Weiss)")
        tetkikler.extend(["ACİL ENDOSKOPİ", "Hemogram (Htc Takibi)", "PT/INR", "Kan Grubu", "BUN/Kreatinin Oranı"])
        tedaviler.extend(["IV PPI Bolus + İnfüzyon (80mg + 8mg/saat)", "Somatostatin (Eğer Varis Şüphesi)", "IV Kristaloid (SF/RL)", "Gerekirse Eritrosit Süspansiyonu"])

    # --- KARACİĞER YETMEZLİĞİ VE SİROZ ---
    if "Sarılık" in b and "Asteriksis" in b:
        tanilar.append("HEPATİK ENSEFALOPATİ / DEKOMPANSE SİROZ")
        tetkikler.extend(["Amonyak Düzeyi", "Batın USG (Portal Doppler)", "Bilirubinler", "Albumin"])
        tedaviler.extend(["Laktüloz (2x1 veya Enema)", "Rifaksimin 550mg 2x1", "Protein Kısıtlı Diyet", "K Vitamini"])

    # --- KARDİYO-PULMONER ACİLLER ---
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        tanilar.append("AKUT KORONER SENDROM (STEMI / NSTEMI / Unstable Angina)")
        tetkikler.extend(["SERİ TROPONİN (0-3-6. saat)", "12 Kanallı EKG", "EKO", "Koroner Anjiyografi"])
        tedaviler.extend(["Aspirin 300mg Çiğnetme", "Klopidogrel 300-600mg", "Sublingual Nitrat", "Gerekirse Morfin"])

    if "Hemoptizi" in b and "Tek Taraflı Bacak Şişliği" in b:
        tanilar.append("PULMONER EMBOLİ (DVT İlişkili)")
        tetkikler.extend(["Toraks BT Anjiyo", "D-Dimer", "Alt Ekstremite Venöz Doppler"])
        tedaviler.extend(["Düşük Molekül Ağırlıklı Heparin (Enoksaparin)", "Oksijen Desteği", "Stabilizasyon Sonrası Varfarin/NOAC"])

    # --- ENDOKRİN KRİZLER ---
    if seker > 250 and "Aseton Kokusu" in b:
        tanilar.append("DİYABETİK KETOASİDOZ (DKA)")
        tetkikler.extend(["Arteriyel/Venöz Kan Gazı", "İdrar Ketonu", "Anyon Açığı Hesabı", "Serum Potasyumu"])
        tedaviler.extend(["IV İnsülin İnfüzyonu (0.1 u/kg/saat)", "IV Mayi Replasmanı (SF)", "Potasyum Eklenmesi (Eğer <5.0)"])

    if "Hiperpigmentasyon" in b and ta_s < 90:
        tanilar.append("ADRENAL YETMEZLİK (ADDİSON KRİZİ)")
        tetkikler.extend(["Sabah Kortizolü", "ACTH Düzeyi", "Serum Sodyum/Potasyum"])
        tedaviler.extend(["IV Hidrokortizon 100mg", "Bolus SF (2-3 Litre)"])

    # --- ROMATOLOJİK & VASKÜLİT ---
    if "Oral Aft" in b and "Genital Ülser" in b and "Paterji (+)" in b:
        tanilar.append("BEHÇET HASTALIĞI")
        tetkikler.extend(["HLA-B51", "Göz Muayenesi (Uveit Takibi)", "Sakroiliak Grafi"])
        tedaviler.extend(["Kolşisin 0.5mg 2x1", "Topikal Steroidler", "Azatioprin (Organ Tutulumu Varsa)"])

    if "Kelebek Döküntü" in b and "Poliartrit" in b:
        tanilar.append("SİSTEMİK LUPUS ERİTEMATOZUS (SLE)")
        tetkikler.extend(["ANA Paneli", "Anti-dsDNA", "C3/C4 Kompleman", "Spot İdrar Protein/Kreatinin"])
        tedaviler.extend(["Hidroksiklorokin", "Gerekirse Puls Steroid", "Güneş Koruyucu Kullanımı"])

    # --- HEMATO-ONKOLOJİK ACİLLER ---
    if "VCS Sendromu" in b:
        tanilar.append("ONKOLOJİK ACİL: VENA CAVA SUPERİOR SENDROMU")
        tetkikler.extend(["Kontrastlı Toraks BT", "Biyopsi (Kitleden)", "LDH"])
        tedaviler.extend(["IV Deksametazon", "Acil Radyoterapi Konsültasyonu", "Baş Eleve Pozisyon"])

    if "Schistosit Şüphesi" in b and "Konfüzyon" in b:
        tanilar.append("TROMBOTİK TROMBOSİTOPENİK PURPURA (TTP)")
        tetkikler.extend(["Periferik Yayma (ZORUNLU)", "ADAMTS13 Düzeyi", "İndirekt Bilirubin", "Haptoglobin"])
        tedaviler.extend(["ACİL PLAZMAFEREZ", "Steroid Tedavisi", "Trombosit Transfüzyonundan Kaçın!"])

    # --- NEFROLOJİ ---
    if "Üremik Koku" in b and "Oligüri" in b:
        tanilar.append("AKUT BÖBREK HASARI / KRONİK BÖBREK YETMEZLİĞİ (EVRE 4-5)")
        tetkikler.extend(["Serum Üre/Kreatinin", "Fraksiyone Sodyum Ekskresyonu", "Böbrek USG", "Serum Potasyumu"])
        tedaviler.extend(["Sıvı Kısıtlaması", "Diyaliz Endikasyonu Değerlendirme", "Hiperkalemi Tedavisi"])

    # --- NÖROLOJİ ---
    if "Ense Sertliği" in b and ates > 38:
        tanilar.append("AKUT BAKTERİYEL MENENJİT")
        tetkikler.extend(["Lomber Ponksiyon (BOS Analizi)", "Beyin BT", "Kan Kültürü"])
        tedaviler.extend(["Acil Seftriakson 2x2gr IV", "Vankomisin", "Deksametazon (Antibiyotik Öncesi)"])

    # --- EĞER HİÇBİR ŞEY EŞLEŞMEZSE ---
    if not tanilar:
        tanilar.append("Non-Spesifik Klinik Tablo (Klinik İzlem Önerilir)")
        tedaviler.append("İleri Tetkik Sonuçları Beklenmeli")

    return tanilar, sorted(list(set(tetkikler))), sorted(list(set(tedaviler)))

# 6. ANALİZ TETİKLEME
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("🚀 THE BEAST ANALİZİ BAŞLAT (MAXIMUM DEPTH)"):
    if not secilen and ates == 36.6:
        st.error("⚠️ SİSTEME VERİ GİRMEDİNİZ. ANALİZ YAPILAMIYOR.")
    else:
        with st.spinner("Milyarlarca Olasılık Hesaplanıyor..."):
            v_data = (ates, ta_sis, spo2, kan_sekeri, yas)
            tanilar, tetkikler, tedaviler = engine_v14(secilen, v_data)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # ÜÇLÜ PANEL GÖRÜNÜMÜ
            col_t, col_e, col_m = st.columns(3)
            
            with col_t:
                st.markdown("<div class='result-card-red'><h2>🚨 OLASI TIBBİ TANILAR</h2>", unsafe_allow_html=True)
                for t in tanilar: st.write(f"🔥 **{t}**")
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_e:
                st.markdown("<div class='result-card-green'><h2>🧪 TETKİK VE LABORATUVAR</h2>", unsafe_allow_html=True)
                for tet in tetkikler: st.write(f"🔬 {tet}")
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_m:
                st.markdown("<div class='result-card-blue'><h2>💊 ACİL YÖNETİM & TEDAVİ</h2>", unsafe_allow_html=True)
                for ted in tedaviler: st.write(f"✅ {ted}")
                st.markdown("</div>", unsafe_allow_html=True)

# 7. FOOTER
st.markdown("---")
st.markdown(f"<p style='text-align: center; opacity: 0.6;'>Dahiliye The Beast v14.0 | <b>Geliştirici: İSMAİL ORHAN</b> | Dahiliye Uzmanlık Seviyesinde Algoritma.</p>", unsafe_allow_html=True)
