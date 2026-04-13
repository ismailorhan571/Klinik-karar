import streamlit as st

# 1. Sayfa Ayarları
st.set_page_config(page_title="Dahiliye CDSS", page_icon="⚕️", layout="wide")

# 2. Görsel Tasarım (v3.7 Profesyonel Tema)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a73e8; color: white; font-weight: bold; border-radius: 10px; height: 3em; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    .result-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-top: 5px solid #1a73e8; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .diagnostic-label { color: #1a73e8; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Başlık
st.title("⚕️ Dahiliye Klinik Karar Destek Sistemi")
st.markdown("**Sürüm:** 5.0 (Ultra Zengin Veri Seti - Çevrimdışı Mod)")
st.divider()

# 4. Sidebar: Vital Bulgular
with st.sidebar:
    st.header("📋 Hasta Parametreleri")
    yas = st.number_input("Yaş", 0, 120, 45)
    ates = st.slider("Ateş (°C)", 34.0, 42.0, 36.6, 0.1)
    ta_sis = st.number_input("Sistolik TA", 50, 250, 120)
    spo2 = st.slider("SpO2 (%)", 50, 100, 98)

# 5. Ultra Zengin Semptom Paneli (Sekmeli)
st.subheader("🔍 Detaylı Semptom Seçimi")
t1, t2, t3, t4, t5 = st.tabs(["🩺 GİS & Karın", "🫁 Göğüs & Solunum", "🧠 Nöro & Psikiyatri", "🦋 Romato & Hematoloji", "🧪 Endokrin & Nefroloji"])

secilen = []
with t1:
    secilen.extend(st.multiselect("Gastrointestinal", ["Sağ Alt Kadran Ağrısı", "Epigastrik Ağrı", "Melena", "Hematemez", "Sarılık", "Asit", "Disfaji", "Kusma"]))
with t2:
    secilen.extend(st.multiselect("Kardiyo-Solunum", ["Baskı Tarzı Göğüs Ağrısı", "Eforla Gelen Nefes Darlığı", "Plevritik Ağrı", "Hemoptizi", "Ortopne", "Paroksizmal Gece Dispnesi"]))
with t3:
    secilen.extend(st.multiselect("Nörolojik", ["Şiddetli Ani Baş Ağrısı", "Konfüzyon", "Fokal Güç Kaybı", "Ense Sertliği", "Ataksi", "Dizartri"]))
with t4:
    secilen.extend(st.multiselect("Romatoloji/Hemato", ["Kelebek Döküntü", "Sabah Sertliği (>30 dk)", "Eklem Şişliği", "Peteşi/Purpura", "Lenfadenopati", "Splenomegali"]))
with t5:
    secilen.extend(st.multiselect("Üriner & Endokrin", ["Poliüri/Polidipsi", "Dizüri", "Oligüri", "Hematüri", "Ekzoftalmi", "Pretibial Miksödem"]))

# 6. DEVASA TANI VE TETKİK MOTORU (Sana ihtiyaç bırakmayacak mantık)
def uzman_analiz(s_list, f_ates, f_spo2, f_ta):
    t_set = set()
    tet_set = {"Hemogram", "Biyokimya Paneli (AST/ALT/BUN/Cre)", "CRP"} # Rutinler
    ss = set(s_list)

    # Akut Batın & GİS
    if "Sağ Alt Kadran Ağrısı" in ss:
        t_set.add("Akut Apandisit")
        tet_set.update(["Batın BT", "Eksploratif Laparoskopi Düşün"])
    if "Melena" in ss or "Hematemez" in ss:
        t_set.add("GİS Kanama (Üst)")
        tet_set.update(["Acil Endoskopi", "Hb Takibi", "INR/PTT"])
    
    # Kardiyoloji & Pulmonoloji
    if "Baskı Tarzı Göğüs Ağrısı" in ss:
        t_set.add("Akut Koroner Sendrom")
        tet_set.update(["EKG", "Troponin I/T (Seri)", "EKO"])
    if f_spo2 < 92 or "Hemoptizi" in ss:
        t_set.add("Pulmoner Emboli / Pnömoni")
        tet_set.update(["D-Dimer", "Toraks BT Anjiyo", "Akciğer Grafisi"])

    # Romatoloji
    if "Kelebek Döküntü" in ss:
        t_set.add("Sistemik Lupus Eritematozus (SLE)")
        tet_set.update(["ANA", "Anti-dsDNA", "C3-C4 Kompleman"])
    if "Sabah Sertliği (>30 dk)" in ss:
        t_set.add("Romatoid Artrit")
        tet_set.update(["RF", "Anti-CCP", "Sedimantasyon"])

    # Nöroloji
    if "Ense Sertliği" in ss and f_ates > 38:
        t_set.add("Menenjit")
        tet_set.update(["LP (Beyin Omurilik Sıvısı)", "Kranial MR", "Kan Kültürü"])

    return sorted(list(t_set)), sorted(list(tet_set))

# 7. Sonuçların Gösterilmesi
if st.button("KLİNİK ANALİZİ TAMAMLA"):
    if not secilen:
        st.warning("Analiz için lütfen en az bir belirti seçiniz.")
    else:
        tanilar, tetkikler = uzman_analiz(secilen, ates, spo2, ta_sis)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.subheader("📋 Olası Diferansiyel Tanılar")
            if tanilar:
                for t in tanilar:
                    st.write(f"🔹 **{t}**")
            else:
                st.write("Belirgin bir spesifik tanı saptanamadı. Genel dahili muayene önerilir.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.subheader("🧪 İstenmesi Gereken Tetkikler")
            for tet in tetkikler:
                st.write(f"• {tet}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.divider()
        st.info("💡 Not: Bu sistem statik tıbbi algoritmalara dayanır. Klinik karar her zaman hekime aittir.")
