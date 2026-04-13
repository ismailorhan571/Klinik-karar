import streamlit as st
from datetime import datetime

# 1. ULTRA-PREMIUM UI (IVORY, GOLD & AGGRESSIVE REDLINE)
st.set_page_config(page_title="İSMAİL ORHAN | DAHİLİYE KLİNİK KARAR ROBOTU", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 30px; border-radius: 40px; text-align: center; margin-bottom: 30px;
        border-top: 12px solid #DC2626; border-bottom: 12px solid #DC2626; border-left: 6px solid #D4AF37; border-right: 6px solid #D4AF37;
        box-shadow: 0 45px 90px rgba(0,0,0,0.18);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 2.8rem; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.3rem; font-weight: 700; text-transform: uppercase; }

    .clinical-card { 
        background: #FFFFFF; padding: 40px; border-radius: 45px; margin-bottom: 30px;
        border-left: 22px solid #DC2626; border-right: 10px solid #D4AF37;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 40px;
        height: 6.5em; width: 100%; font-weight: 800; font-size: 30px; border: 5px solid #DC2626;
    }
    .stButton>button:hover { background: #DC2626; transform: scale(1.01); }
    
    [data-testid="stSidebar"] { background-color: #F9F8F0; border-right: 8px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KARAR MEKANİZMASI</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN </p></div>", unsafe_allow_html=True)

# 2. YAN PANEL - KAN SONUÇLARI (TAM KONTROL)
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR PANELİ")
    p_no = st.text_input("Barkod", "IO-V24-100")
    yas = st.number_input("Yaş", 0, 120, 55)
    kilo = st.number_input("Kilo (kg)", 5, 250, 80)
    
    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 40.0, 1.1)
    hb = st.number_input("Hemoglobin", 3.0, 25.0, 13.5)
    wbc = st.number_input("WBC", 0, 500000, 7500)
    plt = st.number_input("PLT", 0, 2000000, 220000)
    glu = st.number_input("Glukoz", 0, 3000, 100)
    na = st.number_input("Sodyum (Na)", 100, 180, 140)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.0)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 20.0, 9.5)
    ldh = st.number_input("LDH", 0, 10000, 200)
    ast_alt = st.checkbox("AST/ALT > 100")
    trop = st.checkbox("Troponin / CK-MB (+)")
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("eGFR", f"{egfr} ml/dk")

# 3. GENİŞLETİLMİŞ BELİRTİ SEÇİMİ (TÜM SİSTEMLER)
st.subheader("🔍 Klinik Belirtiler ve Bulgular")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KARDİYO", "🫁 AKCİĞER", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖRO", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENF"])

