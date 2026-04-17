import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API YAPILANDIRMASI
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY ekleyin!")

# 2. UI VE TASARIM
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE ROBOTU", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    .main-header { background: white; padding: 25px; border-radius: 20px; text-align: center; border-bottom: 10px solid #DC2626; }
    .clinical-card { background: #FFFFFF; padding: 25px; border-radius: 20px; margin-bottom: 20px; border-left: 20px solid #DC2626; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# 3. VERİ GİRİŞİ (WELLS VE GCS EKLENDİ)
with st.sidebar:
    st.header("📋 HASTA PARAMETRELERİ")
    p_no = st.text_input("Protokol No", "İSMAİL-V32")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    kilo = st.number_input("Kilo (kg)", 10, 250, 80)
    
    st.divider()
    st.subheader("📊 SKORLAMALAR")
    # GKS (Glaskow Koma Skoru)
    gcs = st.slider("GCS (Glaskow Koma Skoru)", 3, 15, 15)
    
    # Wells Skorlama
    w_puan = 0
    if st.checkbox("Aktif Kanser (+1)"): w_puan += 1
    if st.checkbox("Paralizi / İmmobilizasyon (+1)"): w_puan += 1
    if st.checkbox("Yatak Bağımlılığı >3 Gün (+1)"): w_puan += 1
    if st.checkbox("Venöz Hassasiyet (+1)"): w_puan += 1
    if st.checkbox("Tüm Bacakta Şişlik (+1)"): w_puan += 1
    if st.checkbox("Baldır Şişliği >3cm (+1)"): w_puan += 1
    if st.checkbox("Gode Bırakan Ödem (+1)"): w_puan += 1
    if st.checkbox("Kollateral Venler (+1)"): w_puan += 1
    if st.checkbox("Alternatif Tanı Olasılığı (-2)"): w_puan -= 2
    
    st.metric("Wells Skoru", w_puan)
    
    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 10.0, 1.0)
    egfr = round(((140 - yas) * kilo) / (72 * kre) * (0.85 if cinsiyet == "Kadın" else 1), 1)
    st.metric("eGFR Skoru", f"{egfr} ml/dk")

# 4. GÖRÜNTÜ YÜKLEME (AI İÇİN)
uploaded_file = st.file_uploader("📸 Görüntü (EKG/Röntgen) Analizi", type=["jpg", "jpeg", "png"])

# 5. SEMPTOM SEÇİCİ
st.subheader("🔍 Klinik Bulguları Seçin")
tabs = st.tabs(["🫀 KARDİYO", "🫁 PULM", "🤢 GİS", "🧪 ENDO", "🧠 NÖRO", "🩸 HEM", "🧬 ROM"])
secilenler = []
with tabs[0]: secilenler.extend(st.multiselect("KV", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Bradikardi", "Taşikardi", "Üfürüm"]))
with tabs[1]: secilenler.extend(st.multiselect("PULM", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne", "Hipoksi"]))
with tabs[2]: secilenler.extend(st.multiselect("GİS", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal", "Mide Bulantısı"]))
with tabs[3]: secilenler.extend(st.multiselect("ENDO", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi", "Galaktore"]))
with tabs[4]: secilenler.extend(st.multiselect("NÖRO", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik", "Pitozis"]))
with tabs[5]: secilenler.extend(st.multiselect("HEM", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"]))
with tabs[6]: secilenler.extend(st.multiselect("ROM", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)"]))

# 6. SENİN 85 HASTALIK MASTER LİSTEN (Eksiksiz Korumalı)
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

# 7. ANALİZ VE AI MOTORU
if st.button("🚀 TEŞHİS VE AI ANALİZİ BAŞLAT"):
    if not secilenler:
        st.error("Lütfen klinik bir bulgu seçin!")
    else:
        # Algoritmik Teşhis
        results = []
        for ad, v in master_db.items():
            matches = set(secilenler).intersection(set(v["b"]))
            if matches:
                puan = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": puan, "v": v, "m": list(matches)})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        c1, c2 = st.columns([1.8, 1])
        with c1:
            st.markdown("### 🏛️ Klinik Karar Paneli")
            for r in results[:10]:
                st.markdown(f"""
                <div class='clinical-card'>
                    <h2>{r['ad']} (%{r['puan']})</h2>
                    <p><b>Bulgular:</b> {", ".join(r['m'])}</p>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['t']}</p>
                    <p style='color:red;'>💊 <b>Acil Tedavi:</b> {r['v']['ted']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.markdown("### 🤖 GEMINI AI ANALİZ")
            with st.spinner("Görüntü ve Veriler İnceleniyor..."):
                try:
                    # Kütüphane güncelse bu satır hatasız çalışacaktır.
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Dahiliye uzmanı gibi davran. Hasta {yas}y {cinsiyet}, Wells: {w_puan}, GCS: {gcs}. Semptomlar: {', '.join(secilenler)}."
                    
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([prompt, img])
                    else:
                        response = model.generate_content(prompt)
                    st.info(response.text)
                except Exception as e:
                    st.error(f"AI Hatası: {e}")

st.divider()
st.caption("İSMAİL ORHAN DAHİLİYE PROJESİ | 2026")
