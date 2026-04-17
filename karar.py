import streamlit as st
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# API YAPILANDIRMASI
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Secrets hatası! Lütfen API Key'i kontrol edin.")

# UI AYARLARI
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE ROBOTU", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    .main-header {
        background: white; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 20px;
        border-top: 10px solid #DC2626; border-bottom: 10px solid #DC2626; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .clinical-card { 
        background: white; padding: 25px; border-radius: 20px; margin-bottom: 20px;
        border-left: 15px solid #DC2626; box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# SIDEBAR - VERİ GİRİŞİ (GCS & WELLS DAHİL)
with st.sidebar:
    st.header("📋 HASTA VERİLERİ")
    p_no = st.text_input("Protokol No", "İSMAİL-AI-V32")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    kilo = st.number_input("Kilo (kg)", 10, 200, 80)
    
    st.divider()
    st.subheader("📊 SKORLAMALAR")
    gcs = st.slider("GCS (Glaskow Koma Skoru)", 3, 15, 15)
    
    # Wells Skorlama Mantığı
    w_list = [
        st.checkbox("Aktif Kanser (+1)"),
        st.checkbox("Paralizi / İmmobilizasyon (+1)"),
        st.checkbox("Yatak Bağımlılığı >3 Gün (+1)"),
        st.checkbox("Venöz Hassasiyet (+1)"),
        st.checkbox("Bacakta Şişlik (+1)"),
        st.checkbox("Baldır Şişliği >3cm (+1)"),
        st.checkbox("Gode Bırakan Ödem (+1)"),
        st.checkbox("Kollateral Venler (+1)")
    ]
    w_eksi = st.checkbox("Alternatif Tanı Olasılığı (-2)")
    wells_score = sum(w_list) + (-2 if w_eksi else 0)
    st.metric("Wells Skoru", wells_score)

    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 10.0, 1.0)
    hb = st.number_input("Hb", 5.0, 20.0, 14.0)
    wbc = st.number_input("WBC", 0, 50000, 8000)
    plt = st.number_input("PLT", 0, 1000000, 250000)
    
    egfr = round(((140 - yas) * kilo) / (72 * kre) * (0.85 if cinsiyet == "Kadın" else 1), 1)
    st.metric("eGFR", f"{egfr} ml/dk")

# GÖRÜNTÜ YÜKLEME
uploaded_file = st.file_uploader("📸 EKG veya Röntgen Yükle", type=["jpg", "jpeg", "png"])