b = []
with t1: b.extend(st.multiselect("KV", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Boyun Ven Dolgunluğu", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Üfürüm", "Taşikardi"]))
with t2: b.extend(st.multiselect("AKC", ["Nefes Darlığı", "Hemoptizi", "Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı"]))
with t3: b.extend(st.multiselect("GİS", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı"]))
with t4: b.extend(st.multiselect("ENDO", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Galaktore", "El-Ayak Büyümesi", "Tremor", "Soğuk İntoleransı"]))
with t5: b.extend(st.multiselect("NÖRO", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi"]))
with t6: b.extend(st.multiselect("HEM", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması"]))
with t7: b.extend(st.multiselect("ROM", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit"]))

# Lab verilerini tanıya işle
if kre > 1.4: b.append("Renal Bozukluk")
if hb < 11: b.append("Anemi")
if hb > 17.5: b.append("Polisitemi")
if wbc > 11000: b.append("Lökositoz")
if wbc < 4000: b.append("Lökopeni")
if plt < 140000: b.append("Trombositopeni")
if glu > 180: b.append("Hiperglisemi")
if na < 135: b.append("Hiponatremi")
if na > 146: b.append("Hipernatremi")
if ca > 10.4: b.append("Hiperkalsemi")
if ldh > 450: b.append("LDH Yüksekliği")
if ast_alt: b.append("Karaciğer Hasarı")
if trop: b.append("Kardiyak Hasar")

# 4. 100 HASTALIK MASTER DATABASE (MAGNUM VERSION)
master_db = {
    # GASTROENTEROLOJİ & HEPATOLOJİ
    "Üst GİS Kanama (Varis Dışı)": {"b": ["Hematemez", "Melena", "Anemi"], "t": "ÖGD", "ted": "IV PPI Bolus"},
    "Üst GİS Kanama (Varis)": {"b": ["Hematemez", "Melena", "Asit", "Sarılık"], "t": "Endoskopi + Doppler", "ted": "Terlipressin"},
    "Alt GİS Kanama": {"b": ["Hematokezya", "Melena"], "t": "Kolonoskopi", "ted": "Resusitasyon"},
    "Siroz": {"b": ["Asit", "Sarılık", "Asteriksis", "Karaciğer Hasarı"], "t": "USG + Biyokimya", "ted": "Diüretik + Laktüloz"},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Karın Ağrısı", "LDH Yüksekliği"], "t": "Lipaz + BT", "ted": "Hidrasyon"},
    "Wilson Hastalığı": {"b": ["Hepatomegali", "Tremor", "Karaciğer Hasarı"], "t": "Seruloplazmin", "ted": "Penisilamin"},
    "Hemokromatozis": {"b": ["Hiperpigmentasyon", "Hiperglisemi", "Karaciğer Hasarı"], "t": "Ferritin", "ted": "Flebotomi"},
    "PBK (Biliyer Kolanjit)": {"b": ["Sarılık", "Kaşıntı", "Karaciğer Hasarı"], "t": "AMA Antikoru", "ted": "Ursofalk"},
    "Akut KC Yetmezliği": {"b": ["Sarılık", "Konfüzyon", "Karaciğer Hasarı"], "t": "INR + Amonyak", "ted": "NAC"},
    "GÖRH": {"b": ["Göğüs Ağrısı", "Öksürük", "Disfaji"], "t": "Endoskopi", "ted": "PPI"},
    "Çölyak Hastalığı": {"b": ["Anemi", "Kilo Kaybı", "Karın Ağrısı"], "t": "Anti-tTG", "ted": "Glutensiz Diyet"},
    "Ülseratif Kolit": {"b": ["Hematokezya", "Karın Ağrısı", "Ateş (>38)"], "t": "Kolonoskopi", "ted": "5-ASA / Steroid"},
    "Crohn Hastalığı": {"b": ["Karın Ağrısı", "Kilo Kaybı", "Ateş (>38)"], "t": "BT Enterografi", "ted": "Anti-TNF"},
    
    # KARDİYOLOJİ
    "MI (Miyokard İnfarktüsü)": {"b": ["Göğüs Ağrısı", "Kardiyak Hasar"], "t": "Anjiyo", "ted": "Aspirin + PCI"},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Taşikardi"], "t": "BT Anjiyo", "ted": "Heparin"},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Hipotansiyon"], "t": "BT Anjiyo", "ted": "Beta Bloker"},
    "Kalp Yetersizliği": {"b": ["Nefes Darlığı", "Bilateral Ödem", "Boyun Ven Dolgunluğu"], "t": "Pro-BNP + EKO", "ted": "ACEi + Diüretik"},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm", "Peteşi"], "t": "EKO + Kültür", "ted": "Antibiyoterapi"},
    "Perikardit": {"b": ["Göğüs Ağrısı", "Plevritik Ağrı"], "t": "EKG + EKO", "ted": "NSAİİ + Kolşisin"},
    
    # NEFROLOJİ & HİPERTANSİYON
    "KBY (Kronik Böbrek Yetmezliği)": {"b": ["Renal Bozukluk", "Anemi", "Bilateral Ödem"], "t": "Renal USG", "ted": "Diyet + KBY Protokolü"},
    "Nefrotik Sendrom": {"b": ["Bilateral Ödem", "Renal Bozukluk"], "t": "İdrar Proteini", "ted": "Steroid"},
    "Piyelonefrit": {"b": ["Ateş (>38)", "Karın Ağrısı", "Lökositoz"], "t": "İdrar Kültürü", "ted": "Siprofloksasin"},
    "Renal Arter Stenozu": {"b": ["Hipotansiyon", "Renal Bozukluk", "Üfürüm"], "t": "Doppler USG", "ted": "Stent"},
    "Amiloidoz": {"b": ["Renal Bozukluk", "Bilateral Ödem", "Splenomegali"], "t": "Biyopsi", "ted": "KT"},
    
    # ENDOKRİNOLOJİ & METABOLİZMA
    "DKA (Ketoasidoz)": {"b": ["Aseton Kokusu", "Hiperglisemi", "Karın Ağrısı"], "t": "İdrar Ketoni", "ted": "İnsülin"},
    "HHS (Hiperozmolar)": {"b": ["Hiperglisemi", "Konfüzyon", "Hipernatremi"], "t": "Ozmolarite", "ted": "SF Hidrasyon"},
    "Addison Krizi": {"b": ["Hiperpigmentasyon", "Hipotansiyon", "Hiponatremi"], "t": "Kortizol", "ted": "Hidrokortizon"},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria", "Hiperglisemi"], "t": "Kortizol Testi", "ted": "Cerrahi"},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi", "Konfüzyon"], "t": "TFT", "ted": "PTU"},
    "Miksödem Koması": {"b": ["Konfüzyon", "Soğuk İntoleransı", "Bilateral Ödem"], "t": "TFT", "ted": "L-Tiroksin"},
    "Feokromositoma": {"b": ["Ani Baş Ağrısı", "Çarpıntı", "Terleme"], "t": "Metanefrin", "ted": "Alfa Bloker"},
    "Akromegali": {"b": ["El-Ayak Büyümesi", "Ani Baş Ağrısı"], "t": "IGF-1", "ted": "Cerrahi"},
    "Diyabet Şekersiz (DI)": {"b": ["Poliüri", "Polidipsi", "Hipernatremi"], "t": "Susuzluk Testi", "ted": "Desmopressin"},
    "Hiperkalsemik Kriz": {"b": ["Hiperkalsemi", "Konfüzyon", "Poliüri"], "t": "Ca + PTH", "ted": "Bisfosfonat"},
    "Primer Hiperparatiroidi": {"b": ["Hiperkalsemi", "Kemik Ağrısı"], "t": "PTH", "ted": "Cerrahi"},
    "Osteoporoz": {"b": ["Kemik Ağrısı", "Yaş > 60"], "t": "DEXA", "ted": "Kalsiyum + Vitamin D"},
    
    # HEMATOLOJİ & ONKOLOJİ
    "TTP (Purpura)": {"b": ["Trombositopeni", "Anemi", "Konfüzyon", "LDH Yüksekliği"], "t": "ADAMTS13", "ted": "Plazmaferez"},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Renal Bozukluk", "Hiperkalsemi", "Anemi"], "t": "Elektroforez", "ted": "KT"},
    "Lenfoma": {"b": ["Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi"], "t": "Biyopsi", "ted": "KT"},
    "Polisitemia Vera": {"b": ["Polisitemi", "Splenomegali", "Kaşıntı"], "t": "JAK2", "ted": "Flebotomi"},
    "İTP": {"b": ["Trombositopeni", "Peteşi", "Diş Eti Kanaması"], "t": "Klinik", "ted": "Steroid"},
    "Aplastik Anemi": {"b": ["Anemi", "Lökopeni", "Trombositopeni"], "t": "KİB", "ted": "KİT"},
    "DIC": {"b": ["Peteşi", "Diş Eti Kanaması", "Trombositopeni"], "t": "D-Dimer", "ted": "TDP"},
    "B12 Eksikliği": {"b": ["Anemi", "Konfüzyon", "Ataksi"], "t": "B12 Düzeyi", "ted": "Replasman"},
    "Demir Eksikliği": {"b": ["Anemi", "Solukluk", "Kaşıntı"], "t": "Ferritin", "ted": "Demir"},
    "AML / ALL": {"b": ["Lökositoz", "Anemi", "Trombositopeni", "Ateş (>38)"], "t": "KİB", "ted": "Kemoterapi"},
    
    # ROMATOLOJİ & İMMÜNOLOJİ
    "SLE (Lupus)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Lökopeni"], "t": "Anti-dsDNA", "ted": "Steroid"},
    "Behçet Hastalığı": {"b": ["Ağızda Aft", "Uveit", "Paterji Reaksiyonu"], "t": "HLA-B51", "ted": "Kolşisin"},
    "RA (Romatoid Artrit)": {"b": ["Sabah Sertliği", "Eklem Ağrısı"], "t": "RF + Anti-CCP", "ted": "Metotreksat"},
    "Sjögren": {"b": ["Göz Kuruluğu", "Ağızda Aft", "Eklem Ağrısı"], "t": "Anti-SSA", "ted": "Plaquenil"},
    "AS (Ankilozan Spondilit)": {"b": ["Sabah Sertliği", "Eklem Ağrısı", "Uveit"], "t": "HLA-B27", "ted": "Anti-TNF"},
    "GPA (Wegener)": {"b": ["Hemoptizi", "Renal Bozukluk", "Öksürük"], "t": "c-ANCA", "ted": "Pulse Steroid"},
    "Gut Artriti": {"b": ["Eklem Ağrısı", "Ateş (>38)"], "t": "Ürik Asit", "ted": "Kolşisin"},
    "Sarkoidoz": {"b": ["Nefes Darlığı", "Lenfadenopati", "Uveit"], "t": "ACE", "ted": "Steroid"},
    "Dermatomiyozit": {"b": ["Parezi", "Kelebek Döküntü", "Eklem Ağrısı"], "t": "CK", "ted": "Azatioprin"},
    "Skleroderma": {"b": ["Deri Sertleşmesi", "Raynaud", "Disfaji"], "t": "Anti-Scl-70", "ted": "Semptomatik"},
    
    # ENFEKSİYON & SEPSİS
    "Sepsis": {"b": ["Ateş (>38)", "Hipotansiyon", "Lökositoz"], "t": "Laktat", "ted": "Antibiyotik"},
    "Bruselloz": {"b": ["Ateş (>38)", "Eklem Ağrısı", "Splenomegali"], "t": "Wright Testi", "ted": "Rifampisin"},
    "Menenjit": {"b": ["Ense Sertliği", "Ani Baş Ağrısı", "Fotofobi"], "t": "LP", "ted": "Seftriakson"},
    "Sıtma": {"b": ["Ateş (>38)", "Splenomegali", "Sarılık"], "t": "Kalın Damla", "ted": "Artemisinin"},
}

# 5. ANALİZ MOTORU
if st.button("🚀 MAGNUM ANALİZİ BAŞLAT"):
    if not b:
        st.error("Lütfen klinik veri girişi yapınız!")
    else:
        results = []
        for ad, v in master_db.items():
            matches = set(b).intersection(set(v["b"]))
            if matches:
                score = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": score, "v": v, "m": list(matches)})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        col1, col2 = st.columns([1.6, 1])
        with col1:
            st.markdown("### 🏛️ Teşhis & Tedavi Matrisi")
            for r in results:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.5rem; font-weight:800; color:#000;'>{r['ad']} (%{r['puan']})</div>
                    <p style='color:#DC2626; font-weight:700;'>Eşleşen Bulgular: {", ".join(r['m'])}</p>
                    <hr style='border: 1px solid #DC2626;'>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['t']}</p>
                    <p>💊 <b>Tedavi Protokolü:</b> {r['v']['ted']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📝 EPİKRİZ RAPORU")
            epikriz = f"""TIBBİ ANALİZ (V24)\n------------------\nID: {p_no} | {datetime.now().strftime('%d/%m/%Y')}\nLAB: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}\n\nSEÇİLENLER:\n{", ".join(b)}\n\nÖN TANILAR:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in results[:8]])}\n\nİMZA: İSMAİL ORHAN"""
            st.markdown(f"<pre style='background:white; padding:30px; border:4px solid #DC2626; color:#000;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Kaydet", epikriz, file_name=f"{p_no}.txt")

st.markdown("---")
st.caption("GELİŞTİRİCİ: İSMAİL ORHAN  | 2026")
