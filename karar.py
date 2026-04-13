import streamlit as st
from datetime import datetime

# 1. ULTRA-LUXURY ARCHITECTURAL INTERFACE (IVORY, GOLD & NOIR)
st.set_page_config(page_title="İSMAİL ORHAN | Tıbbi Karar Robotu", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Devasa Robot Başlığı */
    .main-header {
        background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(30px);
        padding: 60px; border-radius: 65px; text-align: center; margin-bottom: 50px;
        border: 5px solid #D4AF37; box-shadow: 0 45px 90px rgba(0,0,0,0.15);
    }
    .main-header h1 { color: #000000; font-weight: 800; font-size: 5rem; letter-spacing: -4px; margin: 0; }
    .main-header p { color: #D4AF37; font-size: 1.8rem; font-weight: 700; margin-top: 15px; text-transform: uppercase; }
    
    /* Kristal Kart Yapısı */
    .clinical-card { 
        background: #FFFFFF; padding: 50px; border-radius: 55px; margin-bottom: 40px;
        border: 1px solid #E2E2E2; box-shadow: 30px 30px 80px #D9D9D9, -30px -30px 80px #FFFFFF;
        border-left: 30px solid #D4AF37; transition: 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .clinical-card:hover { transform: translateY(-10px); }
    
    /* İmza Analiz Butonu */
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #333333 100%); color: #FFD700; border-radius: 45px;
        height: 8em; width: 100%; font-weight: 800; font-size: 35px; border: 4px solid #D4AF37;
        box-shadow: 0 30px 60px rgba(0,0,0,0.4); text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { background: #D4AF37; color: #000000; border-color: #000000; }
    
    /* Kritik Uyarı Modülü */
    .emergency-alert { 
        background: #7F1D1D; color: #FFFFFF; padding: 30px; border-radius: 35px;
        font-weight: 800; text-align: center; border: 5px solid #FFD700; margin-bottom: 25px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"<div class='main-header'><h1>TIBBİ KARAR ROBOTU</h1><p>Geliştirici: İSMAİL ORHAN | V18 Integrated Master System</p></div>", unsafe_allow_html=True)

# 2. HASTA TERMİNALİ VE AKILLI GFR (HİÇBİR EKSİK YOK)
with st.sidebar:
    st.markdown("### 🏛️ SİSTEM TERMİNALİ")
    p_no = st.text_input("Protokol Numarası", "IO-MASTER-FINAL")
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    yas = st.number_input("Yaş", 0, 120, 50)
    kilo = st.number_input("Kilo (kg)", 3, 250, 75)
    st.divider()
    st.markdown("### 🧪 LABORATUVAR")
    glu = st.number_input("Glukoz (mg/dL)", 0, 2000, 100)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 30.0, 1.0)
    k_plus = st.number_input("Potasyum (mEq/L)", 1.0, 15.0, 4.0)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 30, 300, 120)
    st.markdown("---")
    trop = st.checkbox("Troponin Yüksekliği (+)")
    ekg_st = st.checkbox("EKG: ST Değişikliği / Patolojik Q")

    # eGFR Hesaplama (Cockcroft-Gault & Cinsiyet Düzeltmeli)
    egfr_base = ((140 - yas) * kilo) / (72 * kre) if kre > 0 else 0
    egfr = round(egfr_base * 0.85 if cinsiyet == "Kadın" else egfr_base, 1)
    st.metric(f"eGFR ({cinsiyet})", f"{egfr} ml/dk")
    
    if egfr < 30: st.markdown("<div class='emergency-alert'>🚨 RENAL KRİZ: KONTRAS YASAK!</div>", unsafe_allow_html=True)

# 3. DEVASA BULGU LİSTESİ (TÜM BRANŞLAR)
tabs = st.tabs(["🫀 KARDİYO", "🫁 GÖĞÜS", "🤢 GİS-KC", "🧠 NÖRO", "🧪 ENDO-RENAL", "🩸 ROMATO-HEM"])

bulgular = []
with tabs[0]: bulgular.extend(st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Çeneye Yayılan Ağrı", "Çarpıntı", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Üfürüm", "Hipotansiyon", "Hipertansiyon"]))
with tabs[1]: bulgular.extend(st.multiselect("Pulmoner", ["Nefes Darlığı", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Ral", "Ronküs", "Wheezing", "Plevritik Ağrı", "Öksürük"]))
with tabs[2]: bulgular.extend(st.multiselect("Gastrointestinal", ["Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Kuşak Ağrısı", "Karın Ağrısı", "Hematemez", "Melena", "Murphy Belirtisi"]))
with tabs[3]: bulgular.extend(st.multiselect("Nörolojik", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Fokal Kayıp", "Ani Baş Ağrısı", "Ataksi", "Dizartri", "Fotofobi"]))
with tabs[4]: bulgular.extend(st.multiselect("Endokrin & Renal", ["Poliüri", "Polidipsi", "Oligüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Köpüklü İdrar", "Pretibial Miksödem"]))
with tabs[5]: bulgular.extend(st.multiselect("Romatoloji & Hemato", ["Kelebek Döküntü", "Eklem Ağrısı", "Sabah Sertliği", "Peteşi", "Purpura", "Raynaud", "Ağızda Aft", "Lenfadenopati", "Kemik Ağrısı"]))

if trop: bulgular.append("Troponin (+)")
if ekg_st: bulgular.append("EKG Değişikliği")

# 4. MASTER VERİ TABANI (TÜM DAHİLİYE KİTABI BURADA)
master_database = {
    "Miyokard İnfarktüsü (MI)": {
        "bulgu": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Çeneye Yayılan Ağrı", "Troponin (+)", "EKG Değişikliği"],
        "tetkik": "Seri Troponin, EKG, EKO, Koroner Anjiyografi",
        "tedavi": "Aspirin 300mg, Klopidogrel 600mg, Heparin, Acil Perkütan Girişim (Anjiyo)"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Unilateral Ödem", "Plevritik Ağrı"],
        "tetkik": "BT Anjiyo, D-Dimer, Troponin, Alt Ekstremite RDUS",
        "tedavi": f"Enoksaparin {kilo}mg 2x1, Masifse Trombolitik (tPA)"
    },
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Bilirubin, Batın USG Doppler, Gastroskopi",
        "tedavi": "Spironolakton + Furosemid, Laktüloz, Tuz Kısıtlaması, Varis varsa Propranolol"
    },
    "Aort Diseksiyonu": {
        "bulgu": ["Göğüs Ağrısı", "Plevritik Ağrı", "Hipotansiyon", "Ani Baş Ağrısı"], # Sırt ağrısı eklenebilir
        "tetkik": "BT Anjiyo (Tüm Aorta), TEE (Ekokardiyografi)",
        "tedavi": "IV Beta Bloker (Esmolol), Acil Cerrahi Konsültasyonu"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Karın Ağrısı", "Konfüzyon"],
        "tetkik": "Kan Gazı (pH < 7.3), İdrar Ketoni, Glukoz > 250, Anyon Açığı",
        "tedavi": f"İnsülin Perfüzyon ({round(kilo*0.1,1)} Ü/saat), Agresif SF Hidrasyonu, K+ Takibi"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Ağrısı", "Karın Ağrısı", "Murphy Belirtisi", "Hipotansiyon"],
        "tetkik": "Lipaz (3 kat artış), Amilaz, Kontrastlı Batın BT (48. saat)",
        "tedavi": "Oral Stop (NPO), Agresif Sıvı (Ringer Laktat), Analjezi"
    },
    "Nefrotik Sendrom": {
        "bulgu": ["Bilateral Ödem", "Köpüklü İdrar", "Asit", "Halsizlik"],
        "tetkik": "24h İdrar Proteini (>3.5g), Serum Albümin, Lipid Paneli",
        "tedavi": "Steroid (Prednizolon), ACE İnhibitörü, Diüretik, Tuz Kısıtlaması"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Peteşi", "Sabah Sertliği"],
        "tetkik": "ANA, Anti-dsDNA, C3-C4, Tam İdrar (Proteinüri)",
        "tedavi": "Hidroksiklorokin, Sistemik Steroid, İmmünsupresif"
    },
    "KOAH Alevlenme": {
        "bulgu": ["Nefes Darlığı", "Wheezing", "Ral", "Ronküs", "Öksürük"],
        "tetkik": "SFT, Arter Kan Gazı, Akciğer Grafisi",
        "tedavi": "SABA/SAMA Nebül, Sistemik Steroid, Antibiyoterapi, Gerekirse Non-invaziv Mekanik Ventilasyon"
    },
    "Kronik Böbrek Yetmezliği (KBY)": {
        "bulgu": ["Bilateral Ödem", "Hipotansiyon", "Kaşıntı", "Halsizlik", "Oligüri"],
        "tetkik": "eGFR Takibi, PTH, Hemoglobin, Ca/P Dengesi",
        "tedavi": "ACEi/ARB, Tuz/Protein Kısıtlaması, Gerekirse Diyaliz"
    }
}

# 5. ANALİZ MOTORU VE RAPORLAMA
if st.button("🚀 TIBBİ KARAR ROBOTUNU ÇALIŞTIR"):
    if not bulgular:
        st.error("En az bir klinik veri girilmelidir!")
    else:
        sonuclar = []
        for ad, veri in master_database.items():
            eslesme = set(bulgular).intersection(set(veri["bulgu"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": veri, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        c_left, c_right = st.columns([1.6, 1])
        with c_left:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.8rem; color:#000000; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p style='color:#D4AF37; font-weight:700; font-size:1.2rem;'>🎯 Eşleşen Bulgular: {", ".join(s['esles'])}</p>
                    <hr style='border: 1px solid #D4AF37;'>
                    <p>🧪 <b>Gerekli Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Modern Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with c_right:
            st.markdown("### 📝 RESMİ EPİKRİZ RAPORU")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON"
            epikriz = f"""KLİNİK ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
ROBOT: V18 MASTER
PROTOKOL: {p_no}

[VİTAL VE PROFİL]
Cinsiyet: {cinsiyet} | Yaş: {yas} | Kilo: {kilo}kg
eGFR: {egfr} ml/dk | TA: {ta_sis} mmHg

[KLİNİK BULGULAR]
{", ".join(bulgular)}

[DİFERANSİYEL TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[GÜVENLİK NOTU]
- {r_not}
--------------------------------------------------
ONAY: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:45px; border-radius:45px; border:3px solid #D4AF37; font-size:15px;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Arşivine Gönder", epikriz, file_name=f"{p_no}_master.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | TIBBİ KARAR ROBOTU V18 | 2026")
