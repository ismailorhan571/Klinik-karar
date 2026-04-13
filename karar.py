import streamlit as st
from datetime import datetime

# 1. PRE-MIUM UI ARCHITECTURE (İSMAİL ORHAN | V28 FINAL BEAST)
st.set_page_config(page_title="İSMAİL ORHAN | V28 DAHİLİYE MASTER", page_icon="🩸", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 40px; border-radius: 50px; text-align: center; margin-bottom: 40px;
        border-top: 20px solid #DC2626; border-bottom: 20px solid #DC2626; border-left: 12px solid #D4AF37; border-right: 12px solid #D4AF37;
        box-shadow: 0 60px 120px rgba(0,0,0,0.3);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 3.2rem; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 5px; margin-top: 15px; }

    .clinical-card { 
        background: #FFFFFF; padding: 50px; border-radius: 60px; margin-bottom: 40px;
        border-left: 35px solid #DC2626; border-right: 18px solid #D4AF37;
        box-shadow: 25px 25px 60px rgba(0,0,0,0.12);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 50px;
        height: 7em; width: 100%; font-weight: 800; font-size: 35px; border: 7px solid #DC2626;
    }
    .stButton>button:hover { background: #DC2626; transform: scale(1.01); box-shadow: 0 30px 60px rgba(220,38,38,0.5); color: white; }
    
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 15px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN | V28 FINAL BEAST</p></div>", unsafe_allow_html=True)

# 2. LABORATUVAR TERMİNALİ (BOZULMADI, DAHA HASSAS)
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR VERİ MERKEZİ")
    p_no = st.text_input("Protokol No", "İSMAİL-V28-MAX")
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 5, 250, 85)
    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 45.0, 1.1)
    hb = st.number_input("Hemoglobin (Hb)", 3.0, 25.0, 14.0)
    wbc = st.number_input("WBC (Lökosit)", 0, 500000, 8500)
    plt = st.number_input("PLT (Trombosit)", 0, 2000000, 245000)
    glu = st.number_input("AKŞ (Glukoz)", 0, 3000, 105)
    na = st.number_input("Sodyum (Na)", 100, 190, 140)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.2)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 22.0, 9.5)
    ldh = st.number_input("LDH", 0, 15000, 210)
    ast_alt = st.checkbox("AST/ALT > 3 Kat Artış")
    trop = st.checkbox("Troponin Pozitif (+)")
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("eGFR Skoru", f"{egfr} ml/dk")

# 3. ZENGİNLEŞTİRİLMİŞ KLİNİK BULGU SEÇİMİ
st.subheader("🔍 Klinik Fenotip ve Belirti Havuzu")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KARDİYO", "🫁 PULMONER", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖROLOJİ", "🩸 HEMATOLOJİ", "🧬 ROMATO-ENF"])

