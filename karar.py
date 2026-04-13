import streamlit as st
from datetime import datetime

# 1. PREMIUM ARCHITECTURAL INTERFACE (IVORY, GOLD & REDLINE)
st.set_page_config(page_title="İSMAİL ORHAN | Tıbbi Karar Robotu V19", page_icon="🚨", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    /* Genel Arka Plan - Bej & Fildişi */
    .stApp { 
        background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); 
        color: #1A1A1A; 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }
    
    /* Optimize Edilmiş Başlık (Taşmayı Önleyen Boyut) */
    .main-header {
        background: rgba(255, 255, 255, 0.95); 
        backdrop-filter: blur(30px);
        padding: 40px; 
        border-radius: 50px; 
        text-align: center; 
        margin-bottom: 40px;
        border-top: 8px solid #DC2626; /* Kırmızı Çizgi Detayı */
        border-bottom: 8px solid #DC2626; /* Kırmızı Çizgi Detayı */
        border-left: 3px solid #D4AF37; 
        border-right: 3px solid #D4AF37;
        box-shadow: 0 40px 80px rgba(0,0,0,0.15);
    }
    .main-header h1 { 
        color: #000000; 
        font-weight: 800; 
        font-size: 3.2rem; /* Boyut 1 tık küçültüldü */
        letter-spacing: -2px; 
        margin: 0;
    }
    .main-header p { 
        color: #DC2626; 
        font-size: 1.4rem; 
        font-weight: 700; 
        margin-top: 10px; 
        text-transform: uppercase; 
    }
    
    /* Kristal Kartlar ve Kırmızı Detaylar */
    .clinical-card { 
        background: #FFFFFF; 
        padding: 45px; 
        border-radius: 50px; 
        margin-bottom: 35px;
        border: 1px solid #E2E2E2; 
        box-shadow: 25px 25px 60px #D9D9D9, -25px -25px 60px #FFFFFF;
        border-left: 20px solid #DC2626; /* Kırmızı Vurgu */
        border-right: 5px solid #D4AF37; /* Altın Vurgu */
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .clinical-card:hover { transform: scale(1.01); }
    
    /* Dev Analiz Butonu */
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #333333 100%); 
        color: #FFFFFF; 
        border-radius: 40px;
        height: 7em; 
        width: 100%; 
        font-weight: 800; 
        font-size: 28px; 
        border: 4px solid #DC2626; /* Kırmızı Çizgi */
        box-shadow: 0 25px 50px rgba(220, 38, 38, 0.3);
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        background: #DC2626; 
        color: #FFFFFF; 
        box-shadow: 0 30px 60px rgba(220, 38, 38, 0.5); 
    }
    
    /* Yan Panel Kırmızı Detay */
    [data-testid="stSidebar"] {
        background-color: #F5F5DC;
        border-right: 5px solid #DC2626;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='main-header'>
        <h1>TIBBİ KARAR ROBOTU</h1>
        <p>UYGULAMA GELİŞTİRİCİSİ: İSMAİL ORHAN </p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - HASTA TERMİNALİ
with st.sidebar:
    st.markdown("### 🏛️ SİSTEM TERMİNALİ")
    p_no = st.text_input("Protokol / Barkod", "IO-MASTER-REDLINE")
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    yas = st.number_input("Yaş", 0, 120, 50)
    kilo = st.number_input("Kilo (kg)", 3, 250, 75)
    
    st.divider()
    st.markdown("### 🧪 LABORATUVAR")
    glu = st.number_input("Glukoz (mg/dL)", 0, 2500, 100)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 35.0, 1.0)
    k_plus = st.number_input("Potasyum (mEq/L)", 1.0, 15.0, 4.2)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 30, 350, 120)
    
    st.markdown("### 🫀 KARDİYAK VERİ")
    trop = st.checkbox("Troponin (+) / CK-MB Yüksek")
    ekg_st = st.checkbox("EKG: ST Elevasyonu / Çökmesi")
    ekg_aritmi = st.checkbox("EKG: AF / VT / Atriyal Flutter")

    # eGFR Hesaplama (Cinsiyet Düzeltmeli)
    egfr_base = ((140 - yas) * kilo) / (72 * kre) if kre > 0 else 0
    egfr = round(egfr_base * 0.85 if cinsiyet == "Kadın" else egfr_base, 1)
    st.metric(f"Böbrek Rezervi (eGFR)", f"{egfr} ml/dk")
    
    if egfr < 30: st.error("🚨 DİKKAT: RENAL YETMEZLİK!")
    if ta_sis > 180: st.warning("🚨 HİPERTANSİF KRİZ!")

# 4. KLİNİK BULGU SEÇİMİ (MAKSİMUM KAPSAM)
st.subheader("🔍 Klinik Bulguları Eksiksiz Tanımlayın")
t1, t2, t3, t4, t5, t6 = st.tabs(["🫀 KARDİYO", "🫁 GÖĞÜS", "🤢 GİS-KC", "🧠 NÖROLOJİ", "🧪 ENDO-RENAL", "🩸 HEMATO-ONKO"])

