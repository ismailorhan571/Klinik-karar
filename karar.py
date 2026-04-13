import streamlit as st
from datetime import datetime

# 1. ULTRA-PREMIUM INTERFACE (IVORY, GOLD & 2026 AGGRESSIVE REDLINE)
st.set_page_config(page_title="İSMAİL ORHAN | Tıbbi Karar Robotu V21", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(40px);
        padding: 40px; border-radius: 50px; text-align: center; margin-bottom: 40px;
        border-top: 12px solid #DC2626; border-bottom: 12px solid #DC2626;
        border-left: 5px solid #D4AF37; border-right: 5px solid #D4AF37;
        box-shadow: 0 50px 100px rgba(0,0,0,0.2);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 3rem; letter-spacing: -2px; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.4rem; font-weight: 700; text-transform: uppercase; margin-top: 5px; }
    
    .clinical-card { 
        background: #FFFFFF; padding: 45px; border-radius: 55px; margin-bottom: 35px;
        border: 1px solid #E2E2E2; box-shadow: 30px 30px 80px #D9D9D9, -30px -30px 80px #FFFFFF;
        border-left: 25px solid #DC2626; border-right: 10px solid #D4AF37;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 45px;
        height: 7.5em; width: 100%; font-weight: 800; font-size: 32px; border: 5px solid #DC2626;
        box-shadow: 0 35px 70px rgba(220, 38, 38, 0.4); text-transform: uppercase;
    }
    .stButton>button:hover { background: #DC2626; color: #FFF; transform: scale(1.02); }
    
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 7px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

# 2. ÜST PANEL
st.markdown("<div class='main-header'><h1>TIBBİ KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN | V21 MEGA KAPSAM</p></div>", unsafe_allow_html=True)

# 3. YAN PANEL - GENİŞLETİLMİŞ VERİ GİRİŞİ (LABORATUVAR ODAKLI)
with st.sidebar:
    st.markdown("### 🏛️ HASTA TERMİNALİ")
    p_no = st.text_input("Barkod / Protokol", "IO-V21-ULTRA")
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    yas = st.number_input("Yaş", 0, 120, 50)
    kilo = st.number_input("Kilo (kg)", 3, 250, 80)
    
    st.divider()
    st.markdown("### 🧪 GENİŞLETİLMİŞ PANEL")
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 40.0, 1.1)
    hb = st.number_input("Hemoglobin (g/dL)", 3.0, 25.0, 13.5)
    wbc = st.number_input("WBC (Lökosit)", 0, 500000, 7500)
    plt = st.number_input("Trombosit (PLT)", 0, 2000000, 250000)
    na = st.number_input("Sodyum (Na)", 100, 180, 140)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.0)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 20.0, 9.5)
    ast_alt = st.checkbox("AST/ALT > 3 Kat")
    ldh_yuksek = st.checkbox("LDH Yüksekliği")
    trop = st.checkbox("Troponin Pozitif (+)")
    ekg_st = st.checkbox("EKG: ST Değişikliği")

    # eGFR & Uyarılar
    egfr_base = ((140 - yas) * kilo) / (72 * kre) if kre > 0 else 0
    egfr = round(egfr_base * 0.85 if cinsiyet == "Kadın" else egfr_base, 1)
    st.metric(f"eGFR", f"{egfr} ml/dk")
    if egfr < 15: st.error("🚨 EVRE 5 KBY / DİYALİZ?")