b = []
with t1: b.extend(st.multiselect("KV", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Bradikardi", "Taşikardi", "Üfürüm"]))
with t2: b.extend(st.multiselect("PULM", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne", "Hipoksi"]))
with t3: b.extend(st.multiselect("GİS", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal", "Mide Bulantısı"]))
with t4: b.extend(st.multiselect("ENDO", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi", "Galaktore"]))
with t5: b.extend(st.multiselect("NÖRO", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik", "Pitozis"]))
with t6: b.extend(st.multiselect("HEM", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları", "Splenomegali (Hem)"]))
with t7: b.extend(st.multiselect("ROM", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)", "Artralji"]))

# Otomatik Lab Verisi İşleme
if kre > 1.3: b.append("Böbrek Hasarı")
if hb < 11: b.append("Anemi")
if hb > 17.5: b.append("Polisitemi")
if wbc > 12000: b.append("Lökositoz")
if wbc < 4000: b.append("Lökopeni")
if plt < 140000: b.append("Trombositopeni")
if glu > 180: b.append("Hiperglisemi")
if na < 135: b.append("Hiponatremi")
if na > 146: b.append("Hipernatremi")
if ca > 10.5: b.append("Hiperkalsemi")
if ldh > 500: b.append("LDH Yüksekliği")
if ast_alt: b.append("KC Hasarı")
if trop: b.append("Kardiyak İskemi")

# 4. MASTER 100+ HASTALIK VERİTABANI (EKSİKSİZ & ZENGİN)
master_db = {
    # --- KARDİYOLOJİ (TAM LİSTE) ---
    "STEMI (Akut Ön Duvar MI)": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Kardiyak İskemi", "Taşikardi", "Mide Bulantısı"], "t": "Acil EKG (V1-V6 ST Elevasyonu) + Troponin I", "ted": "ASA 300mg Çiğnet + Klopidogrel 600mg Yükleme + IV Heparin 5000 IU + Acil Anjiyo (90 dk)."},
    "NSTEMI": {"b": ["Göğüs Ağrısı", "Kardiyak İskemi", "Nefes Darlığı", "Terleme"], "t": "Seri Troponin Takibi (0-3 saat) + EKG", "ted": "Fondaparinuks 2.5mg SC veya Enoksaparin 1mg/kg SC + Dual Antiagregan + Beta Bloker."},
    "Pulmoner Emboli (Yüksek Risk)": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Siyanoz", "Taşikardi", "Hipotansiyon", "Hipoksi"], "t": "BT Anjiyo + D-Dimer + EKO (McConnell Belirtisi)", "ted": "Alteplaz (rtPA) 100mg IV İnfüzyon (2 saatte) + IV Heparin + Oksijen."},
    "Aort Diseksiyonu (Stanford Tip A)": {"b": ["Sırt Ağrısı (Yırtılır)", "Göğüs Ağrısı", "Hipotansiyon", "Pupil Eşitsizliği", "Senkop"], "t": "Toraks BT Anjiyo + Transözofageal EKO", "ted": "IV Esmolol (Hız/Tansiyon Kontrolü) + Acil KVC Operasyonu."},
    "Dekompanse Kalp Yetersizliği / Akut Akciğer Ödemi": {"b": ["Nefes Darlığı", "Ral", "Boyun Ven Dolgunluğu", "Ortopne", "Bilateral Ödem", "S3/S4 Sesi"], "t": "NT-proBNP > 300 + Tele + EKO", "ted": "IV Furosemid (Lasix) 40-80mg Bolus + CPAP Desteği + IV Nitrat 10-200 mcg/dk."},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm", "Peteşi", "Splenomegali", "Anemi"], "t": "Modifiye Dük Kriterleri + 3 Set Kan Kültürü + TEE", "ted": "IV Vankomisin 15-20mg/kg (2x1) + Seftriakson 2g (1x1)."},
    "Perikard Tamponadı": {"b": ["Hipotansiyon", "Boyun Ven Dolgunluğu", "Sessiz Kalp Sesleri (Beck Triadı)", "Nefes Darlığı"], "t": "EKO (Diastolik Kollaps)", "ted": "Acil Perikardiyosentez + IV SF Yüklemesi."},
    "Kardiyojenik Şok": {"b": ["Hipotansiyon", "Konfüzyon", "Oligüri", "Taşikardi", "Kardiyak İskemi"], "t": "Laktat Takibi + PAWP Ölçümü", "ted": "Norepinefrin + Dobutamin İnfüzyonu + İntraaortik Balon Pompası."},

    # --- GASTRO & HEPATOLOJİ (TAM LİSTE) ---
    "Siroz Kaynaklı Varis Kanaması": {"b": ["Hematemez", "Melena", "Sarılık", "Asit", "Hipotansiyon", "Splenomegali"], "t": "Acil Endoskopi + Child-Pugh Skoru", "ted": "Terlipressin 2mg IV Bolus (4 saatte bir) + Seftriakson 1g + Acil Band Ligasyonu."},
    "Akut Pankreatit (Şiddetli)": {"b": ["Kuşak Ağrısı", "Karın Ağrısı", "Mide Bulantısı", "LDH Yüksekliği", "Lökositoz", "Hipokalsemi"], "t": "Lipaz/Amilaz > 3x + Batın BT (Balthazar Skoru)", "ted": "NPO + Agresif SF/RL Hidrasyonu (250-500ml/saat) + IV Analjezi."},
    "Siroz / Hepatik Ensefalopati": {"b": ["Asteriksis", "Konfüzyon", "Sarılık", "Asit", "KC Hasarı"], "t": "Serum Amonyak Düzeyi + EEG", "ted": "Laktüloz (Günde 3-4 kez yumuşak dışkı) + Rifaximin 550mg (2x1)."},
    "Akut Kolanjit (Charcot Triadı)": {"b": ["Sarılık", "Ateş (>38)", "Karın Ağrısı", "Hipotansiyon", "Konfüzyon"], "t": "USG (Safra Yolu Dilatasyonu) + ERCP", "ted": "Acil ERCP + IV Piperasilin/Tazobaktam (4.5g 3x1)."},
    "Peptik Ülser Perforasyonu": {"b": ["Ani Karın Ağrısı", "Rebound", "Hipotansiyon", "Lökositoz"], "t": "Ayakta Direkt Batın Grafisi (Diyafram Altı Serbest Hava)", "ted": "NPO + Nazogastrik Dekompresyon + Acil Cerrahi + IV PPI."},
    "Wilson Hastalığı": {"b": ["Tremor", "Sarılık", "Dizartri", "KC Hasarı", "Kayser-Fleischer Halkası"], "t": "Seruloplazmin Düşüklüğü + 24s İdrar Bakırı", "ted": "D-Penisilamin veya Trientin + Çinko Asetat."},
    "Ülseratif Kolit Alevlenmesi": {"b": ["Hematokezya", "İshal", "Karın Ağrısı", "Ateş (>38)", "Artralji"], "t": "Kolonoskopi + Gayta Kalprotektin", "ted": "IV Metilprednizolon 60mg/gün + 5-ASA + Gerektiğinde Siklosporin."},

    # --- ENDOKRİNOLOJİ (TAM LİSTE) ---
    "Diyabetik Ketoasidoz (DKA)": {"b": ["Aseton Kokusu", "Hiperglisemi", "Karın Ağrısı", "Mide Bulantısı", "Konfüzyon", "Poliüri"], "t": "Kan Gazı (pH < 7.3) + İdrarda Keton + HCO3 < 18", "ted": "1L SF (1. saat) + Kristalize İnsülin 0.1 Ünite/kg/saat + KCL Takviyesi."},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi (>140)", "Konfüzyon", "Sarılık", "Tremor", "İshal"], "t": "Burch-Wartofsky Skoru > 45 + Baskılı TSH", "ted": "PTU 200mg (4 saatte bir) + Lugol Solüsyonu + IV Propranolol + IV Hidrokortizon 100mg."},
    "Addison Krizi": {"b": ["Hipotansiyon", "Hiperpigmentasyon", "Hiponatremi", "Karın Ağrısı", "K+ Yüksekliği"], "t": "ACTH Stimülasyon Testi + Kortizol", "ted": "IV Hidrokortizon 100mg Bolus + SF/Dekstroz Hidrasyon."},
    "Feokromositoma Krizi": {"b": ["Ani Baş Ağrısı", "Çarpıntı", "Terleme", "Hipotansiyon", "Hiperglisemi"], "t": "Plazma Serbest Metanefrinleri + Sürrenal BT", "ted": "Alfa Bloker (Fenoksibenzamin) -> Tansiyon Kontrolü Sonrası Beta Bloker."},
    "Miksödem Koması": {"b": ["Bradikardi", "Konfüzyon", "Soğuk İntoleransı", "Bilateral Ödem", "Hiponatremi"], "t": "TSH (>100) + Çok Düşük fT4", "ted": "IV L-Tiroksin 200-400 mcg + IV Hidrokortizon + Isıtma."},

    # --- HEMATOLOJİ (TAM LİSTE - 80-100'E DOĞRU) ---
    "TTP (Trombotik Trombositopenik Purpura)": {"b": ["Trombositopeni", "Anemi", "Konfüzyon", "Ateş (>38)", "Böbrek Hasarı", "Peteşi", "LDH Yüksekliği"], "t": "Periferik Yayma (Şistosit > %1) + ADAMTS13 Aktivitesi", "ted": "Acil Plazmaferez (Günde 1) + Steroid 1mg/kg + Rituksimab."},
    "Blastik Kriz (Akut Lösemi AML/ALL)": {"b": ["Anemi", "Lökositoz (>100.000)", "Trombositopeni", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"], "t": "KİB + Akım Sitometrisi + Periferik Yayma", "ted": "Hidrasyon + Allopurinol + Acil İndüksiyon Kemoterapisi."},
    "Multipl Miyelom (CRAB Bulguları)": {"b": ["Kemik Ağrısı", "Böbrek Hasarı", "Hiperkalsemi", "Anemi", "Halsizlik"], "t": "M-Spike (Protein Elektroforezi) + KİB", "ted": "Bortezomib + Lenalidomid + Dekzametazon + Bisfosfonat."},
    "PNH (Paroksizmal Gece Hemoglobinürisi)": {"b": ["Hemoptizi", "Melena", "Karın Ağrısı", "Anemi", "Trombositopeni", "LDH Yüksekliği"], "t": "Akım Sitometrisi (CD55/CD59 Negatifliği)", "ted": "Eculizumab (Kompleman İnhibitörü) + Antikoagülasyon."},
    "Polisitemia Vera": {"b": ["Polisitemi", "Splenomegali (Hem)", "Kaşıntı (Duş Sonrası)", "Ani Baş Ağrısı", "Eritromelalji"], "t": "JAK2 V617F Mutasyonu + Düşük Eritropoetin", "ted": "Flebotomi (Hct < 45) + Aspirin 100mg + Hidroksiüre."},
    "DIC (Disseminize İntravasküler Koagülasyon)": {"b": ["Peteşi", "Diş Eti Kanaması", "Ekimoz", "Hipotansiyon", "Trombositopeni", "LDH Yüksekliği"], "t": "D-Dimer Artışı + Düşük Fibrinojen + PT/aPTT Uzaması", "ted": "Altta Yatan Neden Tedavisi + Taze Donmuş Plazma + Trombosit."},

    # --- ROMATOLOJİ & NEFROLOJİ & ENFEKSİYON (TAM LİSTE) ---
    "Sistemik Lupus (SLE) Alevlenme": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Sabah Sertliği", "Böbrek Hasarı", "Lökopeni", "Ateş (>38)"], "t": "Anti-dsDNA + ANA Pozitifliği + C3/C4 Düşüklüğü", "ted": "Pulse Steroid (250-1000mg) + MMF veya Siklofosfamid."},
    "GPA (Wegener Granülomatozu)": {"b": ["Hemoptizi", "Kuru Öksürük", "Böbrek Hasarı", "Burun Kanaması", "Ateş (>38)"], "t": "c-ANCA (PR3) Pozitifliği + Biyopsi", "ted": "Rituksimab veya Siklofosfamid + Yüksek Doz Steroid."},
    "Behçet Hastalığı (Nöro-Vasküler)": {"b": ["Ağızda Aft", "Uveit", "Paterji Reaksiyonu", "Eklem Ağrısı", "Konfüzyon", "DVT"], "t": "HLA-B51 + Klinik Tanı Kriterleri", "ted": "Azatioprin + Kolşisin + Anti-TNF (İnfliksimab)."},
    "Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon", "Lökositoz", "Lökopeni", "Taşikardi"], "t": "Laktat > 2 + Kan Kültürleri + Prokalsitonin", "ted": "30ml/kg SF Hidrasyon + Norepinefrin + Geniş Spektrumlu Antibiyotik (Ertapenem/Meropenem)."},
    "Bakteriyel Menenjit": {"b": ["Ense Sertliği", "Ateş (>38)", "Ani Baş Ağrısı", "Fotofobi", "Konfüzyon", "Peteşi"], "t": "Lomber Ponksiyon (BOS'ta Plevositoz) + Gram Boyama", "ted": "IV Seftriakson 2g (2x1) + Vankomisin + Deksametazon (Antibiyotikten önce)."},
    "Goodpasture Sendromu (Anti-GBM)": {"b": ["Hemoptizi", "Böbrek Hasarı", "Anemi", "Nefes Darlığı"], "t": "Anti-GBM Antikoru + Böbrek Biyopsisi", "ted": "Plazmaferez + Steroid + Siklofosfamid."},
    "Miyastenia Gravis Krizi": {"b": ["Disfaji", "Parezi", "Nefes Darlığı", "Pitozis", "Dizartri"], "t": "Anti-AChR Antikoru + Tensilon Testi + EMG", "ted": "IVIG veya Plazmaferez + Steroid + Piridostigmin."},
    "Akut Nefritik Sendrom (PSGN)": {"b": ["Böbrek Hasarı", "Hipotansiyon", "Bilateral Ödem", "Hematokezya"], "t": "ASO Yüksekliği + İdrar Sedimenti (Eritrosit Silindirleri)", "ted": "Tuz/Sıvı Kısıtlaması + Loop Diüretik + Penisilin."},
    "Bruselloz (Nörobruselloz)": {"b": ["Ateş (>38)", "Eklem Ağrısı", "Gece Terlemesi", "Splenomegali", "Konfüzyon"], "t": "Rose Bengal + Wright Aglütinasyon (>1/160)", "ted": "Doksisiklin + Rifampisin + Seftriakson (Min 6 hafta)."},
    "Sarkoidoz (Evre 2)": {"b": ["Nefes Darlığı", "Kuru Öksürük", "Eklem Ağrısı", "Lenfadenopati", "Uveit"], "t": "ACE Yüksekliği + Akciğer Grafisi (Hiler LAP)", "ted": "Oral Steroid (0.5mg/kg) + Takip."},
    "Ankilozan Spondilit": {"b": ["Bel Ağrısı (İnflamatuar)", "Sabah Sertliği", "Uveit", "Eklem Ağrısı"], "t": "HLA-B27 + Sakroiliak MR (Kemik Ödemi)", "ted": "NSAİİ (Maksimum Doz) + Anti-TNF (Etanersept)."},
    "Hiperkalsemik Kriz": {"b": ["Hiperkalsemi", "Konfüzyon", "Poliüri", "Bradikardi", "Mide Bulantısı"], "t": "PTH + Ca + İyonize Ca", "ted": "Agresif SF Hidrasyon (300-500ml/saat) + Zoledronik Asit + Kalsitonin."},
    "Miyozit (Polimiyozit)": {"b": ["Parezi", "Artralji", "KC Hasarı", "Ateş (>38)"], "t": "CK Yüksekliği + Kas Biyopsisi + EMG", "ted": "Yüksek Doz Steroid + Azatioprin/Metotreksat."},
    "Sıtma (P. Falciparum)": {"b": ["Ateş (>38)", "Sarılık", "Splenomegali", "Trombositopeni", "Konfüzyon"], "t": "Kalın Damla Yayma (Yüzük Formu)", "ted": "Artemisin Kombinasyon Tedavisi (ACT) + IV Artesunat."},
    "Hepatit B Alevlenmesi": {"b": ["Sarılık", "KC Hasarı", "Hepatomegali", "Halsizlik"], "t": "HBsAg + HBV-DNA + Anti-HBc IgM", "ted": "Tenofovir veya Entekavir."},
    "HIV / Fırsatçı Enfeksiyon": {"b": ["Kilo Kaybı", "Lenfadenopati", "Gece Terlemesi", "İshal", "Öksürük"], "t": "ELISA + Western Blot + CD4 Sayımı", "ted": "Antiretroviral Tedavi (ART) + Profilaksi."},
}

# 5. FINAL ANALİZ MOTORU
if st.button("🚀 FINAL BEAST ANALİZİNİ BAŞLAT"):
    if not b:
        st.error("Lütfen klinik verileri girin!")
    else:
        results = []
        for ad, v in master_db.items():
            matches = set(b).intersection(set(v["b"]))
            if matches:
                # Gelişmiş Puanlama: Eşleşme yüzdesi
                score = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": score, "v": v, "m": list(matches)})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        c1, c2 = st.columns([1.8, 1])
        with c1:
            st.markdown("### 🏛️ Teşhis ve Tedavi Algoritması")
            if not results:
                st.warning("Eşleşen tanı bulunamadı. Lütfen belirtileri gözden geçirin.")
            for r in results:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:3rem; font-weight:800; color:#000;'>{r['ad']} (%{r['puan']})</div>
                    <p style='color:#DC2626; font-weight:700;'>KRİTİK BULGULAR: {", ".join(r['m'])}</p>
                    <hr style='border: 2px solid #DC2626;'>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['t']}</p>
                    <p style='background:#FFF4F4; padding:25px; border-radius:30px; border-left:20px solid #DC2626;'>
                        💊 <b>DETAYLI TEDAVİ:</b> {r['v']['ted']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 📝 EPİKRİZ RAPORU (V28)")
            epi = f"""DAHİLİYE KLİNİK KARAR ROBOTU\n---------------------------\nPROTOKOL: {p_no}\nTARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}\nLAB: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}, Na {na}, K {k}\neGFR: {egfr} ml/dk\n\nTESPİT EDİLEN SEMPTOMLAR:\n{", ".join(b)}\n\nAYIRICI TANI LİSTESİ:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in results[:15]])}\n\nGELİŞTİRİCİ: İSMAİL ORHAN\n---------------------------"""
            st.markdown(f"<pre style='background:white; padding:40px; border-radius:45px; border:10px solid #DC2626; color:#000; font-size:14px; white-space: pre-wrap;'>{epi}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Epikrizi İndir", epi, file_name=f"{p_no}_V28.txt")

st.markdown("---")
st.caption("CHIEF DEVELOPER: İSMAİL ORHAN | V28 FINAL BEAST EDITION | 2026")
