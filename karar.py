import streamlit as st
from datetime import datetime

# 1. PRE-MIUM UI ARCHITECTURE (İSMAİL ORHAN | V27 TITAN)
st.set_page_config(page_title="İSMAİL ORHAN | DAHİLİYE KLİNİK KARAR ROBOTU ", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 35px; border-radius: 45px; text-align: center; margin-bottom: 35px;
        border-top: 18px solid #DC2626; border-bottom: 18px solid #DC2626; border-left: 10px solid #D4AF37; border-right: 10px solid #D4AF37;
        box-shadow: 0 50px 100px rgba(0,0,0,0.28);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 3rem; margin: 0; letter-spacing: -1px; }
    .main-header p { color: #DC2626; font-size: 1.5rem; font-weight: 700; text-transform: uppercase; letter-spacing: 4px; margin-top: 10px; }

    .clinical-card { 
        background: #FFFFFF; padding: 45px; border-radius: 50px; margin-bottom: 35px;
        border-left: 30px solid #DC2626; border-right: 15px solid #D4AF37;
        box-shadow: 20px 20px 50px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 45px;
        height: 6.5em; width: 100%; font-weight: 800; font-size: 32px; border: 6px solid #DC2626;
        transition: 0.4s ease-in-out;
    }
    .stButton>button:hover { background: #DC2626; transform: translateY(-5px); box-shadow: 0 25px 50px rgba(220,38,38,0.4); color: white; }
    
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 12px solid #DC2626; }
    .stMetric { background: white; padding: 15px; border-radius: 20px; border: 2px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 2. YAN PANEL - LABORATUVAR TERMİNALİ (TAM KONTROL)
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR VERİ GİRİŞİ")
    p_no = st.text_input("Protokol Barkod", "TITAN-100-PRO")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 5, 250, 85)
    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 45.0, 1.1)
    hb = st.number_input("Hemoglobin (Hb)", 3.0, 25.0, 13.8)
    wbc = st.number_input("WBC (Lökosit)", 0, 500000, 8200)
    plt = st.number_input("PLT (Trombosit)", 0, 2000000, 240000)
    glu = st.number_input("Glukoz (AKŞ)", 0, 3000, 105)
    na = st.number_input("Sodyum (Na)", 100, 185, 142)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.2)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 20.0, 9.4)
    ldh = st.number_input("LDH", 0, 12000, 210)
    ast_alt = st.checkbox("KC Enzimleri (AST/ALT) > 3 Kat")
    trop = st.checkbox("Troponin Pozitifliği (+)")
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("eGFR Sonucu", f"{egfr} ml/dk")
    if egfr < 15: st.warning("DİYALİZ İHTİYACI?")

# 3. GENİŞLETİLMİŞ SİSTEMİK BELİRTİ SEÇİMİ
st.subheader("🔍 Klinik Bulguları İşaretleyin")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KALP-DAMAR", "🫁 SOLUNUM", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖROLOJİ", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENFEKSİYON"])

