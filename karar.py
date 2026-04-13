import streamlit as st

# 1. Sayfa Ayarları ve Modern Görünüm
st.set_page_config(page_title="Dahiliye Klinik Karar Destek", page_icon="⚕️", layout="wide")

# Modern CSS Tasarımı
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stTabs [data-baseweb="tab"] { 
        font-size: 14px; font-weight: bold; padding: 10px 20px; 
        border-radius: 10px 10px 0 0; background-color: rgba(255,255,255,0.5);
    }
    .stTabs [aria-selected="true"] { background-color: #1e3a8a !important; color: white !important; }
    .diagnose-card {
        background-color: white; padding: 25px; border-radius: 20px;
        border-left: 10px solid #1e3a8a; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .test-card {
        background-color: #ffffff; padding: 25px; border-radius: 20px;
        border-left: 10px solid #10b981; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    h1 { color: #1e3a8a; text-align: center; font-weight: 800; }
    .stButton>button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; border: none; border-radius: 15px; height: 3.5em;
        font-weight: bold; transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(59,130,246,0.4); }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Bilgi
st.title("⚕️ Dahiliye Klinik Karar Destek Sistemi")
st.markdown("<p style='text-align: center;'><b>Sürüm: 6.0 (Tam Kapsamlı & Bağımsız Mod)</b></p>", unsafe_allow_html=True)
st.divider()

# 3. Sidebar: Vital Bulgular ve Hasta Profili
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2773/2773533.png", width=100)
    st.header("📋 Hasta Profili")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    st.divider()
    st.header("🌡️ Vital Bulgular")
    ates = st.slider("Vücut Isısı (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA (mmHg)", 50, 250, 120)
    ta_dia = st.number_input("Diastolik TA (mmHg)", 30, 150, 80)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)
    nabiz = st.number_input("Nabız (atım/dk)", 30, 220, 80)

# 4. Sekmeli Devasa Semptom Paneli
st.subheader("🔍 Klinik Semptom ve Bulguların Seçimi")
tabs = st.tabs(["🩺 GİS", "🫁 Kardiyo-Solunum", "🧠 Nöro-Psikiyatri", "🦋 Romatoloji", "🧪 Endokrin/Nefro/Hemato"])

secilen = []
with tabs[0]:
    col_a, col_b = st.columns(2)
    with col_a:
        secilen.extend(st.multiselect("Üst GİS", ["Hematemez", "Melena", "Disfaji", "Epigastrik Ağrı", "Pirozis", "Erken Doyma"]))
    with col_b:
        secilen.extend(st.multiselect("Alt GİS & Hepatobilier", ["Sağ Alt Kadran Ağrısı", "Hematokezya", "Sarılık", "Asit", "Kupür (Rebound)", "İshal (Kronik)"]))

with tabs[1]:
    col_c, col_d = st.columns(2)
    with col_c:
        secilen.extend(st.multiselect("Kardiyovasküler", ["Baskı Tarzı Göğüs Ağrısı", "Plevritik Ağrı", "Çarpıntı", "Senkop", "Paroksizmal Gece Dispnesi", "Ortopne"]))
    with col_d:
        secilen.extend(st.multiselect("Solunum", ["Hemoptizi", "Efor Dispnesi", "Hırıltılı Solunum", "Gece Öksürüğü", "Plevral Efüzyon Şüphesi"]))

with tabs[2]:
    secilen.extend(st.multiselect("Nörolojik Bulgular", ["Ani Şiddetli Baş Ağrısı", "Konfüzyon/Deliryum", "Fokal Güç Kaybı", "Dizartri", "Ataksi", "Ense Sertliği", "Görsel Kayıp"]))

with tabs[3]:
    secilen.extend(st.multiselect("Romatolojik Bulgular", ["Kelebek Döküntü", "Sabah Sertliği (>1 Saat)", "Eklem Şişliği (Artrit)", "Raynaud Fenomeni", "Göz Kuruluğu", "Aftöz Lezyonlar"]))

with tabs[4]:
    secilen.extend(st.multiselect("Endokrin, Nefro & Hemato", ["Poliüri/Polidipsi", "Hematüri", "Oligüri", "Pretibial Ödem", "Peteşi/Purpura", "Lenfadenopati", "Splenomegali", "Sıcak/Soğuk İntoleransı"]))

