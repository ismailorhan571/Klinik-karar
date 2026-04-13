import streamlit as st

# 1. Sayfa Konfigürasyonu ve Premium CSS (Geliştirilmiş)
st.set_page_config(page_title="Dahiliye CDSS Pro Max", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); color: #f8fafc; }
    .header-box {
        background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(15px);
        padding: 40px; border-radius: 24px; border: 1px solid rgba(59, 130, 246, 0.2);
        text-align: center; margin-bottom: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px; padding: 12px 20px; color: #94a3b8; margin-right: 5px;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important; color: white !important;
    }
    .diagnose-card {
        background: rgba(239, 68, 68, 0.05); padding: 25px; border-radius: 20px;
        border: 1px solid rgba(239, 68, 68, 0.3); box-shadow: 0 10px 30px rgba(239, 68, 68, 0.1);
        margin-bottom: 20px;
    }
    .test-card {
        background: rgba(34, 197, 94, 0.05); padding: 25px; border-radius: 20px;
        border: 1px solid rgba(34, 197, 94, 0.3); box-shadow: 0 10px 30px rgba(34, 197, 94, 0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
        color: white; border: none; border-radius: 18px; height: 4.5em;
        font-weight: 900; font-size: 18px; letter-spacing: 1.5px; transition: 0.4s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 30px rgba(37, 99, 235, 0.6); }
    h1, h2, h3 { color: #f8fafc !important; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.markdown("""
    <div class='header-box'>
        <h1 style='margin:0;'>⚕️ DAHİLİYE KARAR DESTEK SİSTEMİ PRO MAX</h1>
        <p style='font-size: 1.3em; color: #38bdf8; margin-top:10px;'><b>Geliştirici: İSMAİL ORHAN | Versiyon 11.0 (Full Algoritma)</b></p>
    </div>
    """, unsafe_allow_html=True)

# 3. Sidebar (Vital Veri Merkezi)
with st.sidebar:
    st.markdown("### 📊 HASTA VİTALLERİ")
    yas = st.number_input("Yaş", 0, 120, 45)
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 40, 100, 98)
    kan_sekeri = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 100)
    st.divider()
    if kan_sekeri > 250 or kan_sekeri < 60: st.error("🚨 GLİSEMİK KRİZ!")
    if ta_sis > 180 or ta_dia > 110: st.error("🚨 HİPERTANSİF ACİL!")

# 4. Devasa Semptom Giriş Alanı
st.markdown("### 🔍 KLİNİK BULGU VE BELİRTİ SEÇİMİ")
tabs = st.tabs(["🩺 GİS & Karaciğer", "🫁 Kardiyo & Solunum", "🧠 Nöro & Psikiyatri", "🦋 Romatoloji & Deri", "🧪 Endokrin & Nefro", "🧬 Hemato & Onko"])

secilen = []
with tabs[0]:
    c1, c2 = st.columns(2)
    with c1: secilen.extend(st.multiselect("Üst GİS", ["Hematemez", "Melena", "Disfaji", "Epigastrik Ağrı", "Grey Turner", "Cullen", "Murphy Belirtisi (+)"]))
    with c2: secilen.extend(st.multiselect("Hepato/Alt GİS", ["Sarılık", "Asit", "Caput Medusae", "Asteriksis", "Hematokezya", "Sağ Alt Kadran Ağrısı", "Rebound (+)"]))

with tabs[1]:
    c3, c4 = st.columns(2)
    with c3: secilen.extend(st.multiselect("Kardiyo", ["Baskı Tarzı Göğüs Ağrısı", "S3 Galo", "Janeway Lezyonları", "Osler Nodülleri", "PND", "Boyun Ven Dolgunluğu"]))
    with c4: secilen.extend(st.multiselect("Solunum", ["Hemoptizi", "Plevritik Ağrı", "Çomak Parmak", "Stridor", "Wheezing", "VCS Sendromu (Yüz Şişliği)"]))

with tabs[2]:
    secilen.extend(st.multiselect("Nörolojik", ["Ani Baş Ağrısı", "Ense Sertliği", "Fokal Güç Kaybı", "Dizartri", "Miyozis", "Midriyazis", "Ataksi", "Konfüzyon"]))

with tabs[3]:
    c5, c6 = st.columns(2)
    with c5: secilen.extend(st.multiselect("Deri/Eklemler", ["Kelebek Döküntü", "Raynaud Fenomeni", "Eritema Nodosum", "Helitrop Raş", "Sabah Sertliği", "Purpura (Palpabl)"]))
    with c6: secilen.extend(st.multiselect("Özel", ["Oral/Genital Aft", "Göz Kuruluğu", "Bambu Omurga", "Paterji (+)", "Uveit"]))

with tabs[4]:
    c7, c8 = st.columns(2)
    with c7: secilen.extend(st.multiselect("Endokrin", ["Poliüri", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Ekzoftalmi", "Hiperpigmentasyon", "Sıcak İntoleransı"]))
    with c8: secilen.extend(st.multiselect("Nefroloji", ["Oligüri", "Hematüri", "Köpüklü İdrar", "Üremik Koku", "Periorbital Ödem", "Flank Ağrısı"]))

with tabs[5]:
    secilen.extend(st.multiselect("Hemato/Onko", ["Solukluk", "Diş Eti Kanaması", "Lenfadenopati", "Splenomegali", "B-Semptomları", "Kemik Ağrısı", "Schistosit Şüphesi"]))

# 5. DEVASA TANI VE TETKİK MOTORU (PRO MAX)
def pro_max_engine(b_list, v):
    tanilar, tetkikler = set(), {"Hemogram", "CRP", "Biyokimya Seti", "TİT", "EKG"}
    b = set(b_list)
    ates, ta_s, spo2, seker, yas = v

    # --- KRİTİK ALGORİTMALAR ---
    # Kardiyo-Pulmoner
    if "Baskı Tarzı Göğüs Ağrısı" in b: tanilar.add("MI / AKS"); tetkikler.update(["Seri Troponin", "EKO", "Anjiografi"])
    if "VCS Sendromu (Yüz Şişliği)" in b: tanilar.add("Onkolojik Acil: VCS Obstrüksiyonu"); tetkikler.update(["Toraks BT Anjiyo", "Biyopsi"])
    if "Hemoptizi" in b and "Plevritik Ağrı" in b: tanilar.add("Pulmoner Emboli"); tetkikler.update(["D-Dimer", "Toraks BT Anjiyo"])
    
    # Endokrin (Genişletilmiş)
    if "Aseton Kokusu" in b and seker > 250: tanilar.add("Diyabetik Ketoasidoz (DKA)"); tetkikler.update(["Veböz Kan Gazı", "Keton"])
    if "Hiperpigmentasyon" in b and ta_s < 90: tanilar.add("Addison Krizi (Adrenal Yetmezlik)"); tetkikler.update(["Kortizol", "ACTH", "Na/K Oranı"])
    if "Sıcak İntoleransı" in b and "Ekzoftalmi" in b: tanilar.add("Tirotoksikoz / Graves"); tetkikler.update(["TSH, sT3, sT4", "Tiroid USG"])
    if ates < 35.5 and "Konfüzyon" in b: tanilar.add("Miksödem Koması"); tetkikler.update(["TSH", "Serbest T4", "Kortizol"])

    # Hemato-Onkoloji (Genişletilmiş)
    if "Schistosit Şüphesi" in b and "Konfüzyon" in b: tanilar.add("TTP / HUS (Hematolojik Acil)"); tetkikler.update(["Periferik Yayma", "LDH", "İndirekt Bilirubin", "ADAMTS13"])
    if "B-Semptomları" in b and "Lenfadenopati" in b: tanilar.add("Lenfoma / Tüberküloz"); tetkikler.update(["Lenf Nodu Biyopsisi", "LDH", "Toraks/Batın BT"])
    if "Kemik Ağrısı" in b and yas > 50: tanilar.add("Multipl Myelom"); tetkikler.update(["Protein Elektroforezi", "Kalsiyum", "Kemik İliği"])

    # Romatoloji & Vaskülit (Genişletilmiş)
    if "Purpura (Palpabl)" in b and "Hematüri" in b: tanilar.add("Vaskülit (GPA / IgA Vasküliti)"); tetkikler.update(["ANCA Paneli", "Böbrek Biyopsisi", "C3-C4"])
    if "Oral/Genital Aft" in b and "Paterji (+)" in b: tanilar.add("Behçet Hastalığı"); tetkikler.update(["Göz Muayenesi", "HLA-B51"])
    if "Helitrop Raş" in b: tanilar.add("Dermatomiyozit"); tetkikler.update(["CK", "Aldolaz", "Kas Biyopsisi"])

    # GİS & Karaciğer
    if "Asteriksis" in b and "Sarılık" in b: tanilar.add("Hepatik Ensefalopati"); tetkikler.update(["Amonyak", "Batın USG", "PT/INR"])
    if "Grey Turner" in b or "Cullen" in b: tanilar.add("Nekrotizan Pankreatit"); tetkikler.update(["Amilaz/Lipaz", "Kontrastlı BT"])
    if "Murphy Belirtisi (+)" in b: tanilar.add("Akut Kolesistit"); tetkikler.update(["USG", "Bilirubinler"])

    # Nöroloji
    if "Ani Baş Ağrısı" in b and "Ense Sertliği" in b: tanilar.add("SAK / Menenjit"); tetkikler.update(["Beyin BT", "Lomber Ponksiyon"])
    if "Fokal Güç Kaybı" in b: tanilar.add("İskemik/Hemorajik SVO"); tetkikler.update(["Beyin BT / Difüzyon MR"])

    return sorted(list(tanilar)), sorted(list(tetkikler))

# 6. Analiz Tetikleyici
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 PRO MAX ANALİZİ ÇALIŞTIR"):
    if not secilen and ates == 36.6 and kan_sekeri == 100:
        st.warning("⚠️ Lütfen belirti giriniz veya vitalleri güncelleyiniz.")
    else:
        v_data = (ates, ta_sis, spo2, kan_sekeri, yas)
        tanilar, tetkikler = pro_max_engine(secilen, v_data)
        
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.markdown("<div class='diagnose-card'><h2>🚨 OLASI TANILAR</h2>", unsafe_allow_html=True)
            if tanilar:
                for t in tanilar: st.write(f"🏷️ **{t}**")
            else: st.info("Spesifik bir sendrom saptanmadı. Klinik izlem önerilir.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_res2:
            st.markdown("<div class='test-card'><h2>🧪 İLERİ TETKİKLER</h2>", unsafe_allow_html=True)
            for tet in tetkikler: st.write(f"💉 {tet}")
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Footer
st.markdown("---")
st.markdown("<p style='text-align: center; opacity: 0.6;'>Dahiliye Pro Max v11.0 | İSMAİL ORHAN | Akademik ve Klinik Referanslıdır.</p>", unsafe_allow_html=True)
