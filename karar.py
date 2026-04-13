import streamlit as st
from datetime import datetime

# 1. ULTIMATE UI ARCHITECTURE (İSMAİL ORHAN - REDLINE & GOLD)
st.set_page_config(page_title="İSMAİL ORHAN | DAHİLİYE KLİNİK KARAR ROBOTU", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 30px; border-radius: 40px; text-align: center; margin-bottom: 30px;
        border-top: 15px solid #DC2626; border-bottom: 15px solid #DC2626; border-left: 8px solid #D4AF37; border-right: 8px solid #D4AF37;
        box-shadow: 0 45px 90px rgba(0,0,0,0.25);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 2.8rem; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.4rem; font-weight: 700; text-transform: uppercase; letter-spacing: 3px; }

    .clinical-card { 
        background: #FFFFFF; padding: 40px; border-radius: 45px; margin-bottom: 30px;
        border-left: 25px solid #DC2626; border-right: 12px solid #D4AF37;
        box-shadow: 15px 15px 40px rgba(0,0,0,0.08);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 40px;
        height: 6em; width: 100%; font-weight: 800; font-size: 30px; border: 5px solid #DC2626;
        box-shadow: 0 20px 40px rgba(220,38,38,0.2);
    }
    .stButton>button:hover { background: #DC2626; transform: scale(1.02); color: white; }
    
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 10px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KARAR DESTEK SİSTEMİ</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 2. YAN PANEL - LABORATUVAR TERMİNALİ
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR PANELİ")
    p_no = st.text_input("Protokol No", "İSMAİL-100-ULTRA")
    yas = st.number_input("Yaş", 0, 120, 50)
    kilo = st.number_input("Ağırlık (kg)", 5, 250, 80)
    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 40.0, 1.0)
    hb = st.number_input("Hemoglobin", 3.0, 25.0, 13.5)
    wbc = st.number_input("WBC (Lökosit)", 0, 500000, 7500)
    plt = st.number_input("PLT (Trombosit)", 0, 2000000, 250000)
    glu = st.number_input("Glukoz", 0, 3000, 110)
    na = st.number_input("Sodyum (Na)", 100, 180, 140)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.2)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 20.0, 9.6)
    ldh = st.number_input("LDH", 0, 10000, 220)
    ast_alt = st.checkbox("Transaminazlar (AST/ALT) > 3x")
    trop = st.checkbox("Kardiyak Belirteçler (Troponin) (+)")
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("eGFR Skoru", f"{egfr} ml/dk")
    if egfr < 15: st.error("DİYALİZ ENDİKASYONU OLABİLİR!")

# 3. GENİŞLETİLMİŞ KLİNİK BULGU PANELİ
st.subheader("🔍 Klinik Fenotip Seçimi (Tüm Sistemler)")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KALP", "🫁 AKCİĞER", "🤢 GİS-KC", "🧪 ENDO", "🧠 NÖRO", "🩸 HEMATO", "🧬 ROMATO-ENF"])

