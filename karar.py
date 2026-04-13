import streamlit as st
from datetime import datetime

# 1. PREMIUM UI ARCHITECTURE (İSMAİL ORHAN SIGNATURE)
st.set_page_config(page_title="İSMAİL ORHAN | V23 ULTIMATE DAHİLİYE", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 30px; border-radius: 40px; text-align: center; margin-bottom: 30px;
        border-top: 12px solid #DC2626; border-bottom: 12px solid #DC2626; border-left: 6px solid #D4AF37; border-right: 6px solid #D4AF37;
        box-shadow: 0 45px 90px rgba(0,0,0,0.18);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 2.8rem; margin: 0; letter-spacing: -1px; }
    .main-header p { color: #DC2626; font-size: 1.3rem; font-weight: 700; text-transform: uppercase; margin-top: 5px; }

    .clinical-card { 
        background: #FFFFFF; padding: 40px; border-radius: 45px; margin-bottom: 30px;
        border-left: 22px solid #DC2626; border-right: 10px solid #D4AF37;
        box-shadow: 15px 15px 45px rgba(0,0,0,0.08); transition: 0.3s;
    }
    .clinical-card:hover { transform: translateY(-5px); box-shadow: 20px 20px 60px rgba(0,0,0,0.12); }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 40px;
        height: 6.5em; width: 100%; font-weight: 800; font-size: 30px; border: 5px solid #DC2626;
        box-shadow: 0 25px 50px rgba(220,38,38,0.3);
    }
    .stButton>button:hover { background: #DC2626; box-shadow: 0 30px 60px rgba(220,38,38,0.5); }
    
    [data-testid="stSidebar"] { background-color: #F9F8F0; border-right: 8px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>DAHİLİYE KARAR DESTEK ROBOTU</h1><p>CHIEF DEVELOPER: İSMAİL ORHAN | V23 - 50+ HASTALIK MODU</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL - KAN SONUÇLARI (BOZULMADI, KAPSAM GENİŞLEDİ)
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR TERMİNALİ")
    p_no = st.text_input("Barkod/ID", "IO-V23-ULTIMATE")
    yas = st.number_input("Yaş", 0, 120, 55)
    kilo = st.number_input("Kilo (kg)", 5, 250, 80)
    
    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 40.0, 1.1)
    hb = st.number_input("Hemoglobin", 3.0, 25.0, 13.5)
    wbc = st.number_input("Lökosit (WBC)", 0, 500000, 7800)
    plt = st.number_input("Trombosit (PLT)", 0, 2000000, 240000)
    glu = st.number_input("Glukoz (mg/dL)", 0, 3000, 105)
    na = st.number_input("Sodyum (Na)", 100, 180, 142)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.2)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 20.0, 9.4)
    ldh = st.number_input("LDH", 0, 10000, 220)
    ast_alt = st.checkbox("AST/ALT > 100")
    trop = st.checkbox("Troponin (+) / CK-MB")
    
    egfr = round(((140 - yas) * kilo) / (72 * kre), 1) if kre > 0 else 0
    st.metric("eGFR Skoru", f"{egfr} ml/dk")
    if egfr < 15: st.error("🚨 EVRE 5 KBY - ACİL DİYALİZ?")

# 4. DEVASA BELİRTİ VE BULGU ÜSSÜ
st.subheader("🔍 Klinik Fenotip ve Fizik Muayene")
tabs = st.tabs(["🫀 KALP-DAMAR", "🫁 AKCİĞER", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖROLOJİ", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENFEKSİYON"])