bulgular = []
with t1: bulgular.extend(st.multiselect("Kardiyovasküler Bulgular", ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Çeneye Yayılan Ağrı", "Sırt Ağrısı (Yırtılır Tarzda)", "Çarpıntı", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Üfürüm", "Hipotansiyon", "Senkop"]))
with t2: bulgular.extend(st.multiselect("Pulmoner Bulgular", ["Nefes Darlığı", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Ral", "Ronküs", "Wheezing", "Öksürük", "Plevritik Ağrı"]))
with t3: bulgular.extend(st.multiselect("Gastro-Hepatobilier", ["Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Kuşak Ağrısı", "Karın Ağrısı", "Hematemez", "Melena", "Murphy Belirtisi"]))
with t4: bulgular.extend(st.multiselect("Nöroloji Bulguları", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Fokal Kayıp", "Ani Baş Ağrısı", "Ataksi", "Dizartri", "Fotofobi", "Pupil Farklılığı"]))
with t5: bulgular.extend(st.multiselect("Endokrin & Üriner", ["Poliüri", "Polidipsi", "Oligüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Köpüklü İdrar", "Pretibial Miksödem"]))
with t6: bulgular.extend(st.multiselect("Hemato-Onkoloji", ["Peteşi", "Purpura", "Kelebek Döküntü", "Raynaud Belirtisi", "Ağızda Aft", "Lenfadenopati", "Kemik Ağrısı", "B Semptomları (Ateş, Terleme, Kilo Kaybı)"]))

# Sidebar verilerini bulgu listesine ekle
if trop: bulgular.append("Troponin (+)")
if ekg_st: bulgular.append("EKG: ST Değişikliği")
if ekg_aritmi: bulgular.append("Aritmi Bulgusu")

# 5. MAKSİMUM KAPSAMLI MASTER VERİ TABANI (TÜM DAHİLİYE KİTABI)
master_database = {
    "Miyokard İnfarktüsü (MI)": {
        "bulgu": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Çeneye Yayılan Ağrı", "Troponin (+)", "EKG: ST Değişikliği"],
        "tetkik": "Seri Troponin, EKG, EKO, Koroner Anjiyografi (Altın Standart)",
        "tedavi": "Aspirin 300mg, Klopidogrel 600mg, Heparin, Acil Perkütan Girişim (Anjiyo)"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Unilateral Ödem", "Plevritik Ağrı"],
        "tetkik": "BT Anjiyo, D-Dimer, Troponin, Alt Ekstremite RDUS",
        "tedavi": f"Enoksaparin {kilo}mg 2x1 S.C., Masifse Trombolitik (tPA)"
    },
    "Aort Diseksiyonu": {
        "bulgu": ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır Tarzda)", "Hipotansiyon", "Ani Baş Ağrısı"],
        "tetkik": "BT Anjiyo (Tüm Aorta), TEE (Transözofageal Eko)",
        "tedavi": "IV Beta Bloker (Esmolol/Labetalol), Acil Kalp Damar Cerrahisi Konsültasyonu"
    },
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Bilirubin, Amonyak, Batın USG Doppler, Gastroskopi",
        "tedavi": "Spironolakton + Furosemid, Laktüloz, Protein Kısıtlaması, Varis varsa Propranolol"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Karın Ağrısı", "Konfüzyon"],
        "tetkik": "Kan Gazı (pH < 7.3, HCO3 < 18), İdrar Ketoni, Glukoz > 250",
        "tedavi": f"İnsülin 0.1 Ü/kg/saat ({round(kilo*0.1,1)} Ü/saat), Agresif SF Hidrasyonu, Potasyum Takibi"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Ağrısı", "Karın Ağrısı", "Murphy Belirtisi", "Bulantı-Kusma"],
        "tetkik": "Lipaz (Spesifik), Amilaz, Kontrastlı Üst Batın BT (48-72. saat)",
        "tedavi": "NPO (Ağızdan beslenme kes), Agresif Sıvı (Ringer Laktat), IV Analjezi"
    },
    "Nefrotik Sendrom": {
        "bulgu": ["Bilateral Ödem", "Köpüklü İdrar", "Asit", "Halsizlik"],
        "tetkik": "24h İdrar Proteini (>3.5g), Serum Albümin, Lipid Paneli",
        "tedavi": "Steroid (Prednizolon), ACE İnhibitörü, Diüretik, Tuz Kısıtlaması"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Peteşi", "Sabah Sertliği"],
        "tetkik": "ANA, Anti-dsDNA, C3-C4 Seviyeleri, Tam İdrar (Proteinüri/Hematüri)",
        "tedavi": "Hidroksiklorokin (Plaquenil), Sistemik Steroid, İmmünsupresif"
    },
    "Tiroid Fırtınası": {
        "bulgu": ["Çarpıntı", "Ateş", "Konfüzyon", "Taşikardi", "Sarılık"],
        "tetkik": "TSH (Baskılı), sT4/sT3 (Çok Yüksek), Burch-Wartofsky Skoru",
        "tedavi": "PTU (Propilthiourasil), Lugol Çözeltisi, Propranolol, IV Steroid"
    },
    "Miksödem Koması": {
        "bulgu": ["Hipotoni", "Bradikardi", "Konfüzyon", "Pretibial Miksödem", "Halsizlik"],
        "tetkik": "TSH (Yüksek), sT4 (Düşük), Kortizol",
        "tedavi": "IV L-Tiroksin, IV Hidrokortizon (Sürrenal yetmezlik dışlanana kadar), Isıtma"
    },
    "Addison Krizi": {
        "bulgu": ["Hiperpigmentasyon", "Hipotansiyon", "Halsizlik", "Karın Ağrısı"],
        "tetkik": "ACTH Stimülasyon Testi, Na (Düşük), K (Yüksek)",
        "tedavi": "IV Hidrokortizon 100mg, Agresif Sıvı Rezidansı (SF)"
    },
    "Lenfoma (Hodgkin/Non-Hodgkin)": {
        "bulgu": ["Lenfadenopati", "Gece Terlemesi", "Kilo Kaybı", "Ateş", "Kaşıntı"],
        "tetkik": "Eksizyonel Lenf Nodu Biyopsisi (Altın Standart), PET-BT",
        "tedavi": "Kemoterapi (CHOP/ABVD), Radyoterapi, İmmünoterapi"
    },
    "Multipl Miyelom": {
        "bulgu": ["Kemik Ağrısı", "Halsizlik", "Anemi Bulguları", "Köpüklü İdrar"],
        "tetkik": "Serum/İdrar Protein Elektroforezi (M-Piki), Kemik İliği Biyopsisi",
        "tedavi": "Bortezomib, Lenalidomid, Deksametazon, Kök Hücre Nakli"
    },
    "Karbonmonoksit Zehirlenmesi": {
        "bulgu": ["Ani Baş Ağrısı", "Bulantı-Kusma", "Konfüzyon", "Senkop"],
        "tetkik": "Karboksihemoglobin (COHb) Seviyesi, Kan Gazı, EKG",
        "tedavi": "%100 Normobarik Oksijen, Gerekirse Hiperbarik Oksijen Tedavisi"
    },
    "Atriyal Fibrilasyon (AF)": {
        "bulgu": ["Çarpıntı", "Nefes Darlığı", "Aritmi Bulgusu", "Halsizlik"],
        "tetkik": "EKG (P dalgası yok), EKO (Trombus?), TSH Takibi",
        "tedavi": "Hız Kontrolü (Beta Bloker), Ritim Kontrolü (Amiodaron), Antikoagülasyon (Warfarin/NOAC)"
    }
}

# 6. ANALİZ MOTORU
if st.button("🚀 TIBBİ KARAR ROBOTUNU ÇALIŞTIR"):
    if not bulgular:
        st.error("Lütfen en az bir klinik bulgu veya laboratuvar verisi seçiniz!")
    else:
        st.divider()
        sonuclar = []
        for ad, veri in master_database.items():
            eslesme = set(bulgular).intersection(set(veri["bulgu"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": veri, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        col_res1, col_res2 = st.columns([1.6, 1])
        with col_res1:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.8rem; color:#000000; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p style='color:#DC2626; font-weight:700; font-size:1.2rem;'>🎯 Eşleşen Kriterler: {", ".join(s['esles'])}</p>
                    <hr style='border: 1px solid #DC2626;'>
                    <p>🧪 <b>Gerekli Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Modern Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_res2:
            st.markdown("### 📝 RESMİ EPİKRİZ RAPORU")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON"
            epikriz = f"""KLİNİK ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
ROBOT SÜRÜMÜ: V19 MASTER REDLINE
PROTOKOL: {p_no}

[VİTAL PARAMETRELER]
Cinsiyet: {cinsiyet} | Yaş: {yas} | Kilo: {kilo}kg
eGFR: {egfr} ml/dk | Glukoz: {glu} | TA: {ta_sis}

[KLİNİK BULGULAR]
{", ".join(bulgular)}

[DİFERANSİYEL TANILAR (İLK 5)]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[GÜVENLİK VE RADYOLOJİ NOTLARI]
- {r_not}
- GKS: 15 (Standart)
- Günlük Sıvı Gereksinimi: {kilo*35}cc
--------------------------------------------------
ONAY VE İMZA: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:45px; border-radius:45px; border:3px solid #DC2626; font-size:15px; box-shadow: 10px 10px 30px rgba(0,0,0,0.1);'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Arşivine Gönder", epikriz, file_name=f"{p_no}_redline.txt")

# Alt Bilgi (Footer)
st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | TIBBİ KARAR ROBOTU V19 REDLINE | 2026")
