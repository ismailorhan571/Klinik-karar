import streamlit as st

# 1. Sayfa Ayarları ve Ultra Modern Görünüm
st.set_page_config(page_title="Dahiliye CDSS", page_icon="⚕️", layout="wide")

# Modern ve Profesyonel CSS
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); }
    .stTabs [data-baseweb="tab"] { 
        font-size: 15px; font-weight: bold; padding: 12px; 
        border-radius: 10px 10px 0 0;
    }
    .stTabs [aria-selected="true"] { background-color: #003366 !important; color: white !important; }
    .diagnose-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 8px solid #003366; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .test-card {
        background-color: #ffffff; padding: 20px; border-radius: 15px;
        border-left: 8px solid #28a745; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    h1 { color: #003366; text-align: center; font-weight: 900; letter-spacing: -1px; }
    .stButton>button {
        background: linear-gradient(90deg, #003366 0%, #00509d 100%);
        color: white; border: none; border-radius: 12px; height: 3.5em;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { box-shadow: 0 8px 20px rgba(0,51,102,0.3); transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Dahiliye Klinik Karar Destek Sistemi")
st.markdown("<p style='text-align: center; font-size: 1.2em;'><b>Sürüm: 7.0 (Geliştirici: İSMAİL ORHAN)</b></p>", unsafe_allow_html=True)
st.divider()

# 3. Sidebar: Genişletilmiş Vital Bulgular (ŞEKER EKLENDİ)
with st.sidebar:
    st.header("📋 Hasta Profili & Vitaller")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    st.divider()
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    nabiz = st.number_input("Nabız (atım/dk)", 30, 220, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)
    # Diyabet Takibi İçin Şeker Parametresi
    kan_sekeri = st.number_input("Açlık/Anlık Kan Şekeri (mg/dL)", 30, 800, 100)
    if kan_sekeri > 200:
        st.warning("⚠️ Hiperglisemi Saptandı!")
    elif kan_sekeri < 70:
        st.error("🚨 Hipoglisemi Riski!")

# 4. Sekmeli Devasa Semptom Paneli
st.subheader("🔍 Klinik Semptom ve Bulgular")
t_gis, t_kardiyo, t_noroloji, t_romatoloji, t_endokrin, t_enfeksiyon = st.tabs([
    "🩺 GİS", "🫁 Kardiyo-Solunum", "🧠 Nörolojik", "🦋 Romatoloji", "🧪 Endokrin/Nefro", "🧬 Enfeksiyon/Genel"
])

secilen = []
with t_gis:
    c1, c2 = st.columns(2)
    with c1:
        secilen.extend(st.multiselect("Üst GİS", ["Hematemez", "Melena", "Disfaji", "Epigastrik Ağrı", "Pirozis", "Hematokezya"]))
    with c2:
        secilen.extend(st.multiselect("Alt GİS & Hepatobilier", ["Sağ Alt Kadran Ağrısı", "Sarılık", "Asit", "Kupür/Rebound", "İshal", "Kabızlık (Yeni Başlangıç)"]))

with t_kardiyo:
    c3, c4 = st.columns(2)
    with c3:
        secilen.extend(st.multiselect("Kardiyovasküler", ["Baskı Tarzı Göğüs Ağrısı", "Çarpıntı", "Senkop", "Ortopne", "PND (Gece Gelen Nefes Darlığı)"]))
    with c4:
        secilen.extend(st.multiselect("Solunum", ["Hemoptizi", "Efor Dispnesi", "Hırıltılı Solunum", "Plevritik Ağrı", "Öksürük (Prodüktif)"]))

with t_noroloji:
    secilen.extend(st.multiselect("Nörolojik Bulgular", ["Ani/Şiddetli Baş Ağrısı", "Konfüzyon", "Fokal Güç Kaybı", "Dizartri", "Ense Sertliği", "Ataksi", "Vertigo"]))

with t_romatoloji:
    secilen.extend(st.multiselect("Romatolojik Bulgular", ["Kelebek Döküntü", "Sabah Sertliği (>1 Saat)", "Eklem Şişliği", "Raynaud Fenomeni", "Aftöz Lezyonlar", "Göz/Ağız Kuruluğu"]))

with t_endokrin:
    secilen.extend(st.multiselect("Endokrin & Nefroloji", ["Poliüri/Polidipsi", "Hematüri", "Oligüri", "Pretibial Ödem", "Sıcak/Soğuk İntoleransı", "Aseton Kokusu"]))

with t_enfeksiyon:
    secilen.extend(st.multiselect("Genel & Enfeksiyon", ["Gece Terlemesi", "İstemsiz Kilo Kaybı", "Lenfadenopati", "Splenomegali", "Peteşi/Purpura", "Halsizlik/Anemi"]))

# 5. ULTRA ZENGİN TANI VE TETKİK MOTORU (Offline)
def uzman_karar_motoru(bulgular, f_ates, f_ta_sis, f_spo2, f_seker):
    t_list = []
    tet_list = {"Hemogram", "CRP", "AST/ALT/BUN/Cre/Glu", "Tam İdrar Tetkiki", "Sedimantasyon"}
    b = set(bulgular)

    # Diyabet Algoritması
    if f_seker > 126 or "Poliüri/Polidipsi" in b:
        t_list.append("Diabetes Mellitus (DM)")
        tet_list.update(["HbA1c", "İdrarda Mikroalbümin", "C-Peptid"])
    if f_seker > 250 and "Aseton Kokusu" in b:
        t_list.append("Diyabetik Ketoasidoz (DKA)")
        tet_list.update(["Venöz Kan Gazı", "İdrarda Keton", "Serum Elektrolitleri"])

    # GİS ve Akut Batın
    if "Hematemez" in b or "Melena" in b:
        t_list.append("Üst GİS Kanama")
        tet_list.update(["Acil Endoskopi", "Kan Grubu/Cross", "INR/PTT"])
    if "Sağ Alt Kadran Ağrısı" in b:
        t_list.append("Akut Apandisit")
        tet_list.update(["Batın BT", "Tüm Batın USG"])
    if "Sarılık" in b:
        t_list.append("Hepatit / Bilier Obstrüksiyon")
        tet_list.update(["Hepatit Paneli", "Bilirubin (Direkt/İndirekt)", "MRCP/USG"])

    # Kardiyo-Solunum
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        t_list.append("Akut Koroner Sendrom")
        tet_list.update(["EKG", "Kardiyak Troponin", "EKO"])
    if f_spo2 < 92 or "Hemoptizi" in b:
        t_list.append("Pulmoner Emboli / Akciğer Ca")
        tet_list.update(["D-Dimer", "Toraks BT Anjiyo", "PAAC Grafisi"])

    # Romatoloji
    if "Kelebek Döküntü" in b:
        t_list.append("Sistemik Lupus (SLE)")
        tet_list.update(["ANA Paneli", "Anti-dsDNA", "C3-C4 Kompleman"])
    if "Sabah Sertliği (>1 Saat)" in b:
        t_list.append("Romatoid Artrit")
        tet_list.update(["RF", "Anti-CCP", "El/El Bileği Grafisi"])

    # Enfeksiyon/Hematoloji
    if "Gece Terlemesi" in b and "Kilo Kaybı" in b:
        t_list.append("Lenfoma / Tüberküloz Şüphesi")
        tet_list.update(["LDH", "Periferik Yayma", "Toraks BT", "PPD/Quantiferon"])
    if f_ates > 38 and "Ense Sertliği" in b:
        t_list.append("Menenjit")
        tet_list.update(["Beyin BT", "Lomber Ponksiyon (BOS İnceleme)"])

    return sorted(t_list), sorted(list(tet_list))

# 6. Analiz ve Sonuç Ekranı
if st.button("ANALİZİ BAŞLAT VE RAPOR OLUŞTUR"):
    if not secilen and kan_sekeri == 100 and ates == 36.6:
        st.warning("⚠️ Lütfen belirti seçiniz veya vitalleri güncelleyiniz.")
    else:
        on_tanilar, onerilenler = uzman_karar_motoru(secilen, ates, ta_sis, spo2, kan_sekeri)
        
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.markdown("<div class='diagnose-card'>", unsafe_allow_html=True)
            st.subheader("📋 Olası Ön Tanılar")
            if on_tanilar:
                for t in on_tanilar: st.write(f"✅ **{t}**")
            else: st.info("Spesifik bir tanıya odaklanılamadı. Klinik takip önerilir.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_res2:
            st.markdown("<div class='test-card'>", unsafe_allow_html=True)
            st.subheader("🧪 Planlanan Tetkikler")
            for tet in onerilenler: st.write(f"💉 {tet}")
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Alt Bilgi
st.markdown("---")
st.caption("Dahiliye Klinik Karar Destek Sistemi © 2026 | Tasarım ve Geliştirme: İSMAİL ORHAN")
