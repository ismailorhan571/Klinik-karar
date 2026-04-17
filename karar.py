import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API YAPILANDIRMASI (Senin belirttiğin gibi GEMINI_API_KEY olarak güncellendi)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"API Anahtarı Hatası: {e}. Lütfen Secrets kısmında 'GEMINI_API_KEY' ismini kontrol edin.")

# 2. SAYFA AYARLARI
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE", layout="wide")
st.title("💊 DAHİLİYE KLİNİK KARAR DESTEK SİSTEMİ")
st.markdown("<p style='text-align: center; color: gray;'>Geliştirici: Hemşire İsmail Orhan</p>", unsafe_allow_html=True)

# 3. YAN PANEL: LABORATUVAR, GKS VE WELLS
with st.sidebar:
    st.header("🧪 HASTA VERİ GİRİŞİ")
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    kilo = st.number_input("Kilo (kg)", 10, 250, 80)
    
    st.divider()
    st.subheader("🩸 KAN VE ŞEKER")
    seker = st.number_input("AKŞ (mg/dL)", 0, 1000, 100)
    hba1c = st.number_input("HbA1c (%)", 0.0, 20.0, 5.7)
    kre = st.number_input("Kreatinin (mg/dL)", 0.1, 20.0, 1.0)
    hb = st.number_input("Hemoglobin (Hb)", 0.0, 25.0, 14.0)
    wbc = st.number_input("WBC (Lökosit)", 0, 100000, 8000)
    plt = st.number_input("PLT (Trombosit)", 0, 2000000, 250000)
    
    # Otomatik eGFR Hesaplama
    egfr = round(((140 - yas) * kilo) / (72 * kre) * (0.85 if cinsiyet == "Kadın" else 1), 1)
    st.metric("eGFR Skoru", f"{egfr} ml/dk")

    st.divider()
    # GKS DEĞERLENDİRMELİ GİRİŞ
    st.subheader("🧠 GKS DEĞERLENDİRMESİ")
    e = st.selectbox("Göz (E)", [4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Ağrıyla','Sesle','Spontan'][x-1]}")
    v = st.selectbox("Sözel (V)", [5, 4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Anlamsız Ses','Uygunsuz Kelime','Konfüze','Oryante'][x-1]}")
    m = st.selectbox("Motor (M)", [6, 5, 4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Ekstansiyon','Fleksiyon','Ağrıdan Kaçar','Ağrıyı Lokalize','Emre Uyar'][x-1]}")
    
    gcs_toplam = e + v + m
    if gcs_toplam <= 8: g_durum = "🔴 Ağır Koma"
    elif gcs_toplam <= 12: g_durum = "🟡 Orta Koma"
    elif gcs_toplam <= 14: g_durum = "🟢 Hafif Koma"
    else: g_durum = "✅ Bilinç Açık"
    st.info(f"Sonuç: {gcs_toplam} - {g_durum}")

    st.divider()
    # WELLS SKORLAMASI
    st.subheader("📊 WELLS SKORU")
    w_list = [
        st.checkbox("Aktif Kanser (+1)"),
        st.checkbox("Paralizi / İmmobilizasyon (+1)"),
        st.checkbox("Yatak Bağımlılığı >3 Gün (+1)"),
        st.checkbox("Venöz Hassasiyet (+1)"),
        st.checkbox("Tüm Bacakta Şişlik (+1)"),
        st.checkbox("Baldır Şişliği >3cm (+1)"),
        st.checkbox("Gode Bırakan Ödem (+1)"),
        st.checkbox("Kollateral Venler (+1)"),
        st.checkbox("Alternatif Tanı Olasılığı (-2)")
    ]
    wells_score = sum(w_list[:-1]) + (-2 if w_list[-1] else 0)
    st.warning(f"Wells Skoru: {wells_score}")

# 4. ANA EKRAN VE GÖRÜNTÜ YÜKLEME
st.subheader("🔍 Klinik Bulgular ve AI Analizi")
bulgular = st.multiselect("Semptomları Seçin", 
    ["Göğüs Ağrısı", "Nefes Darlığı", "Karın Ağrısı", "Ateş (>38)", "Sarılık", "Kuşak Ağrısı", "Konfüzyon", "Hemoptizi", "Hematemez", "Melena", "Bilateral Ödem", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Boyun Ven Dolgunluğu", "Asit", "Kilo Kaybı", "Gece Terlemesi", "Eklem Ağrısı", "Pitozis", "Parezi", "Nöbet", "Ense Sertliği"])

uploaded_file = st.file_uploader("📸 EKG veya Radyolojik Görüntü Yükle", type=["jpg", "jpeg", "png"])

# 5. MASTER VERİTABANI (85 HASTALIK - EKSİKSİZ)
master_db = {
    "STEMI": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Terleme"], "t": "EKG + Troponin", "ted": "Anjiyo"},
    "NSTEMI": {"b": ["Göğüs Ağrısı", "Bulantı"], "t": "Seri Troponin", "ted": "Antikoagülan"},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Hemoptizi", "Taşikardi"], "t": "BT Anjiyo", "ted": "Heparin"},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Hipotansiyon"], "t": "BT Anjiyo", "ted": "Cerrahi"},
    "Akut Kalp Yetersizliği": {"b": ["Nefes Darlığı", "Boyun Ven Dolgunluğu", "Ödem"], "t": "proBNP + EKO", "ted": "Furosemid"},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm"], "t": "Kan Kültürü", "ted": "Antibiyotik"},
    "Perikard Tamponadı": {"b": ["Hipotansiyon", "Boyun Ven Dolgunluğu"], "t": "EKO", "ted": "Perikardiyosentez"},
    "Atriyal Fibrilasyon": {"b": ["Çarpıntı", "Taşikardi"], "t": "EKG", "ted": "Hız Kontrolü"},
    "Miyokardit": {"b": ["Göğüs Ağrısı", "Ateş (>38)"], "t": "Troponin + MR", "ted": "İstirahat"},
    "Stabil Anjina": {"b": ["Göğüs Ağrısı"], "t": "Efor Testi", "ted": "Aspirin"},
    "Kardiyojenik Şok": {"b": ["Hipotansiyon", "Konfüzyon"], "t": "Laktat", "ted": "İnotrop"},
    "Hipertansif Kriz": {"b": ["Baş Ağrısı", "Konfüzyon"], "t": "Tansiyon Takibi", "ted": "IV Antihipertansif"},
    "Aort Stenozu": {"b": ["Senkop", "Üfürüm"], "t": "EKO", "ted": "Kapak Replasmanı"},
    "Mitral Yetersizlik": {"b": ["Nefes Darlığı", "Üfürüm"], "t": "EKO", "ted": "Diüretik"},
    "Tam Blok": {"b": ["Bradikardi", "Senkop"], "t": "EKG", "ted": "Pacemaker"},
    "Varis Kanaması": {"b": ["Hematemez", "Sarılık"], "t": "Endoskopi", "ted": "Band Ligasyonu"},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Bulantı"], "t": "Lipaz/Amilaz", "ted": "Sıvı Tedavisi"},
    "Hepatik Ensefalopati": {"b": ["Konfüzyon", "Asteriksis"], "t": "Amonyak", "ted": "Laktüloz"},
    "Akut Kolanjit": {"b": ["Sarılık", "Ateş (>38)", "Karın Ağrısı"], "t": "ERCP", "ted": "Antibiyotik + ERCP"},
    "Peptik Ülser": {"b": ["Karın Ağrısı", "Melena"], "t": "Endoskopi", "ted": "PPI"},
    "Crohn Hastalığı": {"b": ["Karın Ağrısı", "İshal", "Kilo Kaybı"], "t": "Kolonoskopi", "ted": "Steroid"},
    "Ülseratif Kolit": {"b": ["Hematokezya", "İshal"], "t": "Kolonoskopi", "ted": "Mesalazin"},
    "Wilson Hastalığı": {"b": ["Tremor", "Sarılık"], "t": "Seruloplazmin", "ted": "Penisilamin"},
    "Siroz": {"b": ["Asit", "Sarılık", "Hepatomegali"], "t": "Albumin/INR", "ted": "Diüretik"},
    "AKY (Karaciğer)": {"b": ["Sarılık", "Konfüzyon"], "t": "INR", "ted": "Nakil"},
    "Çölyak": {"b": ["İshal", "Kilo Kaybı"], "t": "tTG-IgA", "ted": "Glutensiz Diyet"},
    "Akalazya": {"b": ["Disfaji", "Regürjitasyon"], "t": "Manometri", "ted": "Dilatasyon"},
    "Gastroparezi": {"b": ["Mide Bulantısı", "Erken Doyma"], "t": "Sintigrafi", "ted": "Metoklopramid"},
    "Hepatit B": {"b": ["Sarılık", "Bulantı"], "t": "HBsAg", "ted": "Destek"},
    "Hepatit C": {"b": ["Halsizlik", "KC Hasarı"], "t": "HCV-RNA", "ted": "Antiviral"},
    "Otoimmün Hepatit": {"b": ["Sarılık", "Eklem Ağrısı"], "t": "ANA/ASMA", "ted": "Steroid"},
    "PBC": {"b": ["Kaşıntı", "Sarılık"], "t": "AMA", "ted": "UDCA"},
    "Pankreas Kanseri": {"b": ["Sarılık", "Kilo Kaybı"], "t": "BT + CA 19-9", "ted": "Whipple"},
    "Mezenter İskemi": {"b": ["Şiddetli Karın Ağrısı"], "t": "BT Anjiyo", "ted": "Cerrahi"},
    "Divertikülit": {"b": ["Karın Ağrısı", "Ateş (>38)"], "t": "BT", "ted": "Antibiyotik"},
    "DKA": {"b": ["Konfüzyon", "Aseton Kokusu"], "t": "Kan Gazı", "ted": "İnsülin"},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi"], "t": "TSH", "ted": "PTU + Beta Bloker"},
    "Addison Krizi": {"b": ["Hipotansiyon", "Hiperpigmentasyon"], "t": "Kortizol", "ted": "Hidrokortizon"},
    "Miksödem Koması": {"b": ["Bradikardi", "Konfüzyon"], "t": "fT4", "ted": "L-Tiroksin"},
    "Feokromositoma": {"b": ["Baş Ağrısı", "Terleme"], "t": "Metanefrin", "ted": "Alfa Bloker"},
    "Cushing": {"b": ["Mor Stria", "Aydede Yüzü"], "t": "DEX Testi", "ted": "Cerrahi"},
    "Diabetes Insipidus": {"b": ["Poliüri", "Polidipsi"], "t": "Susuzluk Testi", "ted": "Desmopressin"},
    "Hiperkalsemi": {"b": ["Konfüzyon", "Poliüri"], "t": "Ca + PTH", "ted": "Hidrasyon"},
    "Akromegali": {"b": ["El-Ayak Büyümesi"], "t": "IGF-1", "ted": "Cerrahi"},
    "Hipoglisemi": {"b": ["Terleme", "Konfüzyon"], "t": "Kan Şekeri", "ted": "Dekstroz"},
    "Hiperaldosteronizm": {"b": ["Hipotansiyon", "Kas Güçsüzlüğü"], "t": "Renin/Aldo", "ted": "Spironolakton"},
    "Hipoparatiroidi": {"b": ["Kas Spazmı", "Parezi"], "t": "Ca + PTH", "ted": "Kalsiyum"},
    "Prolaktinoma": {"b": ["Galaktore", "Baş Ağrısı"], "t": "Prolaktin", "ted": "Kabergolin"},
    "SIADH": {"b": ["Hiponatremi", "Konfüzyon"], "t": "İdrar Sodyumu", "ted": "Sıvı Kısıtlaması"},
    "Hashimoto": {"b": ["Soğuk İntoleransı", "Halsizlik"], "t": "Anti-TPO", "ted": "Levotiroksin"},
    "TTP": {"b": ["Konfüzyon", "Peteşi"], "t": "ADAMTS13", "ted": "Plazmaferez"},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Anemi"], "t": "M-Spike", "ted": "KT"},
    "AML": {"b": ["Anemi", "Kanama"], "t": "KİB", "ted": "Kemoterapi"},
    "Lenfoma": {"b": ["Lenfadenopati", "Gece Terlemesi"], "t": "Biyopsi", "ted": "Kemoterapi"},
    "PNH": {"b": ["Hemoptizi", "Anemi"], "t": "Akım Sitometrisi", "ted": "Eculizumab"},
    "DIC": {"b": ["Kanama", "Peteşi"], "t": "D-Dimer/Fibrinojen", "ted": "TDP"},
    "Polisitemia Vera": {"b": ["Kaşıntı", "Baş Ağrısı"], "t": "JAK2", "ted": "Flebotomi"},
    "İTP": {"b": ["Peteşi", "Diş Eti Kanaması"], "t": "Trombosit düşüklüğü", "ted": "Steroid"},
    "Aplastik Anemi": {"b": ["Anemi", "Halsizlik"], "t": "KİB", "ted": "Nakil"},
    "B12 Eksikliği": {"b": ["Ataksi", "Anemi"], "t": "B12 Düzeyi", "ted": "B12 Enjeksiyon"},
    "Hemofili": {"b": ["Eklem Kanaması"], "t": "Faktör Düzeyi", "ted": "Faktör Replasmanı"},
    "vWF Hastalığı": {"b": ["Burun Kanaması"], "t": "vWF Aktivitesi", "ted": "Desmopressin"},
    "MDS": {"b": ["Anemi", "Halsizlik"], "t": "KİB", "ted": "Destek"},
    "Esansiyel Trombositemi": {"b": ["Trombositoz", "Baş Ağrısı"], "t": "JAK2", "ted": "Aspirin"},
    "Miyelofibrozis": {"b": ["Splenomegali", "Anemi"], "t": "KİB", "ted": "Ruxolitinib"},
    "SLE": {"b": ["Kelebek Döküntü", "Eklem Ağrısı"], "t": "ANA + dsDNA", "ted": "Steroid"},
    "Behçet": {"b": ["Ağızda Aft", "Uveit"], "t": "Paterji", "ted": "Kolşisin"},
    "Ankilozan Spondilit": {"b": ["Bel Ağrısı", "Sabah Sertliği"], "t": "HLA-B27", "ted": "Anti-TNF"},
    "GPA": {"b": ["Hemoptizi", "Burun Kanaması"], "t": "c-ANCA", "ted": "Rituksimab"},
    "Sjögren": {"b": ["Ağız Kuruluğu", "Göz Kuruluğu"], "t": "Anti-SSA/SSB", "ted": "Suni Gözyaşı"},
    "Skleroderma": {"b": ["Deri Sertleşmesi", "Raynaud"], "t": "Anti-Scl70", "ted": "MMF"},
    "Dermatomiyozit": {"b": ["Parezi", "Döküntü"], "t": "Kas Biyopsisi", "ted": "Steroid"},
    "Gut": {"b": ["Eklem Ağrısı", "Ateş (>38)"], "t": "Ürik Asit", "ted": "Kolşisin"},
    "Romatoid Artrit": {"b": ["Eklem Ağrısı", "Sabah Sertliği"], "t": "RF + CCP", "ted": "Metotreksat"},
    "Septik Şok": {"b": ["Hipotansiyon", "Ateş (>38)"], "t": "Laktat", "ted": "Antibiyotik + Sıvı"},
    "Bakteriyel Menenjit": {"b": ["Ense Sertliği", "Ateş (>38)"], "t": "LP", "ted": "Seftriakson"},
    "Goodpasture": {"b": ["Hemoptizi", "Böbrek Hasarı"], "t": "Anti-GBM", "ted": "Plazmaferez"},
    "Miyastenia Gravis": {"b": ["Parezi", "Pitozis"], "t": "Anti-AChR", "ted": "Piridostigmin"},
    "Bruselloz": {"b": ["Terleme", "Ateş (>38)"], "t": "Wright Testi", "ted": "Doksisiklin"},
    "Sıtma": {"b": ["Ateş (>38)", "Sarılık"], "t": "Kalın Damla", "ted": "Artemisin"},
    "KBY (Son Evre)": {"b": ["Ödem", "Böbrek Hasarı"], "t": "eGFR < 15", "ted": "Diyaliz"},
    "Nefrotik Sendrom": {"b": ["Bilateral Ödem"], "t": "Proteinüri", "ted": "Steroid"},
    "Piyelonefrit": {"b": ["Karın Ağrısı", "Ateş (>38)"], "t": "İdrar Kültürü", "ted": "Antibiyotik"},
    "İnterstisyel Akciğer": {"b": ["Nefes Darlığı", "Kuru Öksürük"], "t": "HRCT", "ted": "Steroid"},
    "Sarkoidoz": {"b": ["Lenfadenopati", "Kuru Öksürük"], "t": "ACE", "ted": "Steroid"},
}

# 6. ANALİZ VE AI BAĞLANTISI
if st.button("🚀 KAPSAMLI ANALİZİ BAŞLAT"):
    if not bulgular:
        st.warning("Teşhis için en az bir semptom seçmelisiniz!")
    else:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.subheader("🏥 Klinik Teşhis Öngörüleri")
            sonuclar = []
            for ad, veri in master_db.items():
                eslesme = set(bulgular).intersection(set(veri["b"]))
                if eslesme:
                    puan = round((len(eslesme) / len(veri["b"])) * 100, 1)
                    sonuclar.append({"ad": ad, "puan": puan, "veri": veri})
            
            sonuclar = sorted(sonuclar, key=lambda x: x['puan'], reverse=True)
            for s in sonuclar[:10]:
                st.success(f"**{s['ad']} (%{s['puan']})**\n\nTetkik: {s['veri']['t']}\n\nTedavi: {s['veri']['ted']}")

        with col2:
            st.subheader("🤖 AI Derin Analiz (Gemini)")
            try:
                # API MODEL SEÇİMİ
                model = genai.GenerativeModel('gemini-1.5-flash')
                vaka_metni = f"""
                Dahiliye Uzmanı Asistanı Analizi:
                Hasta: {yas} yaşında {cinsiyet}.
                Vital/Skor: GCS {gcs_toplam} ({g_durum}), Wells {wells_score}.
                Laboratuvar: AKŞ {seker}, HbA1c {hba1c}, Hb {hb}, Kreatinin {kre}, Lökosit {wbc}, Trombosit {plt}.
                Semptomlar: {', '.join(bulgular)}.
                Lütfen klinik bir tablo çiz ve varsa yüklenen görüntüyü yorumla.
                """
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([vaka_metni, img])
                else:
                    response = model.generate_content(vaka_metni)
                st.info(response.text)
            except Exception as e:
                st.error(f"AI Analiz Hatası: {e}")

st.divider()
st.caption("İSMAİL ORHAN DAHİLİYE PROJESİ | 2026")