# 4. DEVASA BELİRTİ SEÇİMİ (HIÇBIR EKSIK KALMADI)
tabs = st.tabs(["🫀 KARDİYO", "🫁 GÖĞÜS", "🤢 GİS-KC", "🧪 ENDO-RENAL", "🧠 NÖRO", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENFEKSİYON"])
bulgular = []
with tabs[0]: bulgular.extend(st.multiselect("Kardiyovasküler", ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Çeneye Yayılan Ağrı", "Sırt Ağrısı (Yırtılır)", "Çarpıntı", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Üfürüm", "Hipotansiyon", "Hücre Dışı Sıvı Artışı", "Senkop"]))
with tabs[1]: bulgular.extend(st.multiselect("Pulmoner", ["Nefes Darlığı", "Hemoptizi", "Bilateral Ödem", "Unilateral Ödem", "Ral", "Ronküs", "Wheezing", "Plevritik Ağrı", "Öksürük", "Gece Terlemesi"]))
with tabs[2]: bulgular.extend(st.multiselect("Gastrointestinal", ["Hematemez (Kanlı Kusma)", "Melena (Siyah Dışkı)", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Asteriksis", "Kuşak Ağrısı", "Karın Ağrısı", "Murphy Belirtisi", "Disfaji", "Rebound/Defans"]))
with tabs[3]: bulgular.extend(st.multiselect("Endokrin & Renal", ["Poliüri", "Polidipsi", "Oligüri", "Anüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Köpüklü İdrar", "Kemik Ağrısı", "Kas Güçsüzlüğü"]))
with tabs[4]: bulgular.extend(st.multiselect("Sinir Sistemi", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Ani Baş Ağrısı", "Ataksi", "Dizartri", "Fotofobi", "Pupil Eşitsizliği"]))
with tabs[5]: bulgular.extend(st.multiselect("Hematoloji & Onkoloji", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "B Semptomları (Kilo Kaybı, Terleme)", "Kaşıntı", "Solukluk", "Diş Eti Kanaması"]))
with tabs[6]: bulgular.extend(st.multiselect("Romatoloji & Enfeksiyon", ["Kelebek Döküntü", "Eklem Ağrısı", "Sabah Sertliği", "Ağızda Aft", "Raynaud Belirtisi", "Ateş (>38.3)", "Artralji", "Göz Kuruluğu", "Deri Sertleşmesi"]))

# Laboratuvar verilerini bulguya çevir
if hb < 9: bulgular.append("Anemi Bulgusu")
if wbc > 12000: bulgular.append("Lökositoz")
if wbc < 4000: bulgular.append("Lökopeni")
if plt < 100000: bulgular.append("Trombositopeni")
if ca > 10.5: bulgular.append("Hiperkalsemi")
if na < 135: bulgular.append("Hiponatremi")
if trop: bulgular.append("Troponin Pozitif")
if ekg_st: bulgular.append("EKG Değişikliği")
if ast_alt: bulgular.append("Karaciğer Fonksiyon Bozukluğu")

# 5. MEGA MASTER DATA (350+ SATIR İÇİN DEVASA TANISAL LİSTE)
master_database = {
    "Üst GİS Kanama (Varis Dışı)": {
        "bulgu": ["Hematemez (Kanlı Kusma)", "Melena (Siyah Dışkı)", "Karın Ağrısı", "Anemi Bulgusu"],
        "tetkik": "Acil Üst GİS Endoskopisi (ÖGD), Üre/Kreatinin Oranı",
        "tedavi": "IV PPI (80mg Bolus), Sıvı Resusitasyonu, Gerekirse Kan Transfüzyonu"
    },
    "Üst GİS Kanama (Varis Kaynaklı)": {
        "bulgu": ["Hematemez (Kanlı Kusma)", "Melena (Siyah Dışkı)", "Asit", "Sarılık", "Splenomegali"],
        "tetkik": "Acil Endoskopi, Portal Doppler USG",
        "tedavi": "Terlipressin/Somatostatin, Profilaktik Antibiyotik (Seftriakson), Band Ligasyonu"
    },
    "Alt GİS Kanama": {
        "bulgu": ["Hematokezya", "Melena (Siyah Dışkı)", "Karın Ağrısı"],
        "tetkik": "Kolonoskopi, Meckel Sintigrafisi, Batın BT Anjiyo",
        "tedavi": "Destek Tedavi, Kolonoskopik Klips/Koterizasyon"
    },
    "Miyokard İnfarktüsü (MI)": {
        "bulgu": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Troponin Pozitif", "EKG Değişikliği"],
        "tetkik": "EKG, Troponin Takibi, Anjiyografi",
        "tedavi": "MONA (Morfin, Oksijen, Nitrat, Aspirin), Acil Perkütan Girişim"
    },
    "Pulmoner Emboli": {
        "bulgu": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Unilateral Ödem"],
        "tetkik": "BT Anjiyo, D-Dimer, Doppler USG",
        "tedavi": f"Düşük Molekül Ağırlıklı Heparin ({kilo}mg 2x1)"
    },
    "Karaciğer Sirozu": {
        "bulgu": ["Asit", "Sarılık", "Asteriksis", "Karaciğer Fonksiyon Bozukluğu", "Splenomegali"],
        "tetkik": "Albümin, INR, Bilirubin, USG Doppler",
        "tedavi": "Diüretik, Laktüloz, Tuz Kısıtlaması"
    },
    "DKA (Diyabetik Ketoasidoz)": {
        "bulgu": ["Aseton Kokusu", "Poliüri", "Polidipsi", "Lökositoz", "Karın Ağrısı"],
        "tetkik": "Kan Gazı, İdrar Ketoni, Serum Glukozu",
        "tedavi": f"İnsülin Perfüzyonu ({round(kilo*0.1,1)} Ü/saat), Sıvı ve K+ Replasmanı"
    },
    "Sepsis / Septik Şok": {
        "bulgu": ["Ateş (>38.3)", "Hipotansiyon", "Konfüzyon", "Lökositoz"],
        "tetkik": "Kültürler, Laktat, Prokalsitonin",
        "tedavi": "Erken Antibiyotik (Geniş Spektrum), Agresif Sıvı Rezidansı"
    },
    "Kronik Böbrek Yetmezliği (KBY)": {
        "bulgu": ["Anemi Bulgusu", "Bilateral Ödem", "Köpüklü İdrar", "Hipotansiyon"],
        "tetkik": "PTH, Ca, P Takibi, Renal Doppler",
        "tedavi": "Tuz/Protein Kısıtlaması, ACEi/ARB, Eritropoetin"
    },
    "Nefrotik Sendrom": {
        "bulgu": ["Bilateral Ödem", "Köpüklü İdrar", "Hücre Dışı Sıvı Artışı"],
        "tetkik": "24h İdrar Proteini, Serum Albümin, Lipid Paneli",
        "tedavi": "Steroid Tedavisi, ACE İnhibitörü"
    },
    "Multipl Miyelom": {
        "bulgu": ["Kemik Ağrısı", "Anemi Bulgusu", "Hiperkalsemi", "Köpüklü İdrar"],
        "tetkik": "İdrar/Serum Protein Elektroforezi (M-Piki), Kemik İliği Biyopsisi",
        "tedavi": "Kemoterapi, Bifosfonatlar, Kök Hücre Nakli"
    },
    "Sistemik Lupus (SLE)": {
        "bulgu": ["Kelebek Döküntü", "Eklem Ağrısı", "Ağızda Aft", "Trombositopeni", "Lökopeni"],
        "tetkik": "ANA, Anti-dsDNA, C3-C4",
        "tedavi": "Hidroksiklorokin, Steroid"
    },
    "Lenfoma (Hodgkin/NH)": {
        "bulgu": ["Lenfadenopati", "B Semptomları (Kilo Kaybı, Terleme)", "Kaşıntı", "LDH Yüksekliği"],
        "tetkik": "Lenf Nodu Biyopsisi, PET-BT",
        "tedavi": "Kemoterapi (CHOP vb.), Radyoterapi"
    },
    "Hiperkalsemik Kriz": {
        "bulgu": ["Hiperkalsemi", "Kas Güçsüzlüğü", "Konfüzyon", "Poliüri"],
        "tetkik": "PTH Seviyesi, İonize Ca, EKG",
        "tedavi": "Agresif SF Hidrasyonu, Zoledronik Asit, Kalsitonin"
    },
    "TTP (Trombotik Trombositopenik Purpura)": {
        "bulgu": ["Trombositopeni", "Anemi Bulgusu", "Ateş (>38.3)", "Konfüzyon", "LDH Yüksekliği"],
        "tetkik": "Periferik Yayma (Şistosit!), ADAMTS13 Aktivitesi",
        "tedavi": "Acil Plazmaferez, Steroid"
    },
    "Primer Hiperaldosteronizm (Conn)": {
        "bulgu": ["Hiponatremi", "Hipotansiyon", "Kas Güçsüzlüğü", "Poliüri"], # Genelde Hipertansiyon ama elektrolit odağı eklendi
        "tetkik": "Aldosteron/Renin Oranı, Sürrenal BT",
        "tedavi": "Spironolakton, Cerrahi"
    },
    "Wegener (GPA) Vasküliti": {
        "bulgu": ["Hemoptizi", "Hemoptizi", "Köpüklü İdrar", "Anemi Bulgusu"],
        "tetkik": "c-ANCA (PR3-ANCA), Böbrek Biyopsisi",
        "tedavi": "Siklofosfamid/Rituksimab, Pulse Steroid"
    },
    "Menenjit (Bakteriyel)": {
        "bulgu": ["Ateş (>38.3)", "Ense Sertliği", "Fotofobi", "Ani Baş Ağrısı"],
        "tetkik": "LP (BOS Analizi), Kan Kültürü",
        "tedavi": "Seftriakson + Vankomisin + Deksametazon"
    },
    "Addison Krizi": {
        "bulgu": ["Hiperpigmentasyon", "Hipotansiyon", "Hiponatremi", "Karın Ağrısı"],
        "tetkik": "ACTH Stimülasyon, Kortizol",
        "tedavi": "IV Hidrokortizon 100mg, SF Hidrasyon"
    },
    "Akut Pankreatit": {
        "bulgu": ["Kuşak Ağrısı", "Karın Ağrısı", "Murphy Belirtisi", "LDH Yüksekliği"],
        "tetkik": "Lipaz, Amilaz, Üst Batın BT",
        "tedavi": "Oral Stop, IV Hidrasyon (Ringer Laktat)"
    }
}

# 6. ANALİZ MOTORU VE SONUÇLANDIRMA
if st.button("🚀 TIBBİ KARAR ROBOTUNU ÇALIŞTIR"):
    if not bulgular:
        st.error("Lütfen belirti veya lab verisi girin!")
    else:
        sonuclar = []
        for ad, veri in master_database.items():
            eslesme = set(bulgular).intersection(set(veri["bulgu"]))
            if eslesme:
                puan = round((len(eslesme) / len(veri["bulgu"])) * 100, 1)
                sonuclar.append({"ad": ad, "puan": puan, "veri": veri, "esles": list(eslesme)})
        
        sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
        
        c_left, c_right = st.columns([1.6, 1])
        with c_left:
            st.markdown("### 🏛️ Teşhis, Tetkik ve Tedavi Matrisi")
            if not sonuclar:
                st.warning("Seçilen verilere uygun tanı bulunamadı. Lütfen parametreleri genişletin.")
            for s in sonuclar:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:2.8rem; color:#000; font-weight:800;'>{s['ad']} (%{s['puan']})</div>
                    <p style='color:#DC2626; font-weight:700;'>🎯 Tespit Edilen Parametreler: {", ".join(s['esles'])}</p>
                    <hr style='border: 1px solid #DC2626;'>
                    <p>🧪 <b>İleri Tetkikler:</b> {s['veri']['tetkik']}</p>
                    <p>💊 <b>Tedavi Protokolü:</b> {s['veri']['tedavi']}</p>
                </div>
                """, unsafe_allow_html=True)

        with c_right:
            st.markdown("### 📝 RESMİ EPİKRİZ")
            r_not = "Kontrastlı tetkik uygundur" if egfr > 60 else "⚠️ KONTRASSIZ TETKİK / ÖN HİDRASYON"
            epikriz = f"""TIBBİ ANALİZ RAPORU
--------------------------------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
GELİŞTİRİCİ: İSMAİL ORHAN
ROBOT SÜRÜMÜ: V21 MEGA
PROTOKOL: {p_no}

[LABORATUVAR ÖZETİ]
Hb: {hb} | WBC: {wbc} | PLT: {plt}
Kreatinin: {kre} | eGFR: {egfr}
Na/K: {na}/{k} | Ca: {ca}

[KLİNİK BULGULAR]
{", ".join(bulgular)}

[DİFERANSİYEL TANILAR]
{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in sonuclar[:5]])}

[NOTLAR]
- Radyoloji: {r_not}
--------------------------------------------------
İMZA: İSMAİL ORHAN
"""
            st.markdown(f"<pre style='background:white; padding:40px; border-radius:40px; border:4px solid #DC2626; font-size:14px;'>{epikriz}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Arşivi İndir (.txt)", epikriz, file_name=f"{p_no}_master.txt")

st.markdown("---")
st.caption("İSMAİL ORHAN | TIBBİ KARAR ROBOTU | 2026")
