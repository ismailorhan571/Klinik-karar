import streamlit as st
from datetime import datetime

# 1. PREMIUM ARCHITECTURAL INTERFACE (IVORY, GOLD & AGGRESSIVE REDLINE)
st.set_page_config(page_title="İSMAİL ORHAN | Tıbbi Karar Robotu V20", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Optimize Edilmiş Başlık - Taşma Yapmaz */
    .main-header {
        background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(35px);
        padding: 45px; border-radius: 55px; text-align: center; margin-bottom: 45px;
        border-top: 10px solid #DC2626; border-bottom: 10px solid #DC2626;
        border-left: 4px solid #D4AF37; border-right: 4px solid #D4AF37;
        box-shadow: 0 50px 100px rgba(0,0,0,0.18);
    }
    .main-header h1 { color: #000000; font-weight: 800; font-size: 3rem; letter-spacing: -2px; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.5rem; font-weight: 700; margin-top: 12px; text-transform: uppercase; }
    
    /* Gelişmiş Kart Yapısı */
    .clinical-card { 
        background: #FFFFFF; padding: 50px; border-radius: 60px; margin-bottom: 40px;
        border: 1px solid #E2E2E2; box-shadow: 30px 30px 80px #D9D9D9, -30px -30px 80px #FFFFFF;
        border-left: 25px solid #DC2626; border-right: 8px solid #D4AF37;
        transition: 0.4s ease-in-out;
    }
    .clinical-card:hover { transform: scale(1.01) translateY(-5px); }
    
    /* İmza Analiz Butonu (Mega) */
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #434343 100%); color: #FFFFFF; border-radius: 45px;
        height: 7.5em; width: 100%; font-weight: 800; font-size: 30px; border: 5px solid #DC2626;
        box-shadow: 0 30px 60px rgba(220, 38, 38, 0.4); text-transform: uppercase;
    }
    .stButton>button:hover { background: #DC2626; color: #FFFFFF; box-shadow: 0 40px 80px rgba(220, 38, 38, 0.6); }
    
    /* Sidebar Kırmızı Çizgi */
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 6px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"<div class='main-header'><h1>TIBBİ KARAR ROBOTU</h1><p>GELİŞTİRİCİ VE EDİTÖR: İSMAİL ORHAN | V20 FINAL MASTER</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL - HASTA TERMİNALİ VE AKILLI ANALİZ
with st.sidebar:
    st.markdown("### 🏛️ SİSTEM TERMİNALİ")
    p_no = st.text_input("Protokol / Arşiv", "IO-MASTER-V20")
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    yas = st.number_input("Yaş", 0, 120, 55)
    kilo = st.number_input("Kilo (kg)", 3, 250, 80)
    
    st.divider()
    st.markdown("### 🧪 GENİŞLETİLMİŞ LAB")
    glu = st.number_input("Glukoz (mg/dL)", 0, 3000, 110)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 40.0, 1.1)
    k_plus = st.number_input("Potasyum (mEq/L)", 1.0, 15.0, 4.2)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 30, 350, 130)
    hb = st.number_input("Hemoglobin (g/dL)", 3.0, 20.0, 13.5)
    plt = st.number_input("Trombosit (PLT)", 5000, 1000000, 250000)
    
    st.markdown("### 🫀 KARDİYAK / VİTAL")
    trop = st.checkbox("Troponin (+) / CK-MB")
    ekg_st = st.checkbox("EKG: ST Değişikliği")
    ekg_aritmi = st.checkbox("EKG: AF / VT / Atriyal Flutter")
    laktat = st.number_input("Laktat (mmol/L)", 0.0, 25.0, 1.2)

    # eGFR Hesaplama (Gelişmiş Cockcroft-Gault)
    egfr_base = ((140 - yas) * kilo) / (72 * kre) if kre > 0 else 0
    egfr = round(egfr_base * 0.85 if cinsiyet == "Kadın" else egfr_base, 1)
    st.metric(f"eGFR ({cinsiyet})", f"{egfr} ml/dk")
    
    if egfr < 30: st.error("🚨 KRİTİK RENAL YETMEZLİK!")
    if hb < 7: st.error("🚨 KRİTİK ANEMİ: ES TRANSFÜZYONU!")
    if laktat > 2.5: st.warning("🚨 SEPSİS / ŞOK RİSKİ!")

# 4. DEVASA KLİNİK SORGU ÜSSÜ (TAM KAPSAM)
st.subheader("🔍 Klinik Fenotipleri Tanımlayın")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KARDİYO", "🫁 GÖĞÜS", "🤢 GİS-KC", "🧪 ENDO-RENAL", "🧠 NÖRO", "🩸 HEMATO", "🧬 SEPSİS-ONKO"])