# 5. AKILLI KLİNİK MANTIK MOTORU
def klinik_karar_motoru(bulgular, f_ates, f_ta_sis, f_spo2, f_yas):
    t_list = []
    tet_list = {"Hemogram (Tam Kan)", "CRP", "Geniş Biyokimya (AST/ALT/BUN/Cre/Glu/Alb)", "Tam İdrar Tetkiki"}
    b = set(bulgular)

    # GİS Algoritmaları
    if "Hematemez" in b or "Melena" in b:
        t_list.append("Üst GİS Kanama (Peptik Ülser/Varis?)")
        tet_list.update(["Acil Üst GİS Endoskopisi", "INR/PTT", "Kan Grubu & Cross-match", "Hb Takibi"])
    if "Sağ Alt Kadran Ağrısı" in b and "Kupür (Rebound)" in b:
        t_list.append("Akut Apandisit (Cerrahi Batın)")
        tet_list.update(["Batın BT (Kontrastlı)", "WBC Takibi"])
    if "Sarılık" in b and "Asit" in b:
        t_list.append("Dekompanse Karaciğer Sirozu / Akut Hepatit")
        tet_list.update(["Tüm Batın USG", "Hepatit Paneli", "Amonyak", "PT/INR"])

    # Kardiyo-Solunum Algoritmaları
    if "Baskı Tarzı Göğüs Ağrısı" in b:
        t_list.append("Akut Koroner Sendrom (MI Şüphesi)")
        tet_list.update(["12 Derivasyonlu EKG", "Kardiyak Troponin (Seri)", "Ekokardiyografi"])
    if "Efor Dispnesi" in b and f_spo2 < 93:
        t_list.append("KOAH/Astım Atak veya Kalp Yetmezliği")
        tet_list.update(["NT-proBNP", "Akciğer Grafisi", "SFT (Stabilse)", "Arter Kan Gazı"])
    if "Hemoptizi" in b or ("Plevritik Ağrı" in b and f_spo2 < 94):
        t_list.append("Pulmoner Emboli / Akciğer Ca / Pnömoni")
        tet_list.update(["D-Dimer", "Toraks BT Anjiyo", "Balgam Kültürü/Sitolojisi"])

    # Romatoloji
    if "Kelebek Döküntü" in b:
        t_list.append("Sistemik Lupus Eritematozus (SLE)")
        tet_list.update(["ANA Paneli", "Anti-dsDNA", "C3-C4 Kompleman", "Sedimantasyon"])
    if "Sabah Sertliği (>1 Saat)" in b and "Eklem Şişliği (Artrit)" in b:
        t_list.append("Romatoid Artrit")
        tet_list.update(["RF (Romatoid Faktör)", "Anti-CCP", "El-El Bileği Grafisi"])

    # Nöroloji & Diğer
    if "Ense Sertliği" in b and f_ates > 38:
        t_list.append("Akut Bakteriyel Menenjit")
        tet_list.update(["Acil Lomber Ponksiyon", "Beyin BT/MR", "Kan Kültürü"])
    if "Poliüri/Polidipsi" in b:
        t_list.append("Diabetes Mellitus / Diyabetes İnsipitus")
        tet_list.update(["HbA1c", "İdrar Dansitesi", "Serum Osmolalitesi"])
    if f_ta_sis > 180:
        t_list.append("Hipertansif Emergency/Urgency")
        tet_list.update(["Fundoskopik Muayene", "Kreatinin Takibi", "İdrarda Protein"])

    return sorted(t_list), sorted(list(tet_list))

# 6. Analiz ve Sonuç Ekranı
if st.button("KLİNİK ANALİZİ BAŞLAT VE RAPORLA"):
    if not secilen:
        st.error("⚠️ Lütfen analiz için en az bir semptom veya bulgu seçiniz!")
    else:
        on_tanilar, onerilenler = klinik_karar_motoru(secilen, ates, ta_sis, spo2, yas)
        
        st.markdown("### 🏥 Klinik Analiz Raporu")
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown("<div class='diagnose-card'>", unsafe_allow_html=True)
            st.subheader("📋 Diferansiyel Tanılar")
            if on_tanilar:
                for t in on_tanilar:
                    st.write(f"✅ **{t}**")
            else:
                st.info("Bulgular spesifik bir dahili tanıya odaklanamadı. İleri muayene gereklidir.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with res_col2:
            st.markdown("<div class='test-card'>", unsafe_allow_html=True)
            st.subheader("🧪 İstenmesi Gereken Tetkikler")
            for tet in onerilenler:
                st.write(f"💉 {tet}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.success("Analiz başarıyla tamamlandı. Veriler yerel tıbbi veritabanı üzerinden işlendi.")

# 7. Alt Bilgi
st.markdown("---")
st.caption("Bu uygulama İsmail Orhan tarafından Dahiliye Klinik Karar Destek süreçleri için geliştirilmiştir. © 2026")
