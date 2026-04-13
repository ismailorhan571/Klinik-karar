import streamlit as st

# 1. Sayfa Ayarları ve Ultra Web Tasarımı
st.set_page_config(page_title="Dahiliye CDSS Ultimate v13", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(160deg, #020617 0%, #0f172a 100%); color: #f8fafc; }
    .header-container {
        background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(20px);
        padding: 50px; border-radius: 30px; border: 1px solid rgba(56, 189, 248, 0.3);
        text-align: center; margin-bottom: 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.6);
    }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 15px 25px; color: #94a3b8; font-weight: 700;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important; color: white !important;
    }
    .diagnose-box {
        background: rgba(239, 68, 68, 0.1); padding: 30px; border-radius: 25px;
        border: 2px solid #ef4444; margin-bottom: 25px;
    }
    .test-box {
        background: rgba(16, 185, 129, 0.1); padding: 30px; border-radius: 25px;
        border: 2px solid #10b981; margin-bottom: 25px;
    }
    .treatment-box {
        background: rgba(59, 130, 246, 0.1); padding: 30px; border-radius: 25px;
        border: 2px solid #3b82f6;
    }
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #d946ef);
        color: white; border: none; border-radius: 20px; height: 5em;
        font-weight: 900; font-size: 20px; text-transform: uppercase;
        letter-spacing: 3px; box-shadow: 0 15px 40px rgba(59, 130, 246, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.markdown("""
    <div class='header-container'>
        <h1 style='font-size: 3em; margin: 0; background: -webkit-linear-gradient(#38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            DAHİLİYE CDSS - ULTIMATE PRO MAX
        </h1>
        <p style='font-size: 1.4em; color: #94a3b8;'><b>Geliştirici: İSMAİL ORHAN | Versiyon 13.0 (Kapsamlı Tanı & Tedavi)</b></p>
    </div>
    """, unsafe_allow_html=True)

# 3. Sidebar: Vital Veri Merkezi
with st.sidebar:
    st.markdown("### 📊 VİTAL PARAMETRELER")
    yas = st.number_input("Yaş", 0, 120, 45)
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA", 30, 150, 80)
    nabiz = st.number_input("Nabız", 30, 250, 80)
    spo2 = st.slider("SpO2 (%)", 40, 100, 98)
    kan_sekeri = st.number_input("Kan Şekeri (mg/dL)", 20, 1000, 100)
    st.divider()
    if spo2 < 90: st.error("🚨 HİPOKSİ!")
    if ta_sis < 90: st.error("🚨 HİPOTANSİF ŞOK?")

# 4. Devasa Semptom Girişi
st.subheader("🔍 Klinik Bulgular (Genişletilmiş Veri Seti)")
tabs = st.tabs(["🩺 GİS", "🫁 Kardiyo & Solunum", "🧠 Nöro", "🦋 Romatoloji", "🧪 Endokrin", "🧬 Hemato/Onko", "🐍 Toksikoloji"])

secilen = []
with tabs[0]: # GİS
    secilen.extend(st.multiselect("Gastrointestinal", ["Hematemez", "Melena", "Hematokezya", "Disfaji", "Odinofaji", "Sarılık", "Asit", "Caput Medusae", "Asteriksis", "Grey Turner", "Cullen", "Murphy (+)", "Rebound (+)", "Kabızlık (Kronik)", "Steatore"]))
with tabs[1]: # Kardiyo
    secilen.extend(st.multiselect("Kardiyopulmoner", ["Baskı Tarzı Göğüs Ağrısı", "Plevritik Ağrı", "Hemoptizi", "PND", "Ortopne", "Çarpıntı", "Senkop", "Çomak Parmak", "Bacak Şişliği (Tek)", "VCS Sendromu"]))
with tabs[2]: # Nöro
    secilen.extend(st.multiselect("Nöroloji", ["Ani Baş Ağrısı", "Ense Sertliği", "Fokal Güç Kaybı", "Dizartri", "Konfüzyon", "Ataksi", "Miyozis", "Midriyazis"]))
with tabs[3]: # Romato
    secilen.extend(st.multiselect("Romatoloji", ["Kelebek Döküntü", "Raynaud", "Oral Aft", "Genital Ülser", "Göz Kuruluğu", "Sabah Sertliği", "Poliartrit", "Bambu Omurga"]))
with tabs[4]: # Endokrin
    secilen.extend(st.multiselect("Endokrin & Nefro", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Hiperpigmentasyon", "Ekzoftalmi", "Aydede Yüzü", "Mor Stria", "Üremik Koku", "Hematüri"]))
with tabs[5]: # Hemato
    secilen.extend(st.multiselect("Hemato-Onkoloji", ["Solukluk", "Peteşi/Purpura", "Lenfadenopati", "Splenomegali", "Gece Terlemesi", "Kilo Kaybı", "Kemik Ağrısı"]))
with tabs[6]: # Toksikoloji
    secilen.extend(st.multiselect("Acil & Toksikoloji", ["Hipersalivasyon", "Kene Isırması", "Sıcak İntoleransı", "Alkol/Madde Kullanımı", "İlaç Doz Aşımı"]))

# 5. DEV ANALİZ MOTORU (Tanı + Tedavi)
def ultimate_engine_v13(b_list, v):
    tanilar, tetkikler, tedaviler = [], set(["Hemogram", "Geniş Biyokimya", "CRP", "TİT", "EKG"]), []
    b = set(b_list)
    ates, ta_s, spo2, seker, yas = v

    # --- GİS KANAMA VE KARACİĞER ---
    if "Hematemez" in b or "Melena" in b:
        tanilar.append("Üst GİS Kanama (Özofagus Varisi / Peptik Ülser)")
        tetkikler.update(["Acil Endoskopi", "PT/INR", "Kan Grubu & Cross-match", "Laktat"])
        tedaviler.extend(["IV PPI İnfüzyonu", "Somatostatin/Oktreotid (Varis şüphesi)", "IV Kristaloid Replasmanı", "Geniş Lümenli IV Erişim"])
    
    if "Sarılık" in b and "Asteriksis" in b:
        tanilar.append("Hepatik Ensefalopati / Dekompanse Siroz")
        tetkikler.update(["Amonyak", "Batın USG", "Albumin", "Bilirubin Paneli"])
        tedaviler.extend(["Laktüloz Enema/Oral", "Rifaksimin", "Protein Kısıtlı Diyet", "K Vitamini"])

    # --- KARDİYOVASKÜLER ACİLLER ---
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        tanilar.append("Akut Koroner Sendrom (STEMI / NSTEMI)")
        tetkikler.update(["Seri Troponin", "EKO", "Koroner Anjiyo"])
        tedaviler.extend(["Aspirin 300mg", "Klopidogrel/Tikagrelor", "Sublingual Nitrogliserin", "O2 Desteği (Spo2 <94)"])

    if "Bacak Şişliği (Tek)" in b:
        tanilar.append("Derin Ven Trombozu (DVT)")
        tetkikler.update(["D-Dimer", "Alt Ekstremite Venöz Doppler"])
        tedaviler.extend(["Enoksaparin (LMWH)", "Eleve Pozisyon", "Oral Antikoagülan Planı"])

    # --- ENDOKRİN VE METABOLİK ---
    if seker > 250 and "Aseton Kokusu" in b:
        tanilar.append("Diyabetik Ketoasidoz (DKA)")
        tetkikler.update(["Kan Gazı", "İdrar Ketonu", "Osmolalite"])
        tedaviler.extend(["0.9% NaCl İnfüzyonu", "IV İnsülin (0.1 u/kg/saat)", "Potasyum Replasmanı"])

    if "Hiperpigmentasyon" in b and ta_s < 90:
        tanilar.append("Akut Adrenal Yetmezlik (Addison Krizi)")
        tetkikler.update(["Kortizol", "ACTH", "Elektrolitler"])
        tedaviler.extend(["IV Hidrokortizon (100mg)", "Bolus SF"])

    # --- ROMATOLOJİ VE VASKÜLİT ---
    if "Oral Aft" in b and "Genital Ülser" in b:
        tanilar.append("Behçet Hastalığı")
        tetkikler.update(["HLA-B51", "Paterji Testi", "Göz Muayenesi"])
        tedaviler.extend(["Kolşisin", "Sistemik Steroid (Atak durumunda)", "Topikal Ajanlar"])

    # --- HEMATO-ONKOLOJİ ---
    if "B-Semptomları" in b or "Lenfadenopati" in b:
        tanilar.append("Lenfoproliferatif Hastalık (Lenfoma?)")
        tetkikler.update(["Eksizyonel Biyopsi", "LDH", "Toraks/Batın BT"])
        tedaviler.append("Onkoloji/Hematoloji Konsültasyonu")

    # --- GENEL KONTROL (HİÇBİR ŞEY SAPTANMAZSA) ---
    if not tanilar and b:
        tanilar.append("Spesifik Olmayan Klinik Tablo (İleri Tetkik Gerekli)")
        tedaviler.append("Semptomatik Destek Tedavisi ve Yakın Takip")

    return tanilar, sorted(list(tetkikler)), tedaviler

# 6. Analiz Tetikleme
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 ULTIMATE ANALİZİ BAŞLAT"):
    if not secilen and ates == 36.6:
        st.warning("⚠️ Lütfen en az bir belirti giriniz.")
    else:
        v_data = (ates, ta_sis, spo2, kan_sekeri, yas)
        tanilar, tetkikler, tedaviler = ultimate_engine_v13(secilen, v_data)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='diagnose-box'><h3>🚨 OLASI TANILAR</h3>", unsafe_allow_html=True)
            for t in tanilar: st.write(f"🏷️ **{t}**")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='test-box'><h3>🧪 TETKİK PLANI</h3>", unsafe_allow_html=True)
            for tet in tetkikler: st.write(f"🔬 {tet}")
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='treatment-box'><h3>💊 ACİL YAKLAŞIM</h3>", unsafe_allow_html=True)
            for ted in tedaviler: st.write(f"✅ {ted}")
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; opacity: 0.6;'>Dahiliye Pro Max v13.0 | <b>İSMAİL ORHAN</b> | {yas} Yaş Grubu İçin Optimize Edildi.</p>", unsafe_allow_html=True)
