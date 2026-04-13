import streamlit as st
from datetime import datetime

# 1. ARCHITECTURAL DESIGN (IVORY, GOLD & AGGRESSIVE REDLINE)
st.set_page_config(page_title="İSMAİL ORHAN | Dahiliye Ansiklopedisi V22", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 35px; border-radius: 45px; text-align: center; margin-bottom: 35px;
        border-top: 10px solid #DC2626; border-bottom: 10px solid #DC2626; border-left: 5px solid #D4AF37; border-right: 5px solid #D4AF37;
        box-shadow: 0 40px 80px rgba(0,0,0,0.15);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 2.8rem; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.3rem; font-weight: 700; text-transform: uppercase; }

    .clinical-card { 
        background: #FFFFFF; padding: 40px; border-radius: 50px; margin-bottom: 30px;
        border-left: 20px solid #DC2626; border-right: 8px solid #D4AF37;
        box-shadow: 20px 20px 50px #D9D9D9;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 40px;
        height: 6em; width: 100%; font-weight: 800; font-size: 28px; border: 4px solid #DC2626;
    }
    .stButton>button:hover { background: #DC2626; transform: scale(1.01); }
    
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 6px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KARAR ROBOTU</h1><p>MASTER DEVELOPER: İSMAİL ORHAN | V22 ULTRA DOMAIN</p></div>", unsafe_allow_html=True)

# 2. YAN PANEL - KAN SONUÇLARI (BOZULMADI, GELİŞTİRİLDİ)
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR TERMİNALİ")
    p_no = st.text_input("Barkod", "IO-V22-FULL")
    yas = st.number_input("Yaş", 0, 120, 55)
    kilo = st.number_input("Kilo (kg)", 5, 250, 85)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 40.0, 1.2)
    hb = st.number_input("Hemoglobin (g/dL)", 3.0, 25.0, 13.0)
    wbc = st.number_input("WBC (Lökosit)", 0, 500000, 8000)
    plt = st.number_input("PLT (Trombosit)", 0, 2000000, 250000)
    glu = st.number_input("Glukoz (mg/dL)", 0, 3000, 110)
    na = st.number_input("Sodyum (Na)", 100, 180, 140)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.2)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 20.0, 9.6)
    ldh = st.number_input("LDH", 0, 10000, 250)
    ast = st.number_input("AST", 0, 5000, 30)
    alt = st.number_input("ALT", 0, 5000, 35)
    
    egfr_base = ((140 - yas) * kilo) / (72 * kre) if kre > 0 else 0
    st.metric("eGFR", f"{round(egfr_base, 1)} ml/dk")

# 3. GENİŞLETİLMİŞ BELİRTİ VE BULGU SEÇİMİ (SEKMELER)
st.subheader("🔍 Klinik Belirti ve Fizik Muayene Bulguları")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KALP-DAMAR", "🫁 GÖĞÜS-AKC", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖROLOJİ", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENFEKSİYON"])