b = []
with t1: b.extend(st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "Bradikardi", "Taşikardi", "Üfürüm"]))
with t2: b.extend(st.multiselect("Pulmoner", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne"]))
with t3: b.extend(st.multiselect("Gastrointestinal", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound"]))
with t4: b.extend(st.multiselect("Endokrin", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "El-Ayak Büyümesi", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı"]))
with t5: b.extend(st.multiselect("Nörolojik", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği"]))
with t6: b.extend(st.multiselect("Hematolojik", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"]))
with t7: b.extend(st.multiselect("Romatoloji-Enf", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)"]))

# Lab Veri Entegrasyonu
if kre > 1.3: b.append("Böbrek Hasarı")
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
if ast_alt: b.append("KC Enzim Yüksekliği")
if trop: b.append("Kardiyak Hasar")

# 4. DEVASA 100 HASTALIK VERİTABANI (MASTER DATA)
master_db = {
    # --- KARDİYO & VASKÜLER ---
    "STEMI (Akut Miyokard İnfarktüsü)": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Kardiyak Hasar", "Taşikardi"], "t": "EKG + Troponin + Koroner Anjiyo", "ted": "ASA 300mg + Klopidogrel 600mg + IV Heparin + Acil PCI (Anjiyo)."},
    "NSTEMI / Kararsız Anjina": {"b": ["Göğüs Ağrısı", "Kardiyak Hasar"], "t": "Seri Troponin Takibi + EKG", "ted": "Düşük Molekül Ağırlıklı Heparin (Enoksaparin 1mg/kg 2x1) + Dual Antiagregan."},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Siyanoz", "Taşikardi"], "t": "BT Anjiyo + D-Dimer + Alt Ekstremite Venöz Doppler", "ted": "IV Heparin veya Trombolitik (Alteplaz 100mg) + O2."},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Göğüs Ağrısı", "Hipotansiyon", "Pupil Eşitsizliği"], "t": "Kontrastlı Toraks BT + TEE", "ted": "IV Beta Bloker (Esmolol) + Acil KVC Operasyonu."},
    "Akut Kalp Yetersizliği": {"b": ["Nefes Darlığı", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "Ral", "Ortopne"], "t": "proBNP + EKO + Telekardiyografi", "ted": "IV Furosemid 40-80mg Bolus + CPAP Desteği + IV Nitrat."},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm", "Peteşi", "Splenomegali"], "t": "Dük Kriterleri + EKO (Vejetasyon) + Kan Kültürü", "ted": "IV Vankomisin + Gentamisin (4-6 hafta)."},
    "Perikard Tamponadı": {"b": ["Hipotansiyon", "Boyun Ven Dolgunluğu", "Nefes Darlığı", "Bradikardi"], "t": "EKO (Plevral Efüzyon + Diastolik Kollaps)", "ted": "Acil Perikardiyosentez."},
    
    # --- GASTRO & HEPATOLOJİ ---
    "Varis Kanaması": {"b": ["Hematemez", "Melena", "Sarılık", "Asit", "Splenomegali"], "t": "Acil Endoskopi + Portal Doppler", "ted": "Terlipressin 2mg IV + Seftriakson 1g + Band Ligasyonu."},
    "Peptik Ülser Kanaması": {"b": ["Hematemez", "Melena", "Karın Ağrısı", "Anemi Bulgusu"], "t": "Endoskopi (Forrest Sınıflaması)", "ted": "IV PPI 80mg Bolus + 8mg/saat İnfüzyon + Adrenalin Enjeksiyonu."},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Karın Ağrısı", "LDH Yüksekliği", "Lökositoz"], "t": "Serum Amilaz/Lipaz (>3x) + Batın BT", "ted": "NPO (Aç Bırakma) + Agresif SF Hidrasyonu (250ml/saat) + Analjezi."},
    "Karaciğer Sirozu (Dekompanse)": {"b": ["Asit", "Sarılık", "Asteriksis", "KC Enzim Yüksekliği", "Splenomegali"], "t": "Albumin + INR + USG", "ted": "Spironolakton 100mg + Furosemid 40mg + Laktüloz."},
    "Akut Karaciğer Yetmezliği": {"b": ["Sarılık", "Konfüzyon", "KC Enzim Yüksekliği", "Asteriksis"], "t": "INR (>1.5) + Bilirubin + Amonyak", "ted": "N-Asetilsistein İnfüzyonu + KC Nakli Hazırlığı."},
    "Akut Kolanjit": {"b": ["Sarılık", "Ateş (>38)", "Karın Ağrısı", "Hipotansiyon", "Konfüzyon"], "t": "USG + ERCP", "ted": "Acil ERCP Drenaj + IV Seftriakson/Metronidazol."},
    "Çölyak Hastalığı": {"b": ["Anemi Bulgusu", "Karın Ağrısı", "Kilo Kaybı", "Kaşıntı"], "t": "Anti-tTG IgA + Duedonum Biyopsisi", "ted": "Ömür Boyu Glutensiz Diyet."},
    "Ülseratif Kolit": {"b": ["Hematokezya", "Karın Ağrısı", "Ateş (>38)", "Eklem Ağrısı"], "t": "Kolonoskopi + Biyopsi", "ted": "5-ASA (Mesalazin) + Steroid Enema."},
    "Crohn Hastalığı": {"b": ["Karın Ağrısı", "Kilo Kaybı", "Ateş (>38)", "Ağızda Aft"], "t": "BT Enterografi + Kolonoskopi", "ted": "Anti-TNF (İnfliksimab) + Azatioprin."},
    "Wilson Hastalığı": {"b": ["Hepatomegali", "Tremor", "Dizartri", "KC Enzim Yüksekliği"], "t": "Düşük Seruloplazmin + Kayser-Fleischer Halkası", "ted": "D-Penisilamin veya Çinko Tedavisi."},

    # --- ENDOKRİN & METABOLİZMA ---
    "Diyabetik Ketoasidoz (DKA)": {"b": ["Aseton Kokusu", "Hiperglisemi", "Karın Ağrısı", "Poliüri", "Konfüzyon"], "t": "Kan Gazı (Asidoz) + İdrarda Keton", "ted": "IV SF Hidrasyon + İnsülin İnfüzyonu (0.1 Ünite/kg/saat) + K+ Replasmanı."},
    "HHS (Hiperozmolar Durum)": {"b": ["Hiperglisemi", "Konfüzyon", "Hipernatremi", "Polidipsi"], "t": "Serum Ozmolaritesi (>320)", "ted": "Agresif SF Hidrasyon + Düşük Doz İnsülin."},
    "Addison Krizi": {"b": ["Hipotansiyon", "Hiperpigmentasyon", "Hiponatremi", "Karın Ağrısı"], "t": "Sabah Kortizolü + ACTH Stimülasyon Testi", "ted": "IV Hidrokortizon 100mg Bolus + SF."},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi", "Konfüzyon", "Sarılık", "Tremor"], "t": "Burch-Wartofsky Skoru + TSH/fT4", "ted": "PTU 200mg (4x1) + Lugol Solüsyonu + IV Propranolol."},
    "Miksödem Koması": {"b": ["Konfüzyon", "Soğuk İntoleransı", "Bilateral Ödem", "Bradikardi"], "t": "Çok Yüksek TSH + Düşük fT4", "ted": "IV L-Tiroksin + IV Steroid."},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria", "Hiperglisemi", "Hipotansiyon"], "t": "24 Saatlik İdrar Kortizolü + Dekzametazon Süpresyon", "ted": "Sürrenal veya Hipofiz Cerrahisi."},
    "Feokromositoma": {"b": ["Ani Baş Ağrısı", "Çarpıntı", "Terleme", "Hiperglisemi"], "t": "Plazma/İdrar Metanefrinleri + Batın BT", "ted": "Alfa Bloker (Fenoksibenzamin) -> 2 hafta sonra Cerrahi."},
    "Akromegali": {"b": ["El-Ayak Büyümesi", "Ani Baş Ağrısı", "Hiperglisemi", "Disfaji"], "t": "IGF-1 + Hipofiz MR", "ted": "Transsfenoidal Cerrahi + Somatostatin Analogları."},
    "Diabetes Insipidus (Şekersiz Şeker)": {"b": ["Poliüri", "Polidipsi", "Hipernatremi"], "t": "Susuzluk Testi + ADH Seviyesi", "ted": "Desmopressin (Minirin)."},
    "Hiperkalsemik Kriz": {"b": ["Hiperkalsemi", "Konfüzyon", "Poliüri", "Bradikardi"], "t": "İyonize Ca + PTH + LDH", "ted": "SF Hidrasyon + Zoledronik Asit + Kalsitonin."},

    # --- HEMATO & ONKO ---
    "TTP (Trombotik Trombositopenik Purpura)": {"b": ["Trombositopeni", "Anemi Bulgusu", "Konfüzyon", "Ateş (>38)", "LDH Yüksekliği", "Peteşi"], "t": "Periferik Yayma (Şistosit!) + ADAMTS13", "ted": "Acil Plazmaferez + Steroid + Rituksimab."},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Böbrek Hasarı", "Hiperkalsemi", "Anemi Bulgusu"], "t": "Protein Elektroforezi (M-Spike) + KİB", "ted": "VAD/VCD Protokolü + Bisfosfonat."},
    "Akut Lösemi (AML/ALL)": {"b": ["Anemi Bulgusu", "Trombositopeni", "Ateş (>38)", "Lökositoz", "Kemik Ağrısı"], "t": "Periferik Yayma + Kemik İliği Aspirasyonu", "ted": "7+3 İndüksiyon Kemoterapisi."},
    "Lenfoma (Hodgkin / Non-Hodgkin)": {"b": ["Lenfadenopati", "B Semptomları", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı"], "t": "Eksizyonel Lenf Nodu Biyopsisi + PET-BT", "ted": "ABVD veya R-CHOP Protokolü."},
    "Polisitemia Vera": {"b": ["Polisitemi Bulgusu", "Splenomegali", "Kaşıntı", "Ani Baş Ağrısı"], "t": "JAK2 Mutasyonu + KİB", "ted": "Flebotomi (Hct < 45) + Hidroksiüre."},
    "PNH (Paroksizmal Gece Hemoglobinürisi)": {"b": ["Anemi Bulgusu", "Hematokezya", "Karın Ağrısı", "Trombositopeni"], "t": "Akım Sitometrisi (CD55/CD59)", "ted": "Eculizumab + Antikoagülan."},
    "Aplastik Anemi": {"b": ["Anemi Bulgusu", "Lökopeni", "Trombositopeni", "Solukluk"], "t": "Kemik İliği Biyopsisi (Hiposelüler)", "ted": "İmmünsupresif Tedavi veya Kök Hücre Nakli."},
    "DIC (Yaygın Damar İçi Pıhtılaşma)": {"b": ["Peteşi", "Diş Eti Kanaması", "Trombositopeni", "LDH Yüksekliği"], "t": "D-Dimer + Fibrinojen", "ted": "TDP (Taze Donmuş Plazma) + Trombosit Süspansiyonu."},

    # --- ROMATO & NEFRO & ENFEKSİSYON ---
    "Sistemik Lupus (SLE)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Lökopeni", "Trombositopeni", "Renal Bozukluk"], "t": "ANA + Anti-dsDNA + C3-C4", "ted": "Plaquenil + Steroid + Mikofenolat Mofetil."},
    "Behçet Hastalığı (Nöro-Vasküler)": {"b": ["Ağızda Aft", "Uveit", "Eklem Ağrısı", "Paterji Reaksiyonu", "Konfüzyon"], "t": "HLA-B51 + Klinik Tanı", "ted": "Kolşisin + Azatioprin + Anti-TNF."},
    "Mikroskopik Polianjitis (MPA)": {"b": ["Hemoptizi", "Böbrek Hasarı", "Purpura", "Ateş (>38)"], "t": "p-ANCA + Biyopsi", "ted": "Siklofosfamid + Pulse Steroid."},
    "GPA (Wegener Vasküliti)": {"b": ["Hemoptizi", "Öksürük", "Böbrek Hasarı", "Lökositoz"], "t": "c-ANCA + Akciğer Biyopsisi", "ted": "Rituksimab + Steroid."},
    "Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon", "Lökositoz", "LDH Yüksekliği"], "t": "Laktat (>2) + Kan Kültürü", "ted": "30ml/kg SF Hidrasyon + IV Norepinefrin + Geniş Spektrumlu Antibiyotik."},
    "Bakteriyel Menenjit": {"b": ["Ense Sertliği", "Ateş (>38)", "Ani Baş Ağrısı", "Fotofobi", "Konfüzyon"], "t": "Lomber Ponksiyon (LP) + BOS Kültürü", "ted": "IV Seftriakson 2g (2x1) + Vankomisin + Deksametazon."},
    "Kronik Böbrek Yetmezliği (Evre 5)": {"b": ["Böbrek Hasarı", "Anemi Bulgusu", "Bilateral Ödem", "Hipotansiyon"], "t": "Renal USG + PTH", "ted": "Acil Diyaliz Endikasyonu + Tuz/Sıvı Kısıtı."},
    "Nefrotik Sendrom": {"b": ["Bilateral Ödem", "Böbrek Hasarı", "Hiperglisemi"], "t": "24 Saatlik İdrarda Protein (>3.5g)", "ted": "Steroid + ACE İnhibitörü."},
    "Bruselloz": {"b": ["Ateş (>38)", "Eklem Ağrısı", "Splenomegali", "Terleme"], "t": "Rose Bengal + Wright Aglütinasyon", "ted": "Doksisiklin + Rifampisin (6 hafta)."},
    "Sıtma (Malarya)": {"b": ["Ateş (>38)", "Splenomegali", "Sarılık", "Trombositopeni"], "t": "Periferik Yayma (Kalın Damla)", "ted": "Artemisinin Tabanlı Kombinasyon Tedavisi."},
    "Addison Hastalığı": {"b": ["Hipotansiyon", "Hiperpigmentasyon", "Hiponatremi", "Karın Ağrısı"], "t": "ACTH Stimülasyon Testi", "ted": "Hidrokortizon + Fludrokortizon."},
    "Ankilozan Spondilit": {"b": ["Bel Ağrısı (İnflamatuar)", "Sabah Sertliği", "Uveit"], "t": "HLA-B27 + Sakroiliak MR", "ted": "NSAİİ + Anti-TNF (Etanersept/Adalimumab)."},
    "Sarkoidoz": {"b": ["Nefes Darlığı", "Lenfadenopati", "Uveit", "Kuru Öksürük"], "t": "ACE Yüksekliği + Akciğer Grafisi (Bilateral Hiler LAP)", "ted": "Semptomatikse Oral Steroid."},
    "İdiyopatik Trombositopenik Purpura (İTP)": {"b": ["Trombositopeni", "Peteşi", "Diş Eti Kanaması"], "t": "Klinik Dışlama + Kemik İliği (Megakaryosit Artışı)", "ted": "Steroid (1mg/kg) + IVIG."},
    "Gut Artriti (Akut Atak)": {"b": ["Eklem Ağrısı", "Ateş (>38)", "Lökositoz"], "t": "Ürik Asit + Eklem Sıvısı Analizi", "ted": "Kolşisin + NSAİİ."},
    "Goodpasture Sendromu": {"b": ["Hemoptizi", "Böbrek Hasarı", "Anemi Bulgusu"], "t": "Anti-GBM Antikoru", "ted": "Plazmaferez + Steroid + Siklofosfamid."},
    "Miyastenia Gravis": {"b": ["Disfaji", "Dizartri", "Parezi", "Nefes Darlığı"], "t": "Anti-AChR Antikoru + Tensilon Testi", "ted": "Piridostigmin + Steroid."},
    "İnterstisyel Akciğer Hastalığı (İPH)": {"b": ["Nefes Darlığı", "Kuru Öksürük", "Ral"], "t": "Yüksek Çözünürlüklü BT (HRCT)", "ted": "Antifibrotik (Nintedanib) + Steroid."},
    "Raynaud Fenomeni (Sistemik Skleroz)": {"b": ["Raynaud", "Deri Sertleşmesi", "Disfaji"], "t": "Anti-Scl-70 + Kapilleroskopi", "ted": "Kalsiyum Kanal Blokeri + Bosentan."},
    "Dermatomiyozit": {"b": ["Parezi", "Kelebek Döküntü", "KC Enzim Yüksekliği"], "t": "CK Yüksekliği + Kas Biyopsisi", "ted": "Yüksek Doz Steroid + Azatioprin."},
}

# 5. ANALİZ VE RAPORLAMA MOTORU
if st.button("🚀 ANALİZİ BAŞLAT"):
    if not b:
        st.error("Lütfen klinik veri girişi yapınız!")
    else:
        results = []
        for ad, v in master_db.items():
            matches = set(b).intersection(set(v["b"]))
            if matches:
                # Doğruluk skoru: Eşleşenlerin toplam belirtilere oranı
                score = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": score, "v": v, "m": list(matches)})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        c1, c2 = st.columns([1.6, 1])
        with c1:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            if not results:
                st.warning("Eşleşen kritik tanı bulunamadı. Lütfen parametreleri kontrol edin.")
            for r in results:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.5rem; font-weight:800; color:#000;'>{r['ad']} (%{r['puan']})</div>
                    <p style='color:#DC2626; font-weight:700;'>TESPİT EDİLEN: {", ".join(r['m'])}</p>
                    <hr style='border: 1.5px solid #DC2626;'>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['t']}</p>
                    <p style='background:#FDF2F2; padding:20px; border-radius:20px; border-left:12px solid #DC2626;'>
                        💊 <b>DETAYLI PROTOKOL:</b> {r['v']['ted']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 RESMİ EPİKRİZ (V26)")
            epi = f"""TIBBİ ANALİZ RAPORU\n---------------------------\nID: {p_no} | {datetime.now().strftime('%d/%m/%Y %H:%M')}\nLAB: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}, Na {na}\neGFR: {egfr} ml/dk\n\nKLİNİK BULGULAR:\n{", ".join(b)}\n\nÖN TANILAR VE OLASILIKLAR:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in results[:12]])}\n\nİMZA: İSMAİL ORHAN\n---------------------------"""
            st.markdown(f"<pre style='background:white; padding:35px; border-radius:35px; border:6px solid #DC2626; color:#000; font-size:14px; white-space: pre-wrap;'>{epi}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Epikrizi Kaydet", epi, file_name=f"{p_no}_V26.txt")

st.markdown("---")
st.caption("GELİŞTİRİCİ: İSMAİL ORHAN | DAHİLİYE KLİNİK KARAR ROBOTU | 2026")