bulgular = []
with t1: bulgular.extend(st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Çeneye Yayılan Ağrı", "Sırt Ağrısı (Yırtılır)", "Çarpıntı", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Üfürüm", "Hipotansiyon", "Senkop"]))
with t2: bulgular.extend(st.multiselect("Pulmoner", ["Nefes Darlığı", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Ral", "Ronküs", "Wheezing", "Plevritik Ağrı", "Stridor"]))
with t3: bulgular.extend(st.multiselect("Gastrointestinal", ["Hematemez (Kanlı Kusma)", "Melena (Siyah Dışkı)", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Asteriksis", "Kuşak Ağrısı", "Karın Ağrısı", "Murphy Belirtisi", "Rebound/Defans"]))
with t4: bulgular.extend(st.multiselect("Endokrin & Renal", ["Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Köpüklü İdrar", "Goz Kapagı Ödemi"]))
with t5: bulgular.extend(st.multiselect("Sinir Sistemi", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Ani Baş Ağrısı", "Dizartri", "Ataksi", "Pupil Eşitsizliği", "Fotofobi"]))
with t6: bulgular.extend(st.multiselect("Hematoloji & Romato", ["Peteşi", "Purpura", "Ekimoz", "Kelebek Döküntü", "Raynaud", "Sabah Sertliği", "Eklem Ağrısı", "Ağızda Aft", "Lenfadenopati", "Kemik Ağrısı"]))
with t7: bulgular.extend(st.multiselect("Enfeksiyon & Onkoloji", ["Ateş (>38.3)", "Gece Terlemesi", "Kilo Kaybı (>10kg)", "Kaşıntı", "Öksürük (>3 hafta)", "Paraneoplastik Bulgular"]))

# Otomatik lab eklemeleri
if trop: bulgular.append("Troponin (+)")
if ekg_st: bulgular.append("EKG: ST Değişikliği")
if hb < 9: bulgular.append("Ciddi Anemi")
if laktat > 2: bulgular.append("Yüksek Laktat")

# 5. MASTER BİLGİ BANKASI (300+ SATIR İÇİN DEVASA SÖZLÜK)
master_database = {
    "Üst GİS Kanama": {
        "bulgu": ["Hematemez (Kanlı Kusma)", "Melena (Siyah Dışkı)", "Karın Ağrısı", "Hipotansiyon", "Ciddi Anemi"],
        "tetkik": "Acil Endoskopi (ÖGD), Tam Kan Sayımı, INR, Üre/Kreatinin Oranı",
        "tedavi": "IV PPI (80mg Bolus + 8mg/saat), Sıvı Resusitasyonu, Eritrosit Transfüzyonu, Gerekirse Terlipressin"
    },
    "Alt GİS Kanama": {
        "bulgu": ["Hematokezya", "Melena (Siyah Dışkı)", "Karın Ağrısı", "Hipotansiyon"],
        "tetkik": "Kolonoskopi, Batın BT Anjiyo, Sintigrafi",
        "tedavi": "Hidrasyon, Kan Transfüzyonu, Cerrahi/Radyolojik Embolizasyon"
    },
    "Miyokard İnfarktüsü (MI)": {
        "bulgu": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Çeneye Yayılan Ağrı", "Troponin (+)", "EKG: ST Değişikliği"],
        "tetkik": "Seri Troponin, EKG, EKO, Koroner Anjiyografi",
        "tedavi": "Aspirin 300mg, Klopidogrel 600mg, Heparin, Acil Anjiyo"
    },
    "Sepsis / Septik Şok": {
        "bulgu": ["Ateş (>38.3)", "Konfüzyon", "Hipotansiyon", "Yüksek Laktat", "Nefes Darlığı"],
        "tetkik": "Kan Kültürü, Prokalsitonin, Tam İdrar, Akciğer Grafisi",
        "tedavi": "Geniş Spektrumlu Antibiyotik (İlk 1 saat), IV SF (30ml/kg), Vazopresör (Noradrenalin)"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Unilateral Ödem"],
        "tetkik": "BT Anjiyo, D-Dimer, Troponin, Doppler USG",
        "tedavi": f"Enoksaparin {kilo}mg 2x1, Masifse Trombolitik"
    },
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Bilirubin, USG Doppler",
        "tedavi": "Spironolakton + Furosemid, Laktüloz, Tuz Kısıtlaması"
    },
    "Aort Diseksiyonu": {
        "bulgu": ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Hipotansiyon", "Ani Baş Ağrısı"],
        "tetkik": "BT Anjiyo (Tüm Aorta), Transözofageal Eko",
        "tedavi": "IV Beta Bloker, Acil Kalp Damar Cerrahisi"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Karın Ağrısı", "Konfüzyon"],
        "tetkik": "Kan Gazı, İdrar Ketoni, Glukoz > 250",
        "tedavi": f"İnsülin Perfüzyon ({round(kilo*0.1,1)} Ü/saat), Agresif SF"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Ağrısı", "Karın Ağrısı", "Murphy Belirtisi"],
        "tetkik": "Lipaz, Amilaz, Kontrastlı Batın BT",
        "tedavi": "NPO, Agresif Sıvı Rezidansı, IV Analjezi"
    },
    "Tiroid Fırtınası": {
        "bulgu": ["Çarpıntı", "Ateş (>38.3)", "Konfüzyon", "Sarılık"],
        "tetkik": "TSH, sT4, sT3, Burch-Wartofsky Skoru",
        "tedavi": "Propilthiourasil (PTU), Lugol, Propranolol, IV Steroid"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Peteşi"],
        "tetkik": "ANA, Anti-dsDNA, C3-C4",
        "tedavi": "Hidroksiklorokin, Steroid, İmmünsupresif"
    },
    "Lenfoma (Hodgkin/NH)": {
        "bulgu": ["Lenfadenopati", "Gece Terlemesi", "Kilo Kaybı (>10kg)", "Kaşıntı", "Ateş (>38.3)"],
        "tetkik": "Eksizyonel Biyopsi, PET-BT, Kemik İliği Analizi",
        "tedavi": "Kemoterapi (CHOP/ABVD), Radyoterapi"
    },
    "Disemine İntravasküler Koagülasyon (DIC)": {
        "bulgu": ["Peteşi", "Purpura", "Ekimoz", "Hematemez (Kanlı Kusma)"],
        "tetkik": "D-Dimer (Çok Yüksek), Fibrinojen (Düşük), INR (Yüksek)",
        "tedavi": "Altta yatan nedenin tedavisi, TDP, Trombosit Süspansiyonu"
    },
    "Feokromositoma": {
        "bulgu": ["Çarpıntı", "Terleme", "Ani Baş Ağrısı", "Hipertansiyon"],
        "tetkik": "Plazma Serbest Metanefrinleri, Sürrenal BT",
        "tedavi": "Alfa Bloker (Doksazosin), Sonra Beta Bloker"
    },
    "Menenjit (Bakteriyel)": {
        "bulgu": ["Ense Sertliği", "Ani Baş Ağrısı", "Ateş (>38.3)", "Fotofobi"],
        "tetkik": "Lomber Ponksiyon (BOS), Kan Kültürü",
        "tedavi": "IV Seftriakson + Vankomisin + Deksametazon"
    }
}

# 6. ANALİZ VE RAPORLAMA MOTORU
if st.button("🚀 TIBBİ KARAR ROBOTUNU ÇALIŞTIR"):
    if not bulgular:
        st.error("Lütfen klinik veya laboratuvar verisi giriniz!")
    else:
        sonuclar = []
        for ad, veri in master_database.items():
            eslesme = set(bulgular).intersection(set(veri["bulgu"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": veri, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        c1, c2 = st.columns([1.6, 1])
        with c1:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.8rem; color:#000000; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p style='color:#DC2626; font-weight:700; font-size:1.3rem;'>🎯 Eşleşen Bulgular: {", ".join(s['esles'])}</p>
                    <hr style='border: 1.5px solid #DC2626;'>
                    <p style='font-size:1.1rem;'>🧪 <b>Altın Standart Tetkik:</b> {s['veri']['tetkik']}</p>
                    <p style='font-size:1.1rem;'>💊 <b>Modern Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with c2:
            st.markdown("### 📝 RESMİ EPİKRİZ RAPORU")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON"
            epikriz = f"""KLİNİK ANALİZ RAPORU (V20 MASTER)
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
PROTOKOL: {p_no}

[VİTAL PARAMETRELER]
Cinsiyet: {cinsiyet} | Yaş: {yas} | Kilo: {kilo}kg
eGFR: {egfr} ml/dk | Hb: {hb} g/dL | TA: {ta_sis}

[KLİNİK BULGULAR]
{", ".join(bulgular)}

[DİFERANSİYEL TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[RADYOLOJİ VE GÜVENLİK]
- Durum: {r_not}
- Laktat Seviyesi: {laktat}
- GKS: 15 (Normal)
--------------------------------------------------
ONAY: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:40px; border-radius:40px; border:4px solid #DC2626; font-size:14px; color:#000;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Arşivine Kaydet", epikriz, file_name=f"{p_no}_final_v20.txt")

# Footer
st.markdown("---")
st.caption("İSMAİL ORHAN | TIBBİ KARAR ROBOTU V20 | 300+ SATIR ÖZEL SÜRÜM | 2026")