b = []
with tabs[0]: b.extend(st.multiselect("KV Sistem", ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Sırt Ağrısı (Yırtılır)", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "Üfürüm", "Bradikardi", "Taşikardi"]))
with tabs[1]: b.extend(st.multiselect("Solunum", ["Nefes Darlığı", "Hemoptizi", "Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz"]))
with tabs[2]: b.extend(st.multiselect("Gastro", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Karın Ağrısı", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Rebound/Defans", "Murphy Belirtisi"]))
with tabs[3]: b.extend(st.multiselect("Endokrin", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Galaktore", "El-Ayak Büyümesi", "Tremor", "Soğuk İntoleransı"]))
with tabs[4]: b.extend(st.multiselect("Nöro", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Pupil Eşitsizliği", "Parezi/Paralizi"]))
with tabs[5]: b.extend(st.multiselect("Hemat-Onko", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"]))
with tabs[6]: b.extend(st.multiselect("Romato-Enf", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu"]))

# Kan Sonuçlarını Algoritmaya Bağla
if kre > 1.4: b.append("Renal Disfonksiyon")
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
if ast_alt: b.append("KC Enzim Yüksekliği")
if trop: b.append("Kardiyak İskemi Bulgusu")

# 5. MEGA MASTER DATABASE (50+ HASTALIK)
master_db = {
    "Üst GİS Kanama (Varis Dışı)": {"b": ["Hematemez", "Melena", "Anemi"], "t": "ÖGD (Endoskopi)", "ted": "IV PPI (80mg Bolus + 8mg/saat)"},
    "Üst GİS Kanama (Varis)": {"b": ["Hematemez", "Melena", "Sarılık", "Asit", "Splenomegali"], "t": "Endoskopi + Doppler USG", "ted": "Terlipressin + Seftriakson + Band Ligasyonu"},
    "Alt GİS Kanama": {"b": ["Hematokezya", "Melena"], "t": "Kolonoskopi + BT Anjiyo", "ted": "Hidrasyon + Gerekirse Embolizasyon"},
    "Miyokard İnfarktüsü (MI)": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Kardiyak İskemi Bulgusu"], "t": "EKG + Troponin + Anjiyo", "ted": "Aspirin + Klopidogrel + Heparin + PCI"},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Taşikardi"], "t": "BT Anjiyo + D-Dimer", "ted": "Enoksaparin (1mg/kg 2x1)"},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Hipotansiyon", "Göğüs Ağrısı"], "t": "BT Anjiyo (Tüm Aorta)", "ted": "Esmolol + Acil Cerrahi"},
    "Sepsis / Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon", "Lökositoz"], "t": "Laktat + Kültürler", "ted": "Erken Antibiyotik + 30ml/kg Sıvı"},
    "Diyabetik Ketoasidoz (DKA)": {"b": ["Aseton Kokusu", "Hiperglisemi", "Karın Ağrısı", "Poliüri"], "t": "Kan Gazı + İdrar Ketoni", "ted": "İnsülin Perfüzyon + SF + K+"},
    "HHS (Hiperozmolar Durum)": {"b": ["Hiperglisemi", "Konfüzyon", "Hipernatremi", "Polidipsi"], "t": "Serum Ozmolaritesi", "ted": "Agresif SF + Düşük Doz İnsülin"},
    "KBY (Kronik Böbrek Yetmezliği)": {"b": ["Renal Disfonksiyon", "Bilateral Ödem", "Anemi"], "t": "Renal USG + PTH", "ted": "Tuz Kısıtı + KBY Protokolü"},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Karın Ağrısı", "LDH Yüksekliği"], "t": "Amilaz/Lipaz + Batın BT", "ted": "NPO + Agresif Sıvı"},
    "Karaciğer Sirozu": {"b": ["Asit", "Sarılık", "Asteriksis", "KC Enzim Yüksekliği"], "t": "Bilirubin + INR + USG", "ted": "Spironolakton + Laktüloz"},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Renal Disfonksiyon", "Hiperkalsemi", "Anemi"], "t": "Protein Elektroforezi + KİB", "ted": "KT + Bisfosfonat"},
    "Lenfoma (Hodgkin/NH)": {"b": ["Lenfadenopati", "B Semptomları", "Kilo Kaybı", "Kaşıntı"], "t": "Eksizyonel Biyopsi + PET-BT", "ted": "Kemoterapi (CHOP/ABVD)"},
    "TTP (Trombotik Trombositopenik Purpura)": {"b": ["Trombositopeni", "Anemi", "Konfüzyon", "Ateş (>38)", "LDH Yüksekliği"], "t": "Şistosit + ADAMTS13", "ted": "Plazmaferez + Steroid"},
    "Sistemik Lupus (SLE)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Lökopeni", "Trombositopeni"], "t": "ANA + Anti-dsDNA", "ted": "Hidroksiklorokin + Steroid"},
    "Behçet Hastalığı": {"b": ["Ağızda Aft", "Uveit", "Eklem Ağrısı", "Paterji Reaksiyonu"], "t": "Klinik Tanı + HLA-B51", "ted": "Kolşisin + İmmünsupresif"},
    "GPA (Wegener Vasküliti)": {"b": ["Hemoptizi", "Renal Disfonksiyon", "Öksürük", "Anemi"], "t": "c-ANCA + Biyopsi", "ted": "Siklofosfamid + Pulse Steroid"},
    "Hiperkalsemik Kriz": {"b": ["Hiperkalsemi", "Konfüzyon", "Poliüri", "Bradikardi"], "t": "İonize Ca + PTH", "ted": "SF + Zoledronik Asit + Kalsitonin"},
    "Addison Krizi": {"b": ["Hiperpigmentasyon", "Hipotansiyon", "Hiponatremi", "Karın Ağrısı"], "t": "Kortizol + ACTH Stim", "ted": "IV Hidrokortizon 100mg"},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi", "Konfüzyon", "Sarılık"], "t": "TSH + sT4 + Burch-Wartofsky", "ted": "PTU + Lugol + Propranolol"},
    "Miksödem Koması": {"b": ["Bradikardi", "Soğuk İntoleransı", "Konfüzyon", "Bilateral Ödem"], "t": "TSH (Çok Yüksek) + sT4", "ted": "IV L-Tiroksin + Steroid"},
    "Akromegali": {"b": ["El-Ayak Büyümesi", "Hiperglisemi", "Ani Baş Ağrısı", "Terleme"], "t": "IGF-1 + Hipofiz MR", "ted": "Cerrahi + Octreotide"},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria", "Hiperglisemi", "Hiperglisemi"], "t": "DST + 24s İdrar Kortizol", "ted": "Cerrahi / Ketokonazol"},
    "Feokromositoma": {"b": ["Çarpıntı", "Ani Baş Ağrısı", "Terleme", "Hiperglisemi"], "t": "Plazma Metanefrin", "ted": "Alfa Bloker -> Cerrahi"},
    "Bruselloz": {"b": ["Ateş (>38)", "Terleme", "Eklem Ağrısı", "Splenomegali"], "t": "Wright Aglütinasyon", "ted": "Doksisiklin + Rifampisin"},
    "Menenjit (Bakteriyel)": {"b": ["Ense Sertliği", "Ateş (>38)", "Fotofobi", "Ani Baş Ağrısı"], "t": "Lomber Ponksiyon (BOS)", "ted": "Seftriakson + Vankomisin"},
    "Ankilozan Spondilit": {"b": ["Sabah Sertliği", "Eklem Ağrısı", "Uveit"], "t": "HLA-B27 + Sakroiliak MR", "ted": "NSAİİ + Anti-TNF"},
    "Polisitemia Vera": {"b": ["Polisitemi", "Kaşıntı", "Splenomegali", "Ani Baş Ağrısı"], "t": "JAK2 V617F", "ted": "Flebotomi + Hidroksiüre"},
    "İdiyopatik Trombositopenik Purpura (İTP)": {"b": ["Trombositopeni", "Peteşi", "Diş Eti Kanaması"], "t": "Kemik İliği (Dışlama)", "ted": "Steroid + IVIG"},
    "Herediter Anjioödem": {"b": ["Bilateral Ödem", "Stridor", "Karın Ağrısı"], "t": "C4 Düşüklüğü", "ted": "C1 İnhibitör / İkatibant"},
    "Diyabet Şekersiz (DI)": {"b": ["Poliüri", "Polidipsi", "Hipernatremi"], "t": "Susuzluk Testi", "ted": "Desmopressin"},
    "Sjögren Sendromu": {"b": ["Göz Kuruluğu", "Ağızda Aft", "Eklem Ağrısı"], "t": "Anti-SSA / SSB / Schirmer", "ted": "Suni Gözyaşı + Hidroksiklorokin"},
    "Primer Biliyer Kolanjit (PBK)": {"b": ["Sarılık", "Kaşıntı", "KC Enzim Yüksekliği"], "t": "Anti-Mitokondriyal Antikor (AMA)", "ted": "UDCA (Ursofalk)"},
    "Wilson Hastalığı": {"b": ["Hepatomegali", "Tremor", "Dizartri", "KC Enzim Yüksekliği"], "t": "Seruloplazmin + Kayser-Fleischer", "ted": "D-Penisilamin / Çinko"},
    "Hemokromatozis": {"b": ["Hiperpigmentasyon", "Hiperglisemi", "Eklem Ağrısı", "KC Enzim Yüksekliği"], "t": "Ferritin + Transferrin Sat.", "ted": "Flebotomi"},
    "Osteomiyelit": {"b": ["Ateş (>38)", "Kemik Ağrısı", "Lökositoz"], "t": "MR + Kemik Kültürü", "ted": "IV Antibiyotik (6 hafta)"},
    "Sarkoidoz": {"b": ["Nefes Darlığı", "Öksürük", "Lenfadenopati", "Uveit"], "t": "ACE Yüksekliği + Akciğer BX", "ted": "Steroid (Gerekirse)"},
    "Gut Artriti": {"b": ["Eklem Ağrısı", "Ateş (>38)", "Alkol/Et Tüketimi?"], "t": "Ürik Asit + Eklem Sıvısı", "ted": "Kolşisin + NSAİİ"},
    "Aplastik Anemi": {"b": ["Anemi", "Lökopeni", "Trombositopeni", "Solukluk"], "t": "Kemik İliği Biyopsisi", "ted": "İmmünsupresyon / KİT"},
    "DIC (Yaygın Pıhtılaşma)": {"b": ["Peteşi", "Diş Eti Kanaması", "Trombositopeni", "LDH Yüksekliği"], "t": "D-Dimer + Fibrinojen", "ted": "TDP + Trombosit + Altta Yatan Neden"},
    "Enfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm", "Peteşi", "Splenomegali"], "t": "EKO (Vejetasyon) + Kültür", "ted": "IV Antibiyotik (Uzun Süre)"},
    "Myastenia Gravis": {"b": ["Disfaji", "Dizartri", "Parezi/Paralizi"], "t": "AChR Antikoru + Tensilon Testi", "ted": "Piridostigmin + Steroid"},
    "İnterstisyel Akciğer Hastalığı": {"b": ["Nefes Darlığı", "Öksürük", "Ral"], "t": "Yüksek Çözünürlüklü BT", "ted": "Antifibrotikler / Steroid"},
    "Renal Arter Stenozu": {"b": ["Hipotansiyon", "Renal Disfonksiyon", "Üfürüm"], "t": "Renal Doppler / MR Anjiyo", "ted": "Anjiyoplasti / Stent"},
    "Amiloidoz": {"b": ["Köpüklü İdrar", "Bilateral Ödem", "Makroglossi"], "t": "Karın Yağı Biyopsisi", "ted": "Altta Yatan Neden + KT"},
    "Dermatomiyozit": {"b": ["Parezi/Paralizi", "Kelebek Döküntü", "Eklem Ağrısı"], "t": "CK Yüksekliği + EMG", "ted": "Steroid + Azatioprin"},
    "Hipertrigliseridemi Pankreatit": {"b": ["Kuşak Ağrısı", "Karın Ağrısı", "Hiperglisemi"], "t": "Trigliserid (>1000)", "ted": "Plazmaferez / İnsülin"},
    "Gastroözofageal Reflü (GÖRH)": {"b": ["Göğüs Ağrısı", "Öksürük", "Disfaji"], "t": "pH Metre + Endoskopi", "ted": "Yaşam Tarzı + PPI"},
    "Huzursuz Bacak Sendromu": {"b": ["Tremor", "Uykusuzluk"], "t": "Klinik", "ted": "Pramipeksol / Demir"}
}

# 6. ANALİZ VE RAPORLAMA
if st.button("🚀 MASTER ANALİZİ ÇALIŞTIR"):
    if not b:
        st.error("Lütfen klinik veri girişi yapınız!")
    else:
        res = []
        for ad, v in master_db.items():
            match = set(b).intersection(set(v["b"]))
            if match:
                score = round((len(match) / len(v["b"])) * 100, 1)
                res.append({"ad": ad, "puan": score, "v": v, "m": match})
        
        res = sorted(res, key=lambda x: x['puan'], reverse=True)
        
        col_res, col_epi = st.columns([1.6, 1])
        with col_res:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            for r in res:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.6rem; font-weight:800; color:#000;'>{r['ad']} (%{r['puan']})</div>
                    <p style='color:#DC2626; font-weight:700;'>Uyumlu Parametreler: {", ".join(r['m'])}</p>
                    <hr style='border: 1px solid #DC2626;'>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['t']}</p>
                    <p>💊 <b>Tedavi Protokolü:</b> {r['v']['ted']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_epi:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            epi = f"""TIBBİ ANALİZ RAPORU (V23)\n---------------------------\nID: {p_no} | {datetime.now().strftime('%d/%m/%Y')}\nLAB: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}, Na {na}\n\nSEÇİLEN BULGULAR:\n{", ".join(b)}\n\nÖN TANILAR:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in res[:5]])}\n\nONAY: İSMAİL ORHAN"""
            st.markdown(f"<pre style='background:white; padding:35px; border-radius:35px; border:4px solid #DC2626; font-size:14px; color:#000;'>{epi}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Epikrizi Kaydet", epi, file_name=f"{p_no}_V23.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | V23 ULTIMATE DAHİLİYE | 350+ SATIR KOD | 2026")