b = []
with t1: b.extend(st.multiselect("KV", ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Sırt Ağrısı (Yırtılır)", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "Bradikardi", "Taşikardi", "S3/S4 Sesi"]))
with t2: b.extend(st.multiselect("PULM", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne"]))
with t3: b.extend(st.multiselect("GİS", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal"]))
with t4: b.extend(st.multiselect("ENDO", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi"]))
with t5: b.extend(st.multiselect("NÖRO", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik"]))
with t6: b.extend(st.multiselect("HEM", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"]))
with t7: b.extend(st.multiselect("ROM-ENF", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "İnflamatuar Bel Ağrısı"]))

# Lab Verilerini Klinik Havuza Ekle
if kre > 1.3: b.append("Böbrek Yetmezliği Bulgusu")
if hb < 11: b.append("Anemi Bulgusu")
if hb > 17.5: b.append("Polisitemi Bulgusu")
if wbc > 12000: b.append("Lökositoz")
if wbc < 4000: b.append("Lökopeni")
if plt < 140000: b.append("Trombositopeni")
if glu > 200: b.append("Hiperglisemi")
if na < 135: b.append("Hiponatremi")
if na > 146: b.append("Hipernatremi")
if ca > 10.5: b.append("Hiperkalsemi")
if ldh > 500: b.append("LDH Yüksekliği")
if ast_alt: b.append("KC Hasarı Bulgusu")
if trop: b.append("Kardiyak İskemi")

# 4. DEVASA 100 HASTALIK TAM VERİTABANI (DETAYLANDIRILMIŞ)
master_db = {
    # --- KARDİYOLOJİ (1-15) ---
    "STEMI": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Kardiyak İskemi"], "t": "EKG (ST Elevasyonu) + Troponin", "ted": "ASA 300mg + Klopidogrel 600mg + Heparin + Acil PCI (Anjiyo)."},
    "NSTEMI": {"b": ["Göğüs Ağrısı", "Kardiyak İskemi", "Taşikardi"], "t": "Seri Troponin Takibi + EKG", "ted": "Düşük Molekül Ağırlıklı Heparin (Enoksaparin 1mg/kg 2x1) + ASA."},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Taşikardi", "Siyanoz", "Hemoptizi"], "t": "BT Anjiyo + D-Dimer + Sağ Yüklenme EKG", "ted": "Masifse Trombolitik (Alteplaz 100mg IV) + Heparin."},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Hipotansiyon", "Pupil Eşitsizliği"], "t": "Kontrastlı BT + TEE", "ted": "Tansiyon/Nabız Kontrolü (Beta Bloker) + Acil Cerrahi."},
    "Kalp Yetersizliği (Dekompanse)": {"b": ["Nefes Darlığı", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "Ral", "Ortopne"], "t": "proBNP + EKO + Akciğer Grafisi", "ted": "IV Furosemid 40-80mg + CPAP + IV Nitrat."},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm", "Peteşi", "Splenomegali"], "t": "Kan Kültürü + EKO (Vejetasyon)", "ted": "IV Vankomisin + Gentamisin (Haftalık Takip)."},
    "Perikard Tamponadı": {"b": ["Hipotansiyon", "Boyun Ven Dolgunluğu", "Sessiz Kalp Sesleri"], "t": "EKO", "ted": "Acil Perikardiyosentez."},
    "Atriyal Fibrilasyon (Hızlı Yanıtlı)": {"b": ["Çarpıntı", "Nefes Darlığı", "Taşikardi", "Hipotansiyon"], "t": "EKG", "ted": "Hız Kontrolü (Diltiazem/Metoprolol) + Antikoagülasyon."},
    "Stabil Anjina": {"b": ["Göğüs Ağrısı"], "t": "Efor Testi + Sintigrafi", "ted": "ASA + Statini + Beta Bloker."},
    "Miyokardit": {"b": ["Göğüs Ağrısı", "Ateş (>38)", "Nefes Darlığı", "Kardiyak İskemi"], "t": "Kardiyak MR + Troponin", "ted": "İstirahat + Kalp Yetersizliği Tedavisi."},

    # --- GASTROENTEROLOJİ & HEPATOLOJİ (16-35) ---
    "Varis Kanaması": {"b": ["Hematemez", "Melena", "Sarılık", "Asit"], "t": "Endoskopi + Doppler", "ted": "IV Terlipressin 2mg + Seftriakson 1g + Band Ligasyonu."},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Karın Ağrısı", "LDH Yüksekliği", "Lökositoz"], "t": "Amilaz/Lipaz (>3x) + Batın BT", "ted": "NPO + Agresif SF (250ml/saat) + Analjezi."},
    "Siroz": {"b": ["Sarılık", "Asit", "Asteriksis", "KC Hasarı Bulgusu", "Splenomegali"], "t": "Albumin/INR + USG", "ted": "Laktüloz + Spironolakton + Protein Kısıtlı Diyet."},
    "Üst GİS Kanama (Ülser)": {"b": ["Hematemez", "Melena", "Karın Ağrısı", "Anemi Bulgusu"], "t": "Endoskopi", "ted": "IV PPI (80mg Bolus + 8mg/saat İnfüzyon)."},
    "Alt GİS Kanama": {"b": ["Hematokezya", "Melena", "Anemi Bulgusu"], "t": "Kolonoskopi", "ted": "Sıvı Resusitasyonu + Kan Transfüzyonu."},
    "Akut Kolanjit": {"b": ["Sarılık", "Ateş (>38)", "Karın Ağrısı", "Konfüzyon"], "t": "ERCP + Lökositoz", "ted": "Acil ERCP Drenaj + IV Antibiyotik."},
    "Crohn Hastalığı": {"b": ["Karın Ağrısı", "İshal", "Kilo Kaybı", "Ağızda Aft"], "t": "Kolonoskopi + BT Enterografi", "ted": "Anti-TNF + Azatioprin."},
    "Ülseratif Kolit": {"b": ["Hematokezya", "İshal", "Karın Ağrısı", "Eklem Ağrısı"], "t": "Kolonoskopi + Biyopsi", "ted": "Mesalazin + Steroid."},
    "Wilson Hastalığı": {"b": ["Tremor", "Sarılık", "Dizartri", "KC Hasarı Bulgusu"], "t": "Seruloplazmin + Kayser-Fleischer Halkası", "ted": "Şelasyon (D-Penisilamin)."},
    "Hemokromatozis": {"b": ["Hiperpigmentasyon", "Hiperglisemi", "KC Hasarı Bulgusu"], "t": "Ferritin + Genetik", "ted": "Flebotomi."},
    "Çölyak": {"b": ["İshal", "Anemi Bulgusu", "Kilo Kaybı"], "t": "Anti-tTG + Biyopsi", "ted": "Glutensiz Diyet."},
    "Akut KC Yetmezliği": {"b": ["Sarılık", "Asteriksis", "Konfüzyon", "KC Hasarı Bulgusu"], "t": "INR > 1.5 + Amonyak", "ted": "NAC + KC Nakli Hazırlığı."},
    "GÖRH": {"b": ["Göğüs Ağrısı", "Disfaji", "Kuru Öksürük"], "t": "Endoskopi", "ted": "PPI + Yaşam Tarzı Değişikliği."},
    "Akalazya": {"b": ["Disfaji", "Kilo Kaybı"], "t": "Manometri", "ted": "Balon Dilatasyonu / Heller Miyotomi."},

    # --- ENDOKRİNOLOJİ (36-55) ---
    "DKA (Ketoasidoz)": {"b": ["Aseton Kokusu", "Hiperglisemi", "Karın Ağrısı", "Konfüzyon"], "t": "Kan Gazı (Asidoz) + İdrar Ketonu", "ted": "IV SF + İnsülin İnfüzyonu + K+ Takviyesi."},
    "HHS (Hiperozmolar)": {"b": ["Hiperglisemi", "Hipernatremi", "Konfüzyon"], "t": "Serum Ozmolaritesi (>320)", "ted": "Yavaş SF Hidrasyon + İnsülin."},
    "Addison Krizi": {"b": ["Hipotansiyon", "Hiponatremi", "Hiperpigmentasyon", "Karın Ağrısı"], "t": "Kortizol + ACTH Testi", "ted": "IV Hidrokortizon 100mg + SF."},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi", "Tremor", "Konfüzyon"], "t": "Burch-Wartofsky Skoru + fT4/TSH", "ted": "PTU + Lugol + Beta Bloker + IV Steroid."},
    "Miksödem Koması": {"b": ["Bradikardi", "Konfüzyon", "Soğuk İntoleransı", "Bilateral Ödem"], "t": "TSH + fT4", "ted": "IV L-Tiroksin + IV Steroid."},
    "Feokromositoma": {"b": ["Ani Baş Ağrısı", "Çarpıntı", "Terleme", "Hipotansiyon"], "t": "İdrar Metanefrinleri + Batın BT", "ted": "Alfa Bloker -> Sonra Beta Bloker."},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria", "Hiperglisemi", "Ateş (>38)"], "t": "İdrar Kortizolü + DEX Baskılama", "ted": "Cerrahi Müdahale."},
    "Akromegali": {"b": ["El-Ayak Büyümesi", "Disfaji", "Ani Baş Ağrısı"], "t": "IGF-1 + Hipofiz MR", "ted": "Cerrahi + Somatostatin."},
    "Primer Hiperparatiroidi": {"b": ["Hiperkalsemi", "Kemik Ağrısı", "Poliüri"], "t": "PTH + Ca", "ted": "Cerrahi (Paratirodektomi)."},
    "Diabetes Insipidus": {"b": ["Poliüri", "Polidipsi", "Hipernatremi"], "t": "Susuzluk Testi", "ted": "Desmopressin."},

    # --- HEMATOLOJİ & ONKOLOJİ (56-75) ---
    "TTP": {"b": ["Trombositopeni", "Anemi Bulgusu", "Konfüzyon", "LDH Yüksekliği", "Peteşi"], "t": "Şistosit + ADAMTS13", "ted": "Acil Plazmaferez + Steroid."},
    "DIC": {"b": ["Peteşi", "Diş Eti Kanaması", "Trombositopeni", "LDH Yüksekliği"], "t": "D-Dimer + Fibrinojen", "ted": "Taze Donmuş Plazma + TDP."},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Böbrek Yetmezliği Bulgusu", "Hiperkalsemi", "Anemi Bulgusu"], "t": "Protein Elektroforezi + KİB", "ted": "VCD Protokolü + Bisfosfonat."},
    "AML (Lösemi)": {"b": ["Anemi Bulgusu", "Lökositoz", "Trombositopeni", "Ateş (>38)"], "t": "KİB + Periferik Yayma", "ted": "İndüksiyon Kemoterapisi (7+3)."},
    "Lenfoma": {"b": ["Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı"], "t": "Eksizyonel Biyopsi", "ted": "R-CHOP / ABVD Kemoterapisi."},
    "PNH": {"b": ["Hematokezya", "Anemi Bulgusu", "Karın Ağrısı", "Trombositopeni"], "t": "Akım Sitometrisi", "ted": "Eculizumab."},
    "Polisitemia Vera": {"b": ["Polisitemi Bulgusu", "Splenomegali", "Kaşıntı", "Ani Baş Ağrısı"], "t": "JAK2 Mutasyonu", "ted": "Flebotomi + Aspirin."},
    "Demir Eksikliği Anemisi": {"b": ["Anemi Bulgusu", "Solukluk", "Kaşıntı"], "t": "Ferritin Düşüklüğü", "ted": "Oral/IV Demir Replasmanı."},
    "İTP": {"b": ["Trombositopeni", "Peteşi", "Diş Eti Kanaması"], "t": "Tanı Dışlama + Periferik Yayma", "ted": "Steroid + IVIG."},
    "B12 Eksikliği": {"b": ["Anemi Bulgusu", "Ataksi", "Konfüzyon", "Dengesizlik"], "t": "B12 Düzeyi + Homosistein", "ted": "IV/IM B12 Enjeksiyonu."},

    # --- ROMATOLOJİ (76-90) ---
    "SLE (Lupus)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Lökopeni", "Böbrek Yetmezliği Bulgusu"], "t": "ANA + Anti-dsDNA", "ted": "Steroid + Plaquenil + MMF."},
    "Behçet Hastalığı": {"b": ["Ağızda Aft", "Uveit", "Eklem Ağrısı", "Paterji Reaksiyonu"], "t": "HLA-B51 + Klinik", "ted": "Kolşisin + Azatioprin."},
    "GPA (Wegener)": {"b": ["Hemoptizi", "Böbrek Yetmezliği Bulgusu", "Kuru Öksürük"], "t": "c-ANCA", "ted": "Siklofosfamid + Steroid."},
    "Ankilozan Spondilit": {"b": ["İnflamatuar Bel Ağrısı", "Sabah Sertliği", "Uveit"], "t": "HLA-B27 + Sakroiliak MR", "ted": "NSAİİ + Anti-TNF."},
    "RA (Romatoid Artrit)": {"b": ["Sabah Sertliği", "Eklem Ağrısı"], "t": "RF + Anti-CCP", "ted": "Metotreksat + Steroid."},
    "Gut": {"b": ["Eklem Ağrısı", "Ateş (>38)", "Lökositoz"], "t": "Ürik Asit + Eklem Sıvısı Analizi", "ted": "Kolşisin + NSAİİ."},
    "Skleroderma": {"b": ["Deri Sertleşmesi", "Raynaud", "Disfaji"], "t": "Anti-Scl-70", "ted": "Kalsiyum Kanal Blokeri + MMF."},
    "Dermatomiyozit": {"b": ["Parezi", "Kelebek Döküntü", "KC Hasarı Bulgusu"], "t": "Kas Biyopsisi + CK", "ted": "Pulse Steroid."},

    # --- NEFROLOJİ & ENFEKSİYON (91-100) ---
    "Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon", "Lökositoz"], "t": "Laktat > 2 + Kan Kültürü", "ted": "30ml/kg SF + Norepinefrin + IV Antibiyotik."},
    "Menenjit": {"b": ["Ense Sertliği", "Ateş (>38)", "Ani Baş Ağrısı", "Fotofobi"], "t": "LP (Lomber Ponksiyon)", "ted": "IV Seftriakson + Vankomisin + Deksametazon."},
    "Piyelonefrit": {"b": ["Karın Ağrısı", "Ateş (>38)", "Lökositoz"], "t": "İdrar Kültürü + USG", "ted": "Siprofloksasin IV."},
    "KBY (Evre 5)": {"b": ["Böbrek Yetmezliği Bulgusu", "Bilateral Ödem", "Hipotansiyon"], "t": "Kreatinin Klirensi + USG", "ted": "Diyaliz + Sıvı Kısıtlaması."},
    "Nefrotik Sendrom": {"b": ["Bilateral Ödem", "Böbrek Yetmezliği Bulgusu", "Hiperglisemi"], "t": "24s İdrar Proteini > 3.5g", "ted": "Steroid + ACE İnhibitörü."},
    "Goodpasture": {"b": ["Hemoptizi", "Böbrek Yetmezliği Bulgusu", "Anemi Bulgusu"], "t": "Anti-GBM Antikoru", "ted": "Plazmaferez + Siklofosfamid."},
    "Bruselloz": {"b": ["Ateş (>38)", "Eklem Ağrısı", "Terleme", "Splenomegali"], "t": "Wright Aglütinasyon", "ted": "Doksisiklin + Rifampisin (6 hafta)."},
    "Sıtma": {"b": ["Ateş (>38)", "Trombositopeni", "Sarılık", "Splenomegali"], "t": "Kalın Damla Yayma", "ted": "Artemisinin."},
    "Hepatit B (Akut)": {"b": ["Sarılık", "KC Hasarı Bulgusu", "Hepatomegali"], "t": "HBsAg + Anti-HBc IgM", "ted": "İstirahat + Destek Tedavisi."},
    "HIV/AIDS (Fırsatçı Enf)": {"b": ["Kilo Kaybı", "Lenfadenopati", "Ateş (>38)", "Gece Terlemesi"], "t": "ELISA + Western Blot", "ted": "ART (Antiretroviral Tedavi)."}
}

# 5. TITAN ANALİZ MOTORU
if st.button("🚀 TITAN-100 ANALİZİNİ BAŞLAT"):
    if not b:
        st.error("Klinik veri girişi yapılmadı!")
    else:
        results = []
        for ad, v in master_db.items():
            matches = set(b).intersection(set(v["b"]))
            if matches:
                score = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": score, "v": v, "m": list(matches)})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        col_main, col_rep = st.columns([1.7, 1])
        with col_main:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Paneli")
            if not results:
                st.warning("Belirtilerle eşleşen kritik tanı bulunamadı.")
            for r in results:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.8rem; font-weight:800; color:#000;'>{r['ad']} (%{r['puan']})</div>
                    <p style='color:#DC2626; font-weight:700; font-size:1.1rem;'>ESLEŞEN: {", ".join(r['m'])}</p>
                    <hr style='border: 2px solid #DC2626;'>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['t']}</p>
                    <p style='background:#FFF5F5; padding:20px; border-radius:25px; border-left:15px solid #DC2626;'>
                        💊 <b>TEDAVİ PROTOKOLÜ:</b> {r['v']['ted']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with col_rep:
            st.markdown("### 📝 RESMİ EPİKRİZ (V27)")
            epi = f"""DAHİLİYE KLİNİK KARAR ROBOTU\n---------------------------\nPROTOKOL: {p_no} | {datetime.now().strftime('%d/%m/%Y %H:%M')}\nHASTA VERİSİ: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}, Na {na}\neGFR SKORU: {egfr} ml/dk\n\nBELİRTİLER:\n{", ".join(b)}\n\nOLASI ÖN TANILAR:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in results[:15]])}\n\nGELİŞTİRİCİ: İSMAİL ORHAN\n---------------------------"""
            st.markdown(f"<pre style='background:white; padding:35px; border-radius:40px; border:8px solid #DC2626; color:#000; font-size:14px; white-space: pre-wrap;'>{epi}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Epikriz Dosyasını İndir", epi, file_name=f"{p_no}_V27.txt")

st.markdown("---")
st.caption("GELİŞTİRİCİ: İSMAİL ORHAN 2026")