# SEMPTOM SEÇİMİ (TÜM GRUPLAR)
st.subheader("🔍 Klinik Bulgular")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KARDİYO", "🫁 PULM", "🤢 GİS", "🧪 ENDO", "🧠 NÖRO", "🩸 HEM", "🧬 ROM"])
b = []
with t1: b.extend(st.multiselect("Bulgu", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Bradikardi", "Taşikardi", "Üfürüm"]))
with t2: b.extend(st.multiselect("Bulgu ", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne", "Hipoksi"]))
with t3: b.extend(st.multiselect("Bulgu  ", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal", "Mide Bulantısı"]))
with t4: b.extend(st.multiselect("Bulgu   ", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi", "Galaktore"]))
with t5: b.extend(st.multiselect("Bulgu    ", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik", "Pitozis"]))
with t6: b.extend(st.multiselect("Bulgu     ", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"]))
with t7: b.extend(st.multiselect("Bulgu      ", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)"]))

# 85 HASTALIK MASTER VERİTABANI (HİÇBİR DEĞİŞİKLİK YAPILMADI)
master_db = {
    "STEMI": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Kardiyak İskemi", "Terleme", "Taşikardi"], "t": "EKG + Troponin", "ted": "ASA 300mg + Klopidogrel 600mg + IV Heparin + Acil Anjiyo."},
    "NSTEMI": {"b": ["Göğüs Ağrısı", "Kardiyak İskemi", "Bulantı", "Nefes Darlığı"], "t": "Seri Troponin + EKG", "ted": "Enoksaparin 1mg/kg SC + ASA + Beta Bloker."},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Taşikardi", "Siyanoz", "Hipoksi"], "t": "BT Anjiyo + D-Dimer", "ted": "Alteplaz 100mg (Masifse) + IV Heparin."},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Hipotansiyon", "Pupil Eşitsizliği", "Senkop"], "t": "BT Anjiyo + TEE", "ted": "IV Esmolol + Acil Cerrahi."},
    "Akut Kalp Yetersizliği": {"b": ["Nefes Darlığı", "Ral", "Boyun Ven Dolgunluğu", "Ortopne", "Bilateral Ödem"], "t": "proBNP + EKO", "ted": "IV Furosemid 40-80mg + Nitrat + CPAP."},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm", "Peteşi", "Splenomegali", "Halsizlik"], "t": "Kan Kültürü + TEE", "ted": "IV Vankomisin + Seftriakson."},
    "Perikard Tamponadı": {"b": ["Hipotansiyon", "Boyun Ven Dolgunluğu", "Sessiz Kalp Sesleri", "Nefes Darlığı"], "t": "EKO", "ted": "Acil Perikardiyosentez."},
    "Atriyal Fibrilasyon (Hızlı)": {"b": ["Çarpıntı", "Nefes Darlığı", "Taşikardi", "Senkop"], "t": "EKG", "ted": "Metoprolol veya Diltiazem + Antikoagülan."},
    "Miyokardit": {"b": ["Göğüs Ağrısı", "Ateş (>38)", "Nefes Darlığı", "Kardiyak İskemi"], "t": "Kardiyak MR + Troponin", "ted": "İstirahat + Kalp Yetersizliği Tedavisi."},
    "Stabil Anjina": {"b": ["Göğüs Ağrısı", "Halsizlik"], "t": "Efor Testi", "ted": "ASA + Statini + Beta Bloker."},
    "Kardiyojenik Şok": {"b": ["Hipotansiyon", "Konfüzyon", "Taşikardi", "Oligüri"], "t": "Laktat + EKO", "ted": "Norepinefrin + Dobutamin."},
    "Hipertansif Acil Durum": {"b": ["Ani Baş Ağrısı", "Konfüzyon", "Göğüs Ağrısı", "Nefes Darlığı"], "t": "Tansiyon Takibi (>180/120)", "ted": "IV Nitroprussid veya Labetalol."},
    "Aort Stenozu": {"b": ["Senkop", "Göğüs Ağrısı", "Nefes Darlığı", "Üfürüm"], "t": "EKO", "ted": "Kapak Replasmanı (TAVI/Cerrahi)."},
    "Mitral Yetersizlik": {"b": ["Nefes Darlığı", "Ortopne", "Üfürüm", "Bilateral Ödem"], "t": "EKO", "ted": "Diüretik + ACE İnhibitörü + Cerrahi."},
    "Bradiaritmi (Tam Blok)": {"b": ["Bradikardi", "Senkop", "Hipotansiyon", "Konfüzyon"], "t": "EKG", "ted": "Atropin 0.5mg + Geçici Pacemaker."},
    "Varis Kanaması": {"b": ["Hematemez", "Melena", "Sarılık", "Asit", "Splenomegali"], "t": "Endoskopi", "ted": "IV Terlipressin 2mg + Seftriakson + Band Ligasyonu."},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Mide Bulantısı", "LDH Yüksekliği", "Lökositoz", "Karın Ağrısı"], "t": "Lipaz/Amilaz > 3x + BT", "ted": "NPO + Agresif SF (250ml/saat) + Analjezi."},
    "Hepatik Ensefalopati": {"b": ["Asteriksis", "Konfüzyon", "Sarılık", "Asit"], "t": "Amonyak", "ted": "Laktüloz + Rifaximin."},
    "Akut Kolanjit": {"b": ["Sarılık", "Ateş (>38)", "Karın Ağrısı", "Hipotansiyon", "Konfüzyon"], "t": "ERCP", "ted": "Acil ERCP + IV Antibiyotik."},
    "Peptik Ülser Kanaması": {"b": ["Hematemez", "Melena", "Karın Ağrısı", "Anemi"], "t": "Endoskopi", "ted": "IV PPI (80mg Bolus + 8mg/saat İnfüzyon)."},
    "Crohn Hastalığı": {"b": ["Karın Ağrısı", "İshal", "Kilo Kaybı", "Ağızda Aft"], "t": "BT Enterografi + Kolonoskopi", "ted": "Anti-TNF + Azatioprin."},
    "Ülseratif Kolit": {"b": ["Hematokezya", "İshal", "Karın Ağrısı", "Eklem Ağrısı"], "t": "Kolonoskopi", "ted": "Mesalazin + Steroid."},
    "Wilson Hastalığı": {"b": ["Tremor", "Sarılık", "Dizartri", "KC Hasarı"], "t": "Seruloplazmin + İdrar Bakırı", "ted": "D-Penisilamin + Çinko."},
    "Siroz": {"b": ["Sarılık", "Asit", "Hepatomegali", "Anemi", "Örümcek Anjiyom"], "t": "Albumin/INR + USG", "ted": "Spironolakton + Tuz Kısıtlaması."},
    "Akut Karaciğer Yetmezliği": {"b": ["Sarılık", "Konfüzyon", "KC Hasarı", "Asteriksis"], "t": "INR > 1.5", "ted": "NAC İnfüzyonu + Karaciğer Nakli."},
    "Çölyak": {"b": ["İshal", "Anemi", "Kilo Kaybı", "Karın Ağrısı"], "t": "Anti-tTG + Biyopsi", "ted": "Glutensiz Diyet."},
    "Akalazya": {"b": ["Disfaji", "Regürjitasyon", "Kilo Kaybı"], "t": "Manometri", "ted": "Balon Dilatasyonu / Heller."},
    "Gastroparezi": {"b": ["Mide Bulantısı", "Kusma", "Erken Doyma", "Karın Ağrısı"], "t": "Mide Boşalım Sintigrafisi", "ted": "Metoklopramid + Diyet."},
    "Hepatit B (Akut)": {"b": ["Sarılık", "Bulantı", "KC Hasarı", "İdrarda Koyu Renk"], "t": "Seroloji (HBsAg, Anti-HBc)", "ted": "Destek Tedavisi + İstirahat."},
    "Hepatit C (Kronik)": {"b": ["Halsizlik", "KC Hasarı", "Sarılık"], "t": "HCV-RNA", "ted": "Direkt Etkili Antiviraller (DAA)."},
    "Otoimmün Hepatit": {"b": ["Sarılık", "Eklem Ağrısı", "KC Hasarı", "Ateş (>38)"], "t": "ANA/ASMA + Biyopsi", "ted": "Steroid + Azatioprin."},
    "Primer Biliyer Kolanjit": {"b": ["Kaşıntı", "Sarılık", "Halsizlik", "Hepatomegali"], "t": "Anti-Mitokondriyal Antikor (AMA)", "ted": "Ursodeoksikolik Asit (UDCA)."},
    "Pankreas Kanseri": {"b": ["Sarılık", "Kuşak Ağrısı", "Kilo Kaybı", "Yeni Başlayan Diyabet"], "t": "Batın BT + CA 19-9", "ted": "Whipple Operasyonu / KT."},
    "Mezenter İskemi": {"b": ["Şiddetli Karın Ağrısı", "Bulantı", "Hipotansiyon", "Laktat Yüksekliği"], "t": "BT Anjiyo", "ted": "Acil Cerrahi / Embolektomi."},
    "Divertikülit": {"b": ["Karın Ağrısı", "Ateş (>38)", "Kabızlık", "Lökositoz"], "t": "Batın BT", "ted": "Antibiyotik + Sıvı Diyet."},
    "DKA": {"b": ["Aseton Kokusu", "Hiperglisemi", "Karın Ağrısı", "Konfüzyon", "Poliüri"], "t": "Kan Gazı + Keton", "ted": "IV SF + İnsülin İnfüzyonu + K+."},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi", "Konfüzyon", "Tremor", "Sarılık"], "t": "Burch-Wartofsky Skoru", "ted": "PTU + Lugol + Beta Bloker + IV Steroid."},
    "Addison Krizi": {"b": ["Hipotansiyon", "Hiperpigmentasyon", "Hiponatremi", "Karın Ağrısı"], "t": "Kortizol + ACTH Testi", "ted": "IV Hidrokortizon 100mg + SF."},
    "Miksödem Koması": {"b": ["Bradikardi", "Konfüzyon", "Soğuk İntoleransı", "Bilateral Ödem"], "t": "TSH + fT4", "ted": "IV L-Tiroksin + IV Steroid."},
    "Feokromositoma": {"b": ["Ani Baş Ağrısı", "Çarpıntı", "Terleme", "Hipotansiyon"], "t": "İdrar Metanefrinleri", "ted": "Alfa Bloker -> Beta Bloker."},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria", "Hiperglisemi", "Hipotansiyon"], "t": "DEX Baskılama Testi", "ted": "Cerrahi Müdahale."},
    "Diabetes Insipidus": {"b": ["Poliüri", "Polidipsi", "Hipernatremi"], "t": "Susuzluk Testi", "ted": "Desmopressin."},
    "Hiperkalsemik Kriz": {"b": ["Hiperkalsemi", "Konfüzyon", "Poliüri", "Bradikardi"], "t": "PTH + Ca", "ted": "SF Hidrasyon + Zoledronik Asit."},
    "Akromegali": {"b": ["El-Ayak Büyümesi", "Disfaji", "Ani Baş Ağrısı"], "t": "IGF-1 + MR", "ted": "Cerrahi + Somatostatin."},
    "Hipoglisemi Koması": {"b": ["Konfüzyon", "Terleme", "Taşikardi", "Nöbet"], "t": "Kan Şekeri < 50", "ted": "IV %10-20 Dekstroz Bolus."},
    "Primer Hiperaldosteronizm": {"b": ["Hipotansiyon", "Kas Güçsüzlüğü", "Poliüri"], "t": "Aldosteron/Renin Oranı", "ted": "Spironolakton / Cerrahi."},
    "Hipoparatiroidi": {"b": ["Kas Spazmı", "Nöbet", "Parezi"], "t": "Düşük Ca + Düşük PTH", "ted": "Kalsiyum + Vitamin D."},
    "Prolaktinoma": {"b": ["Galaktore", "Ani Baş Ağrısı", "Görme Bozukluğu"], "t": "Prolaktin + MR", "ted": "Kabergolin / Bromokriptin."},
    "SIADH": {"b": ["Hiponatremi", "Konfüzyon", "Nöbet", "Bulantı"], "t": "İdrar Sodyumu / Ozmolarite", "ted": "Sıvı Kısıtlaması + Tolvaptan."},
    "Hashimoto Tiroiditi": {"b": ["Halsizlik", "Soğuk İntoleransı", "Bilateral Ödem", "Kabızlık"], "t": "Anti-TPO + TSH", "ted": "Levotiroksin."},
    "TTP": {"b": ["Trombositopeni", "Anemi", "Konfüzyon", "Peteşi", "LDH Yüksekliği"], "t": "Şistosit + ADAMTS13", "ted": "Acil Plazmaferez + Steroid."},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Böbrek Hasarı", "Hiperkalsemi", "Anemi"], "t": "M-Spike + KİB", "ted": "VCD Protokolü + Bisfosfonat."},
    "AML": {"b": ["Anemi", "Lökositoz", "Trombositopeni", "Kemik Ağrısı", "Ateş (>38)"], "t": "KİB + Akım Sitometrisi", "ted": "Kemoterapi (7+3)."},
    "Lenfoma": {"b": ["Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Ateş (>38)"], "t": "Lenf Nodu Biyopsisi", "ted": "R-CHOP / ABVD."},
    "PNH": {"b": ["Hemoptizi", "Anemi", "Karın Ağrısı", "Trombositopeni"], "t": "CD55/CD59", "ted": "Eculizumab."},
    "DIC": {"b": ["Peteşi", "Diş Eti Kanaması", "Trombositopeni", "LDH Yüksekliği"], "t": "D-Dimer + Fibrinojen", "ted": "TDP + Trombosit + Neden Tedavisi."},
    "Polisitemia Vera": {"b": ["Polisitemi", "Splenomegali", "Kaşıntı", "Ani Baş Ağrısı"], "t": "JAK2 Mutasyonu", "ted": "Flebotomi + Aspirin."},
    "İTP": {"b": ["Trombositopeni", "Peteşi", "Diş Eti Kanaması"], "t": "Tanı Dışlama", "ted": "Steroid + IVIG."},
    "Aplastik Anemi": {"b": ["Anemi", "Lökopeni", "Trombositopeni", "Halsizlik"], "t": "Kemik İliği Biyopsisi", "ted": "Kök Hücre Nakli / ATG."},
    "B12 Eksikliği": {"b": ["Anemi", "Ataksi", "Dizartri", "Konfüzyon"], "t": "B12 Düzeyi", "ted": "IM B12 Enjeksiyonu."},
    "Hemofili A/B": {"b": ["Eklem Kanaması", "Ekimoz", "Diş Eti Kanaması"], "t": "Faktör Düzeyi + aPTT", "ted": "Faktör Replasmanı."},
    "Von Willebrand Hastalığı": {"b": ["Peteşi", "Burun Kanaması", "Diş Eti Kanaması"], "t": "vWF Aktivitesi", "ted": "Desmopressin / Faktör."},
    "Miyelodisplastik Sendrom (MDS)": {"b": ["Anemi", "Lökopeni", "Enfeksiyon Sıklığı", "Halsizlik"], "t": "Kemik İliği (Displazi)", "ted": "Azasitidin / Destek."},
    "Esansiyel Trombositemi": {"b": ["Trombositoz (>600k)", "Eritromelalji", "Ani Baş Ağrısı"], "t": "JAK2 / CALR Mutasyonu", "ted": "Hidroksiüre + Aspirin."},
    "Miyelofibrozis": {"b": ["Splenomegali", "Anemi", "Kilo Kaybı", "Kemik Ağrısı"], "t": "Kemik İliği (Kuru Aspirasyon)", "ted": "Ruxolitinib / Nakil."},
    "SLE (Lupus)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Böbrek Hasarı", "Lökopeni"], "t": "ANA + Anti-dsDNA", "ted": "Steroid + MMF + Plaquenil."},
    "Behçet Hastalığı": {"b": ["Ağızda Aft", "Uveit", "Paterji Reaksiyonu", "Eklem Ağrısı"], "t": "HLA-B51", "ted": "Kolşisin + Azatioprin."},
    "Ankilozan Spondilit": {"b": ["Bel Ağrısı (İnflamatuar)", "Sabah Sertliği", "Uveit"], "t": "HLA-B27 + MR", "ted": "NSAİİ + Anti-TNF."},
    "GPA (Wegener)": {"b": ["Hemoptizi", "Böbrek Hasarı", "Kuru Öksürük", "Burun Kanaması"], "t": "c-ANCA", "ted": "Rituksimab + Steroid."},
    "Sjögren Sendromu": {"b": ["Göz Kuruluğu", "Ağız Kuruluğu", "Artralji", "Lenfadenopati"], "t": "Anti-SSA/SSB + Schirmer Testi", "ted": "Suni Gözyaşı + Plaquenil."},
    "Skleroderma": {"b": ["Deri Sertleşmesi", "Raynaud", "Disfaji", "Nefes Darlığı"], "t": "Anti-Scl-70", "ted": "MMF + Kalsiyum Kanal Blokeri."},
    "Dermatomiyozit": {"b": ["Parezi", "Kelebek Döküntü", "KC Hasarı", "Artralji"], "t": "CK + Kas Biyopsisi", "ted": "Yüksek Doz Steroid."},
    "Gut Artriti": {"b": ["Eklem Ağrısı", "Ateş (>38)", "Lökositoz"], "t": "Ürik Asit + Eklem Sıvısı", "ted": "Kolşisin + NSAİİ."},
    "Romatoid Artrit": {"b": ["Eklem Ağrısı", "Sabah Sertliği", "Halsizlik"], "t": "RF + Anti-CCP", "ted": "Metotreksat + Steroid."},
    "Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon", "Taşikardi"], "t": "Laktat > 2 + Kültür", "ted": "30ml/kg SF + Norepinefrin + Antibiyotik."},
    "Bakteriyel Menenjit": {"b": ["Ense Sertliği", "Ateş (>38)", "Ani Baş Ağrısı", "Fotofobi"], "t": "Lomber Ponksiyon", "ted": "IV Seftriakson + Vankomisin."},
    "Goodpasture": {"b": ["Hemoptizi", "Böbrek Hasarı", "Nefes Darlığı", "Anemi"], "t": "Anti-GBM Antikoru", "ted": "Plazmaferez + Steroid."},
    "Miyastenia Gravis": {"b": ["Parezi", "Disfaji", "Pitozis", "Nefes Darlığı"], "t": "Anti-AChR + Tensilon", "ted": "Piridostigmin + IVIG."},
    "Bruselloz": {"b": ["Ateş (>38)", "Eklem Ağrısı", "Terleme", "Splenomegali"], "t": "Rose Bengal + Wright", "ted": "Doksisiklin + Rifampisin."},
    "Sıtma": {"b": ["Ateş (>38)", "Sarılık", "Splenomegali", "Trombositopeni"], "t": "Kalın Damla Yayma", "ted": "Artemisin."},
    "KBY (Evre 5)": {"b": ["Böbrek Hasarı", "Bilateral Ödem", "Hipotansiyon", "Anemi"], "t": "eGFR < 15", "ted": "Acil Diyaliz + Sıvı Kısıtlaması."},
    "Nefrotik Sendrom": {"b": ["Bilateral Ödem", "Böbrek Hasarı", "Halsizlik"], "t": "24s Protein > 3.5g", "ted": "Steroid + ACE İnhibitörü."},
    "Piyelonefrit": {"b": ["Karın Ağrısı", "Ateş (>38)", "Bulantı", "Lökositoz"], "t": "İdrar Kültürü", "ted": "IV Siprofloksasin / Seftriakson."},
    "İnterstisyel Akciğer Hastalığı": {"b": ["Nefes Darlığı", "Kuru Öksürük", "Ral", "Çomak Parmak"], "t": "HRCT (BT)", "ted": "Steroid + Nintedanib."},
    "Sarkoidoz": {"b": ["Nefes Darlığı", "Lenfadenopati", "Uveit", "Kuru Öksürük"], "t": "ACE + Akciğer Grafisi", "ted": "Oral Steroid."},
}

# ANALİZ BUTONU
if st.button("🚀 ANALİZİ BAŞLAT"):
    if not b:
        st.warning("Lütfen en az bir bulgu seçin.")
    else:
        # Puanlama Mantığı
        sonuclar = []
        for ad, veri in master_db.items():
            eslesme = set(b).intersection(set(veri["b"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["b"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "detay": veri, "eslesen": list(eslesme)})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🏥 Olası Teşhisler")
            for s in sonuclar[:10]:
                st.markdown(f"""
                <div class='clinical-card'>
                    <h3>{s['ad']} (%{s['puan']})</h3>
                    <p><b>Bulgular:</b> {", ".join(s['eslesen'])}</p>
                    <p>🧪 <b>Tetkik:</b> {s['detay']['t']}</p>
                    <p style='color:red;'>💊 <b>Tedavi:</b> {s['detay']['ted']}</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.subheader("🤖 AI Analizi")
            with st.spinner("AI analiz yapıyor..."):
                try:
                    # KESİN ÇÖZÜM: Kütüphane güncelse bu satır hatasız çalışacaktır.
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    txt = f"Vaka: {yas}y {cinsiyet}, Wells: {wells_score}, GCS: {gcs}. Semptomlar: {', '.join(b)}."
                    
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        res = model.generate_content([txt, img])
                    else:
                        res = model.generate_content(txt)
                    st.write(res.text)
                except Exception as e:
                    st.error(f"AI Hatası: {e}")

            st.download_button("📥 Epikrizi İndir", f"PROTOKOL: {p_no}\nTEŞHİSLER: {sonuclar[0]['ad'] if sonuclar else 'Bulunamadı'}", file_name="epikriz.txt")

st.caption("GELİŞTİRİCİ: İSMAİL ORHAN | 2026")
