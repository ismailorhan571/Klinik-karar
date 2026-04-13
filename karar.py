import streamlit as st
from datetime import datetime

# 1. ULTRA-LUXURY BEIGE INTERFACE (NEUMORPHIC GOLD)
st.set_page_config(page_title="İSMAİL ORHAN | Tıbbi Karar Robotu", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp { background: linear-gradient(135deg, #F5F5DC 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);
        padding: 50px; border-radius: 50px; text-align: center; margin-bottom: 40px;
        border: 3px solid #D4AF37; box-shadow: 0 30px 60px rgba(0,0,0,0.1);
    }
    .main-header h1 { 
        color: #000000; font-weight: 800; font-size: 4.5rem; letter-spacing: -3px; margin: 0;
    }
    .main-header p { color: #D4AF37; font-size: 1.6rem; font-weight: 700; margin-top: 10px; }
    
    .clinical-card { 
        background: #FFFFFF; padding: 40px; border-radius: 45px; margin-bottom: 30px;
        border: 1px solid #E2E2E2; box-shadow: 20px 20px 60px #D9D9D9, -20px -20px 60px #FFFFFF;
        border-left: 20px solid #D4AF37; transition: 0.4s ease;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #333333 100%); color: #D4AF37; border-radius: 35px;
        height: 7em; width: 100%; font-weight: 800; font-size: 30px; border: 2px solid #D4AF37;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    .stButton>button:hover { transform: translateY(-5px); box-shadow: 0 30px 60px rgba(0,0,0,0.4); color: #FFD700; }
    
    .alert-premium { 
        background: #991B1B; color: #FFFFFF; padding: 25px; border-radius: 30px;
        font-weight: 800; text-align: center; border: 4px solid #D4AF37; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown(f"""
    <div class='main-header'>
        <h1>TIBBİ KARAR ROBOTU</h1>
        <p>Geliştirici: İSMAİL ORHAN</p>
    </div>
    """, unsafe_allow_html=True)

# 3. YAN PANEL - GENİŞLETİLMİŞ HASTA TERMİNALİ
with st.sidebar:
    st.markdown("### 🤖 HASTA VERİ GİRİŞİ")
    p_no = st.text_input("Protokol / Barkod", "IO-ROBOT-V16")
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 3, 250, 75)
    
    st.divider()
    st.markdown("### 🧪 LABORATUVAR")
    glu = st.number_input("Glukoz (mg/dL)", 0, 1500, 110)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 25.0, 1.2)
    k_plus = st.number_input("Potasyum (mEq/L)", 1.0, 12.0, 4.2)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 30, 300, 120)
    
    # AKILLI eGFR HESAPLAMA (Cinsiyet Faktörlü)
    egfr_base = ((140 - yas) * kilo) / (72 * kre) if kre > 0 else 0
    egfr = round(egfr_base * 0.85 if cinsiyet == "Kadın" else egfr_base, 1)
    
    st.metric(f"eGFR ({cinsiyet})", f"{egfr} ml/dk")
    
    if egfr < 30: st.markdown("<div class='alert-premium'>🚨 RENAL KRİZ: KONTRAST YASAK!</div>", unsafe_allow_html=True)
    if k_plus > 5.8: st.markdown("<div class='alert-premium'>🚨 KRİTİK HİPERKALEMİ!</div>", unsafe_allow_html=True)

# 4. SKORLAMA VE YOĞUN BAKIM MODÜLÜ
st.subheader("📊 Klinik Karar Destek Skorları")
s1, s2, s3 = st.columns(3)
with s1:
    wells = st.multiselect("Wells (PE) Kriterleri", ["DVT Bulgusu (+3)", "Alt. Tanı Az (+3)", "Nabız >100 (+1.5)", "İmmobilite (+1.5)", "Önceki PE (+1.5)", "Hemoptizi (+1)", "Kanser (+1)"])
    st.info(f"Wells Skoru: {len(wells)}")
with s2:
    gks = st.select_slider("GKS (Bilinc Durumu)", options=list(range(3, 16)), value=15)
    if gks <= 8: st.error("⚠️ ENTÜBASYON HAZIRLIĞI YAPILMALI!")
with s3:
    st.markdown("**Sıvı Rezidansı**")
    def_sivi = kilo * 35
    st.success(f"Günlük Bazal İdame: {def_sivi} cc")

# 5. DEVASA DAHİLİYE BİLGİ KÜTÜPHANESİ (Hastalık + Bulgu + Tetkik + Tedavi)
st.subheader("🔍 Klinik Bulguları Eksiksiz İşleyin")
tabs = st.tabs(["🧬 SİSTEMİK", "🫀 KALP-AKCİĞER", "🤢 GİS-KC-BATIN", "🧪 ENDO-RENAL", "🩸 ROMATO-HEMATO", "💊 TOKSİKO-YOĞUN BAKIM"])

bulgular = []
with tabs[0]: bulgular.extend(st.multiselect("Bulgu", ["Ateş", "Kilo Kaybı", "Gece Terlemesi", "Halsizlik", "Kaşıntı", "Lenfadenopati", "Anemi Bulguları"]))
with tabs[1]: bulgular.extend(st.multiselect("Bulgu ", ["Nefes Darlığı", "Göğüs Ağrısı", "Ortopne", "PND", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Boyun Ven Dolgunluğu", "Taşikardi", "Ral", "Ronküs"]))
with tabs[2]: bulgular.extend(st.multiselect("Bulgu  ", ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae", "Hematemez", "Melena", "Kuşak Ağrısı", "Karın Ağrısı"]))
with tabs[3]: bulgular.extend(st.multiselect("Bulgu   ", ["Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Köpüklü İdrar", "Ekzoftalmi"]))
with tabs[4]: bulgular.extend(st.multiselect("Bulgu    ", ["Peteşi", "Purpura", "Kelebek Döküntü", "Raynaud", "Sabah Sertliği", "Eklem Ağrısı", "Ağızda Aft", "Deri Sertleşmesi"]))
with tabs[5]: bulgular.extend(st.multiselect("Bulgu     ", ["Miyozis", "Midriyazis", "Hipotoni", "Karakteristik Koku", "Bradikardi", "Konfüzyon", "Paraneoplastik Bulgular"]))

# 6. MASTER DAHİLİYE VERİ TABANI
master_database = {
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Hepatomegali", "Splenomegali", "Asteriksis", "Caput Medusae"],
        "tetkik": "INR, Albümin, Amonyak, Batın USG, Portal Doppler, Gastroskopi",
        "tedavi": "Spironolakton + Furosemid, Laktüloz, Tuz Kısıtlaması, Varis varsa Propranolol"
    },
    "Diyabetik Ketoasidoz (DKA)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Karın Ağrısı", "Konfüzyon"],
        "tetkik": "Kan Gazı (pH < 7.3), İdrar Ketoni, Glukoz > 250, Anyon Açığı",
        "tedavi": f"İnsülin Perfüzyon ({round(kilo*0.1,1)} Ü/saat), Agresif SF Hidrasyonu, K+ Takibi"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Hemoptizi", "Unilateral Ödem", "Nefes Darlığı", "Taşikardi", "Göğüs Ağrısı"],
        "tetkik": "BT Anjiyo, D-Dimer, Troponin, EKG (S1Q3T3)",
        "tedavi": f"Düşük Molekül Ağırlıklı Heparin ({kilo}mg 2x1), Stabil değilse Trombolitik"
    },
    "Kalp Yetmezliği (KKY)": {
        "bulgu": ["Bilateral Ödem", "Ortopne", "PND", "Boyun Ven Dolgunluğu", "Ral"],
        "tetkik": "NT-proBNP, EKO (EF Ölçümü), PA Akciğer Grafisi",
        "tedavi": "IV Furosemid, ACEi, Beta Bloker, SGLT2 İnhibitörü"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Peteşi", "Fotosensitivite"],
        "tetkik": "ANA, Anti-dsDNA, C3-C4 Seviyeleri, Tam İdrar (Proteinüri)",
        "tedavi": "Hidroksiklorokin, Sistemik Steroid, İmmünsupresifler"
    },
    "Menedjit (Bakteriyel)": {
        "bulgu": ["Ateş", "Ense Sertliği", "Konfüzyon", "Ani Baş Ağrısı"],
        "tetkik": "Lomber Ponksiyon (BOS Analizi), Kan Kültürü, Kafa BT",
        "tedavi": "Seftriakson 2x2g + Vankomisin + Deksametazon"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Ağrısı", "Karın Ağrısı", "Bulantı-Kusma"],
        "tetkik": "Lipaz (Spesifik), Amilaz, Kontrastlı Batın BT",
        "tedavi": "NPO (Oral Stop), Agresif Sıvı Rezidansı (Ringer Laktat)"
    },
    "Addison Krizi": {
        "bulgu": ["Hiperpigmentasyon", "Halsizlik", "Tuz Açlığı", "Hipotansiyon"],
        "tetkik": "Sabah Kortizolü, ACTH Stimülasyon, Na (Düşük), K (Yüksek)",
        "tedavi": "IV Hidrokortizon 100mg + Agresif Sıvı Hidrasyonu"
    },
    "Nefrotik Sendrom": {
        "bulgu": ["Bilateral Ödem", "Köpüklü İdrar", "Asit", "Halsizlik"],
        "tetkik": "24h İdrar Proteini (>3.5g), Serum Albümin, Lipid Paneli",
        "tedavi": "Prednizolon, ACE İnhibitörü, Diüretik, Tuz Kısıtlaması"
    },
    "Wegener (GPA)": {
        "bulgu": ["Hemoptizi", "Peteşi", "Purpura", "Nefes Darlığı"],
        "tetkik": "c-ANCA, Akciğer BT, Böbrek Biyopsisi",
        "tedavi": "Pulse Steroid (1g) + Siklofosfamid/Rituksimab"
    }
}

# 7. ANALİZ MOTORU
if st.button("🚀 TIBBİ KARAR ROBOTUNU ÇALIŞTIR"):
    if not bulgular:
        st.error("Lütfen klinik bulgu seçimi yapınız!")
    else:
        sonuclar = []
        for ad, veri in master_database.items():
            eslesme = set(bulgular).intersection(set(veri["bulgu"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": veri, "esles": eslesme})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        col_r1, col_r2 = st.columns([1.6, 1])
        with col_r1:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            for s in sonuclar:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.3rem; color:#000000; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p style='color:#D4AF37; font-weight:700;'>🎯 Tespit Edilen Bulgular: {", ".join(s['esles'])}</p>
                    <hr style='border: 1px solid #E2E2E2;'>
                    <p>🧪 <b>İstenmesi Gereken Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Modern Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)

        with col_r2:
            st.markdown("### 📝 RESMİ EPİKRİZ RAPORU")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON"
            epikriz = f"""TIBBİ KARAR ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
ROBOT VERSİYONU: V16
PROTOKOL: {p_no}

[HASTA PROFİLİ VE VİTALLER]
Cinsiyet: {cinsiyet} | Yaş: {yas} | Kilo: {kilo}kg
eGFR: {egfr} ml/dk (Cinsiyet düzeltmeli)
Glukoz: {glu} | Potasyum: {k_plus} | TA: {ta_sis}

[KLİNİK BULGULAR]
{", ".join(bulgular)}

[DİFERANSİYEL TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[GÜVENLİK NOTLARI]
- Radyoloji: {r_not}
- GKS: {gks} | Günlük Sıvı: {def_sivi}cc
--------------------------------------------------
ONAY VE İMZA: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:40px; border-radius:40px; border:3px solid #D4AF37; font-size:15px; box-shadow: 10px 10px 30px rgba(0,0,0,0.05);'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Raporu PDF Arşivine Al", epikriz, file_name=f"{p_no}_final.txt")

st.markdown("---")
st.caption("Geliştirici: İSMAİL ORHAN | TIBBİ KARAR ROBOTU V16 | 2026")