b = []
with t1: b.extend(st.multiselect("Kardiyo", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Boyun Ven Dolgunluğu", "Çarpıntı", "Senkop", "Hipotansiyon", "Bilateral Bacak Ödemi", "Üfürüm"]))
with t2: b.extend(st.multiselect("Göğüs", ["Nefes Darlığı", "Hemoptizi", "Ral", "Ronküs", "Wheezing", "Öksürük", "Stridor", "Plevritik Ağrı"]))
with t3: b.extend(st.multiselect("Gastro", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Rebound", "Murphy Belirtisi", "Asteriksis"]))
with t4: b.extend(st.multiselect("Endokrin", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Galaktore", "Terleme", "El-Ayak Büyümesi"]))
with t5: b.extend(st.multiselect("Nöro", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Fokal Kayıp", "Ani Baş Ağrısı", "Fotofobi", "Dizartri", "Tremor"]))
with t6: b.extend(st.multiselect("Hemato", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması"]))
with t7: b.extend(st.multiselect("Romato", ["Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Ateş (>38)"]))

# KAN SONUÇLARINI OTOMATİK BULGUYA DÖNÜŞTÜR (BOZMADAN EKLE)
if kre > 1.5: b.append("Yüksek Kreatinin")
if hb < 11: b.append("Düşük Hemoglobin")
if hb > 17: b.append("Yüksek Hemoglobin (Polisitemi)")
if wbc > 12000: b.append("Lökositoz")
if wbc < 4000: b.append("Lökopeni")
if plt < 150000: b.append("Trombositopeni")
if plt > 450000: b.append("Trombositoz")
if glu > 200: b.append("Hiperglisemi")
if na < 135: b.append("Hiponatremi")
if na > 145: b.append("Hipernatremi")
if ca > 10.5: b.append("Hiperkalsemi")
if ldh > 500: b.append("Yüksek LDH")
if ast > 100 or alt > 100: b.append("Transaminaz Yüksekliği")

# 4. DEVASA MASTER DATABASE (1000 SATIRA DOĞRU)
master_db = {
    "Üst GİS Kanama (Varis Dışı)": {"b": ["Hematemez", "Melena", "Düşük Hemoglobin"], "tetkik": "Acil Üst GİS Endoskopisi", "tedavi": "IV PPI Bolus + İnfüzyon"},
    "Üst GİS Kanama (Varis)": {"b": ["Hematemez", "Melena", "Sarılık", "Asit", "Splenomegali"], "tetkik": "Endoskopi + Portal Doppler USG", "tedavi": "Terlipressin + Band Ligasyonu"},
    "Alt GİS Kanama": {"b": ["Hematokezya", "Melena"], "tetkik": "Kolonoskopi + BT Anjiyo", "tedavi": "Sıvı + Gerekirse Cerrahi"},
    "Miyokard İnfarktüsü": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Hipotansiyon"], "tetkik": "EKG + Troponin + Anjiyo", "tedavi": "Aspirin + Klopidogrel + Heparin"},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Göğüs Ağrısı", "Hipotansiyon"], "tetkik": "BT Anjiyo (Tüm Aorta)", "tedavi": "IV Beta Bloker + Acil Cerrahi"},
    "Sepsis / Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon", "Lökositoz"], "tetkik": "Kan Kültürü + Laktat", "tedavi": "IV Antibiyotik + Agresif Sıvı"},
    "Diyabetik Ketoasidoz": {"b": ["Aseton Kokusu", "Hiperglisemi", "Poliüri", "Karın Ağrısı"], "tetkik": "Kan Gazı + İdrar Ketoni", "tedavi": "IV İnsülin + Sıvı + K+"},
    "B12 Eksikliği Anemisi": {"b": ["Düşük Hemoglobin", "Konfüzyon", "Solukluk", "Dizartri"], "tetkik": "Serum B12 + Periferik Yayma (Makrosit)", "tedavi": "B12 İntramüsküler Replasman"},
    "Demir Eksikliği Anemisi": {"b": ["Düşük Hemoglobin", "Solukluk", "Kaşıntı"], "tetkik": "Ferritin + Demir Bağlama", "tedavi": "Oral/IV Demir Tedavisi"},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Yüksek Kreatinin", "Hiperkalsemi", "Düşük Hemoglobin"], "tetkik": "Protein Elektroforezi + KİB", "tedavi": "VAD/VCD Protokolü + Kök Hücre"},
    "Primer Hiperparatiroidi": {"b": ["Hiperkalsemi", "Kemik Ağrısı", "Polidipsi"], "tetkik": "PTH + Paratiroid Sintigrafisi", "tedavi": "Cerrahi Eksizyon"},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria", "Hiperglisemi", "Bilateral Bacak Ödemi"], "tetkik": "24s İdrar Kortizolü + Dekzametazon Süpresyon", "tedavi": "Etiyolojiye Göre Cerrahi"},
    "Akromegali": {"b": ["El-Ayak Büyümesi", "Hiperglisemi", "Ani Baş Ağrısı"], "tetkik": "IGF-1 + OGTT Baskılama Testi", "tedavi": "Hipofiz Cerrahisi + Somatostatin"},
    "Polisitemia Vera": {"b": ["Yüksek Hemoglobin (Polisitemi)", "Kaşıntı", "Splenomegali", "Ani Baş Ağrısı"], "tetkik": "JAK2 Mutasyonu + KİB", "tedavi": "Flebotomi + Hidroksiüre"},
    "Sistemik Lupus (SLE)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Lökopeni", "Trombositopeni"], "tetkik": "ANA + Anti-dsDNA", "tedavi": "Plaquenil + Steroid"},
    "Behçet Hastalığı": {"b": ["Ağızda Aft", "Eklem Ağrısı", "Uveit", "Peteşi"], "tetkik": "Paterji Testi + HLA-B51", "tedavi": "Kolşisin + İmmünsupresif"},
    "Vaskülit (GPA/Wegener)": {"b": ["Hemoptizi", "Nefes Darlığı", "Yüksek Kreatinin", "Öksürük"], "tetkik": "c-ANCA + Akciğer/Böbrek Biyopsisi", "tedavi": "Siklofosfamid + Pulse Steroid"},
    "Karaciğer Yetmezliği (Akut)": {"b": ["Sarılık", "Konfüzyon", "Transaminaz Yüksekliği", "Asteriksis"], "tetkik": "INR + Amonyak + Bilirubin", "tedavi": "N-Asetilsistein + Karaciğer Nakli Hazırlığı"},
    "Pankreas Ca": {"b": ["Sarılık", "Kilo Kaybı", "Karın Ağrısı", "Hepatomegali"], "tetkik": "CA 19-9 + Batın BT/MRCP", "tedavi": "Cerrahi (Whipple) + KT"},
    "Feokromositoma": {"b": ["Çarpıntı", "Terleme", "Ani Baş Ağrısı", "Hiperglisemi"], "tetkik": "Plazma Metanefrinleri", "tedavi": "Alfa Bloker -> Sonra Cerrahi"},
    "Kronik Böbrek Yetmezliği": {"b": ["Yüksek Kreatinin", "Bilateral Bacak Ödemi", "Hipotansiyon", "Anemi Bulgusu"], "tetkik": "Renal USG + PTH", "tedavi": "Diyet + KBY Protokolü"},
    "TTP (Trombotik Trombositopenik Purpura)": {"b": ["Trombositopeni", "Düşük Hemoglobin", "Konfüzyon", "Ateş (>38)", "Yüksek LDH"], "tetkik": "Şistosit Takibi + ADAMTS13", "tedavi": "Acil Plazmaferez + Steroid"},
    "Bruselloz": {"b": ["Ateş (>38)", "Eklem Ağrısı", "Splenomegali", "Terleme"], "tetkik": "Rose Bengal + Wright Aglütinasyon", "tedavi": "Doksisiklin + Rifampisin"},
    "Herediter Anjioödem": {"b": ["Bilateral Bacak Ödemi", "Karın Ağrısı", "Stridor"], "tetkik": "C4 Düşüklüğü + C1 Esteraz İnhibitör", "tedavi": "C1 İnhibitör Konsantresi / İkatibant"},
    "Diyabet Şekersiz (DI)": {"b": ["Poliüri", "Polidipsi", "Hipernatremi"], "tetkik": "Susuzluk Testi + ADH Seviyesi", "tedavi": "Desmopressin (Minirin)"}
}

# 5. ANALİZ MOTORU
if st.button("🚀 MASTER ANALİZİ BAŞLAT"):
    if not b:
        st.error("Lütfen klinik veri seçiniz!")
    else:
        results = []
        for ad, v in master_db.items():
            matches = set(b).intersection(set(v["b"]))
            if matches:
                score = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": score, "v": v, "matches": matches})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("### 🏛️ Teşhis & Tedavi Matrisi")
            for r in results:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.5rem; font-weight:800;'>{r['ad']} (%{r['puan']})</div>
                    <p style='color:#DC2626; font-weight:700;'>Uyumlu Bulgular: {", ".join(r['matches'])}</p>
                    <hr>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['tetkik']}</p>
                    <p>💊 <b>Tedavi:</b> {r['v']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📝 EPİKRİZ RAPORU")
            epikriz = f"""TIBBİ ANALİZ (V22)\n------------------\nHASTA: {p_no}\nYAŞ: {yas} | KİLO: {kilo}\nLAB: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}, Na {na}\n\nBULGULAR:\n{", ".join(b)}\n\nÖN TANILAR:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in results[:5]])}\n\nİMZA: İSMAİL ORHAN"""
            st.markdown(f"<pre style='background:white; padding:30px; border:3px solid #DC2626;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Kaydet", epikriz, file_name=f"{p_no}.txt")

st.markdown("---")
st.caption("GELİŞTİRİCİ: İSMAİL ORHAN | V22 ULTRA | 2026")
