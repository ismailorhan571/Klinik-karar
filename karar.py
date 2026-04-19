import streamlit as st
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io
from gtts import gTTS

# --- 1. PREMIUM UI ARCHITECTURE ---
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE ROBOTU", page_icon="💊", layout="wide")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Secrets'da 'GEMINI_API_KEY' bulunamadı!")

# Tek seferde model oluştur ve cache'le (kota dostu)
@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-2.5-flash-lite')

model = get_model()

# Session State
if 'ai_klinik_yorum' not in st.session_state: st.session_state.ai_klinik_yorum = None
if 'top_tani_seslendirildi' not in st.session_state: st.session_state.top_tani_seslendirildi = False
if 'voice_symptoms' not in st.session_state: st.session_state.voice_symptoms = []
if 'selected_symptoms' not in st.session_state: st.session_state.selected_symptoms = []
if 'ses_protokol' not in st.session_state: st.session_state.ses_protokol = "İSMAİL ORHAN"
if 'ses_cinsiyet' not in st.session_state: st.session_state.ses_cinsiyet = "Erkek"
if 'ses_yas' not in st.session_state: st.session_state.ses_yas = 45
if 'ses_kilo' not in st.session_state: st.session_state.ses_kilo = 85
if 'ses_hb' not in st.session_state: st.session_state.ses_hb = 14.0
if 'ses_wbc' not in st.session_state: st.session_state.ses_wbc = 8500
if 'ses_plt' not in st.session_state: st.session_state.ses_plt = 245000
if 'ses_kre' not in st.session_state: st.session_state.ses_kre = 1.1
if 'ses_glu' not in st.session_state: st.session_state.ses_glu = 105

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    .main-header { background: rgba(255,255,255,0.98); padding: 40px; border-radius: 50px; text-align: center; margin-bottom: 40px;
        border-top: 20px solid #DC2626; border-bottom: 20px solid #DC2626; border-left: 12px solid #D4AF37; border-right: 12px solid #D4AF37;
        box-shadow: 0 60px 120px rgba(0,0,0,0.3); }
    .main-header h1 { color: #000; font-weight: 800; font-size: 3.2rem; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 5px; margin-top: 15px; }
    .clinical-card { background: #FFFFFF; padding: 50px; border-radius: 60px; margin-bottom: 40px;
        border-left: 35px solid #DC2626; border-right: 18px solid #D4AF37; box-shadow: 25px 25px 60px rgba(0,0,0,0.12); }
    .stButton>button { background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 50px;
        height: 7em; width: 100%; font-weight: 800; font-size: 35px; border: 7px solid #DC2626; }
    .stButton>button:hover { background: #DC2626; transform: scale(1.01); color: white; }
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 15px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN </p></div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR VERİ MERKEZİ")
    p_no = st.text_input("Ad Soyad", value=st.session_state.ses_protokol)
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"], index=0 if st.session_state.ses_cinsiyet == "Erkek" else 1)
    yas = st.number_input("Yaş", 0, 120, value=st.session_state.ses_yas)
    kilo = st.number_input("Kilo (kg)", 5, 250, value=st.session_state.ses_kilo)
    st.divider()
    
    st.subheader("🧠 GKS DEĞERLENDİRMESİ")
    g_e = st.selectbox("Göz (E)", [4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Ağrıyla','Sesle','Spontan'][x-1]}")
    g_v = st.selectbox("Sözel (V)", [5, 4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Anlamsız Ses','Uygunsuz Kelime','Konfüze','Oryante'][x-1]}")
    g_m = st.selectbox("Motor (M)", [6, 5, 4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Ekstansiyon','Fleksiyon','Ağrıdan Kaçar','Ağrıyı Lokalize','Emre Uyar'][x-1]}")
    gcs_skor = g_e + g_v + g_m
    st.info(f"Toplam GCS: {gcs_skor}")

    st.divider()
    st.subheader("📊 WELLS SKORU")
    w_inputs = [st.checkbox(x) for x in ["Aktif Kanser (+1)", "Paralizi/İmmobilizasyon (+1)", "Yatak Bağımlılığı >3 Gün (+1)", "Venöz Hassasiyet (+1)", "Tüm Bacakta Şişlik (+1)", "Baldır Şişliği >3cm (+1)", "Gode Bırakan Ödem (+1)", "Kollateral Venler (+1)", "Alternatif Tanı Olasılığı Düşük (+1)"]]
    wells_score = sum(w_inputs)
    st.warning(f"Wells Skoru: {wells_score}")

    st.divider()
    hb = st.number_input("Hemoglobin (Hb)", 3.0, 25.0, value=st.session_state.ses_hb)
    wbc = st.number_input("WBC (Lökosit)", 0, 500000, value=st.session_state.ses_wbc)
    plt = st.number_input("PLT (Trombosit)", 0, 2000000, value=st.session_state.ses_plt)
    kre = st.number_input("Kreatinin", 0.1, 45.0, value=st.session_state.ses_kre)
    glu = st.number_input("AKŞ (Glukoz)", 0, 3000, value=st.session_state.ses_glu)
    na = st.number_input("Sodyum (Na)", 100, 190, 140)
    k = st.number_input("Potasyum (K)", 1.0, 15.0, 4.2)
    ca = st.number_input("Kalsiyum (Ca)", 5.0, 22.0, 9.5)
    ast_alt = st.checkbox("AST/ALT > 3 Kat Artış")
    trop = st.checkbox("Troponin Pozitif (+)")

    if kre > 0:
        base_egfr = ((140 - yas) * kilo) / (72 * kre)
        if cinsiyet == "Kadın": base_egfr *= 0.85
        egfr = round(base_egfr, 1)
    else: egfr = 0
    st.metric("eGFR Skoru", f"{egfr} ml/dk")

# Ses ile giriş
st.subheader("🎤 Ses ile Semptom + Lab + Ad Soyad Girişi")
audio_value = st.audio_input("Ses kaydı yapın")

all_possible_symptoms = [
    "Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Bradikardi", "Taşikardi", "Üfürüm",
    "Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne", "Hipoksi",
    "Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal", "Mide Bulantısı",
    "Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi", "Galaktore",
    "Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik", "Pitozis",
    "Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları",
    "Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)"
]

if audio_value is not None:
    if st.button("🔍 Sesi Analiz Et ve Tüm Verileri Doldur"):
        try:
            with st.spinner("Ses dinleniyor..."):
                prompt = f"""
Ses kaydını dinle ve SADECE şu formatta cevap ver (hiçbir açıklama yazma):

ADSOYAD: ...
SEMPTOMLAR: semptom1, semptom2, ...
CİNSİYET: Erkek veya Kadın
YAŞ: sayı
KİLO: sayı
HB: sayı
WBC: sayı
PLT: sayı
KRE: sayı
AKŞ: sayı

Olası semptomlar: {', '.join(all_possible_symptoms)}
"""
                response = model.generate_content(
                    [prompt, {"mime_type": "audio/wav", "data": audio_value.getvalue()}],
                    generation_config=genai.GenerationConfig(max_output_tokens=400, temperature=0.2)
                )
                text = response.text.strip()

                lines = text.split("\n")
                new_symptoms = []

                for line in lines:
                    line = line.strip()
                    upper_line = line.upper()

                    if any(k in upper_line for k in ["ADSOYAD", "AD SOYAD", "HATA ADI", "HASTA ADI", "İSİM", "AD:"]):
                        if ":" in line:
                            value = line.split(":", 1)[1].strip()
                            if value:
                                st.session_state.ses_protokol = value

                    elif line.startswith("SEMPTOMLAR:"):
                        new_symptoms = [s.strip() for s in line.replace("SEMPTOMLAR:", "").split(",") if s.strip() in all_possible_symptoms]
                    elif line.startswith("CİNSİYET:"): 
                        st.session_state.ses_cinsiyet = line.replace("CİNSİYET:", "").strip()
                    elif line.startswith("YAŞ:"):
                        try: st.session_state.ses_yas = int(line.replace("YAŞ:", "").strip())
                        except: pass
                    elif line.startswith("KİLO:"):
                        try: st.session_state.ses_kilo = int(line.replace("KİLO:", "").strip())
                        except: pass
                    elif line.startswith("HB:"):
                        try: st.session_state.ses_hb = float(line.replace("HB:", "").strip())
                        except: pass
                    elif line.startswith("WBC:"):
                        try: st.session_state.ses_wbc = int(line.replace("WBC:", "").strip())
                        except: pass
                    elif line.startswith("PLT:"):
                        try: st.session_state.ses_plt = int(line.replace("PLT:", "").strip())
                        except: pass
                    elif line.startswith("KRE:"):
                        try: st.session_state.ses_kre = float(line.replace("KRE:", "").strip())
                        except: pass
                    elif line.startswith("AKŞ:"):
                        try: st.session_state.ses_glu = int(line.replace("AKŞ:", "").strip())
                        except: pass

                if new_symptoms:
                    st.session_state.voice_symptoms = new_symptoms
                    st.success("✅ Ses analizi tamamlandı. Aşağıda algılanan semptomlar yeşil kutuda listeleniyor.")
                st.success(f"✅ Ad Soyad ve lab değerleri dolduruldu! → {st.session_state.ses_protokol}")
                st.rerun()
        except Exception as e:
            st.error(f"Ses analizi hatası: {e}")

# SESLE GELEN SEMPTOMLARIN ÖNİZLEMESİ
if st.session_state.voice_symptoms:
    st.subheader("🟢 Algılanan Semptomlar")
    st.markdown(f"<div style='background:#d4edda; padding:20px; border-radius:15px; color:#155724; font-weight:600;'>"
                f"{', '.join(st.session_state.voice_symptoms)}"
                f"</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Değiştir (Tekrar ses analizi yap)"):
            st.session_state.voice_symptoms = []
            st.rerun()
    with col2:
        if st.button("✅ Listeye Ekle"):
            for s in st.session_state.voice_symptoms:
                if s not in st.session_state.selected_symptoms:
                    st.session_state.selected_symptoms.append(s)
            st.success("✅ Semptomlar ana listeye eklendi!")
            st.session_state.voice_symptoms = []

# 3. KLİNİK BULGU SEÇİMİ
st.subheader("🔍 Klinik Semptom ve Fizik Muayene Bulguları")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KARDİYO", "🫁 PULMONER", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖROLOJİ", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENF"])

b = []
with t1: b.extend(st.multiselect("KV", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Bradikardi", "Taşikardi", "Üfürüm"], default=[s for s in st.session_state.selected_symptoms if s in ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Bradikardi", "Taşikardi", "Üfürüm"]]))
with t2: b.extend(st.multiselect("PULM", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne", "Hipoksi"], default=[s for s in st.session_state.selected_symptoms if s in ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne", "Hipoksi"]]))
with t3: b.extend(st.multiselect("GİS", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal", "Mide Bulantısı"], default=[s for s in st.session_state.selected_symptoms if s in ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal", "Mide Bulantısı"]]))
with t4: b.extend(st.multiselect("ENDO", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi", "Galaktore"], default=[s for s in st.session_state.selected_symptoms if s in ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi", "Galaktore"]]))
with t5: b.extend(st.multiselect("NÖRO", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik", "Pitozis"], default=[s for s in st.session_state.selected_symptoms if s in ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik", "Pitozis"]]))
with t6: b.extend(st.multiselect("HEM", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"], default=[s for s in st.session_state.selected_symptoms if s in ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"]]))
with t7: b.extend(st.multiselect("ROM", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)"], default=[s for s in st.session_state.selected_symptoms if s in ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)"]]))

# Sesle gelen semptomları buraya ekle
b.extend(st.session_state.voice_symptoms)

# Otomatik Lab Değerlendirme
if kre > 1.3: b.append("Böbrek Hasarı")
if hb < 11: b.append("Anemi")
if wbc > 12000: b.append("Lökositoz")
if plt < 140000: b.append("Trombositopeni")
if glu > 180: b.append("Hiperglisemi")
if na < 135: b.append("Hiponatremi")
if ast_alt: b.append("KC Hasarı")
if trop: b.append("Kardiyak İskemi")

# Görüntü yükleme
st.divider()
st.subheader("📸 RADYOLOJİK/KARDİYOLOJİK GÖRÜNTÜ ANALİZİ (AI)")
up_file = st.file_uploader("EKG, Röntgen veya Laboratuvar Sonucu Yükle", type=["jpg", "png", "jpeg"])

# MASTER DB - TAM LİSTE (hiçbir şey silinmedi, orijinal haliyle)
master_db = {
    "STEMI": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı", "Kardiyak İskemi", "Terleme", "Taşikardi"], "t": "EKG + Troponin", "ted": "ASA 300mg + Klopidogrel 600mg + IV Heparin + Acil Anjiyo."},
    "NSTEMI": {"b": ["Göğüs Ağrısı", "Kardiyak İskemi", "Bulantı", "Nefes Darlığı"], "t": "Seri Troponin + EKG", "ted": "Enoksaparin 1mg/kg SC + ASA + Beta Bloker."},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Taşikardi", "Siyanoz", "Hipoksi"], "t": "BT Anjiyo + D-Dimer", "ted": "Alteplaz 100mg (Masifse) + IV Heparin."},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Hipotansiyon", "Pupil Eşitsizliği", "Senkop"], "t": "BT Anjiyo + TEE", "ted": "IV Esmolol + Acil Cerrahi."},
    "Akut Kalp Yetersizliği": {"b": ["Nefes Darlığı", "Ral", "Boyun Ven Dolgunluğu", "Ortopne", "Bilateral Ödem"], "t": "proBNP + EKO", "ted": "IV Furosemid 40-80mg + Nitrat + CPAP."},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Üfürüm", "Peteşi", "Splenomegali", "Halsizlik"], "t": "Kan Kültürü + TEE", "ted": "IV Vankomisin + Seftriakson."},
    "Perikard Tamponadı": {"b": ["Hipotansiyon", "Boyun Ven Dolgunluğu", "Sessiz Kalp Sesleri", "Nefes Darlığı"], "t": "EKO", "ted": "Acil Perikardiyosentez."},
    "Atriyal Fibrilasyon (Hızlı)": {"b": ["Çarpıntı", "Nefes Darlığı", "Taşikardi", "Senkop"], "t": "EKG", "ted": "Metoprolol veya Diltiazem + Antikoagülan."},
    "Miyokardit": {"b": ["Göğüs Ağrısı", "Ateş (>38)", "Nefes Darlığı", "Kardiyak İskemi"], "t": "Kardiyak MR + Troponin", "ted": "İstirahat + Kalp Yetersizliği Tedavisi."},
    "Stabil Anjina": {"b": ["Göğüs Ağrısı", "Halsizlik"], "t": "Efor Testi", "ted": "ASA + Statini + Beta Bloker."},
    "Kardiyojenik Şok": {"b": ["Hipotansiyon", "Konfüzyon", "Taşikardi", "Oligüri"], "t": "Laktat + EKO", "ted": "Norepinefrin + Dobutamin."},
    "Hipertansif Acil Durum": {"b": ["Ani Baş Ağrısı", "Konfüzyon", "Göğüs Ağrısı", "Nefes Darlığı"], "t": "Tansiyon Takibi (>180/120)", "ted": "IV Nitroprussid veya Labetalol."},
    "Aort Stenozu": {"b": ["Senkop", "Göğüs Ağrısı", "Nefes Darlığı", "Üfürüm"], "t": "EKO", "ted": "Kapak Replasmanı (TAVI/Cerrahi)."},
    "Mitral Yetersizlik": {"b": ["Nefes Darlığı", "Ortopne", "Üfürüm", "Bilateral Ödem"], "t": "EKO", "ted": "Diüretik + ACE İnhibitörü + Cerrahi."},
    "Bradiaritmi (Tam Blok)": {"b": ["Bradikardi", "Senkop", "Hipotansiyon", "Konfüzyon"], "t": "EKG", "ted": "Atropin 0.5mg + Geçici Pacemaker."},
    "Varis Kanaması": {"b": ["Hematemez", "Melena", "Sarılık", "Asit", "Splenomegali"], "t": "Endoskopi", "ted": "IV Terlipressin 2mg + Seftriakson + Band Ligasyonu."},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Mide Bulantısı", "LDH Yüksekliği", "Lökositoz", "Karın Ağrısı"], "t": "Lipaz/Amilaz > 3x + BT", "ted": "NPO + Agresif SF (250ml/saat) + Analjezi."},
    "Hepatik Ensefalopati": {"b": ["Asteriksis", "Konfüzyon", "Sarılık", "Asit"], "t": "Amonyak", "ted": "Laktüloz + Rifaximin."},
    "Akut Kolanjit": {"b": ["Sarılık", "Ateş (>38)", "Karın Ağrısı", "Hipotansiyon", "Konfüzyon"], "t": "ERCP", "ted": "Acil ERCP + IV Antibiyotik."},
    "Peptik Ülser Kanaması": {"b": ["Hematemez", "Melena", "Karın Ağrısı", "Anemi"], "t": "Endoskopi", "ted": "IV PPI (80mg Bolus + 8mg/saat İnfüzyon)."},
    "Crohn Hastalığı": {"b": ["Karın Ağrısı", "İshal", "Kilo Kaybı", "Ağızda Aft"], "t": "BT Enterografi + Kolonoskopi", "ted": "Anti-TNF + Azatioprin."},
    "Ülseratif Kolit": {"b": ["Hematokezya", "İshal", "Karın Ağrısı", "Eklem Ağrısı"], "t": "Kolonoskopi", "ted": "Mesalazin + Steroid."},
    "Wilson Hastalığı": {"b": ["Tremor", "Sarılık", "Dizartri", "KC Hasarı"], "t": "Seruloplazmin + İdrar Bakırı", "ted": "D-Penisilamin + Çinko."},
    "Siroz": {"b": ["Sarılık", "Asit", "Hepatomegali", "Anemi", "Örümcek Anjiyom"], "t": "Albumin/INR + USG", "ted": "Spironolakton + Tuz Kısıtlaması."},
    "Akut Karaciğer Yetmezliği": {"b": ["Sarılık", "Konfüzyon", "KC Hasarı", "Asteriksis"], "t": "INR > 1.5", "ted": "NAC İnfüzyonu + Karaciğer Nakli."},
    "Çölyak": {"b": ["İshal", "Anemi", "Kilo Kaybı", "Karın Ağrısı"], "t": "Anti-tTG + Biyopsi", "ted": "Glutensiz Diyet."},
    "Akalazya": {"b": ["Disfaji", "Regürjitasyon", "Kilo Kaybı"], "t": "Manometri", "ted": "Balon Dilatasyonu / Heller."},
    "Gastroparezi": {"b": ["Mide Bulantısı", "Kusma", "Erken Doyma", "Karın Ağrısı"], "t": "Mide Boşalım Sintigrafisi", "ted": "Metoklopramid + Diyet."},
    "Hepatit B (Akut)": {"b": ["Sarılık", "Bulantı", "KC Hasarı", "İdrarda Koyu Renk"], "t": "Seroloji (HBsAg, Anti-HBc)", "ted": "Destek Tedavisi + İstirahat."},
    "Hepatit C (Kronik)": {"b": ["Halsizlik", "KC Hasarı", "Sarılık"], "t": "HCV-RNA", "ted": "Direkt Etkili Antiviraller (DAA)."},
    "Otoimmün Hepatit": {"b": ["Sarılık", "Eklem Ağrısı", "KC Hasarı", "Ateş (>38)"], "t": "ANA/ASMA + Biyopsi", "ted": "Steroid + Azatioprin."},
    "Primer Biliyer Kolanjit": {"b": ["Kaşıntı", "Sarılık", "Halsizlik", "Hepatomegali"], "t": "Anti-Mitokondriyal Antikor (AMA)", "ted": "Ursodeoksikolik Asit (UDCA)."},
    "Pankreas Kanseri": {"b": ["Sarılık", "Kuşak Ağrısı", "Kilo Kaybı", "Yeni Başlayan Diyabet"], "t": "Batın BT + CA 19-9", "ted": "Whipple Operasyonu / KT."},
    "Mezenter İskemi": {"b": ["Şiddetli Karın Ağrısı", "Bulantı", "Hipotansiyon", "Laktat Yüksekliği"], "t": "BT Anjiyo", "ted": "Acil Cerrahi / Embolektomi."},
    "Divertikülit": {"b": ["Karın Ağrısı", "Ateş (>38)", "Kabızlık", "Lökositoz"], "t": "Batın BT", "ted": "Antibiyotik + Sıvı Diyet."},
    "DKA": {"b": ["Aseton Kokusu", "Hiperglisemi", "Karın Ağrısı", "Konfüzyon", "Poliüri"], "t": "Kan Gazı + Keton", "ted": "IV SF + İnsülin İnfüzyonu + K+."},
    "Tiroid Fırtınası": {"b": ["Ateş (>38)", "Taşikardi", "Konfüzyon", "Tremor", "Sarılık"], "t": "Burch-Wartofsky Skoru", "ted": "PTU + Lugol + Beta Bloker + IV Steroid."},
    "Addison Krizi": {"b": ["Hipotansiyon", "Hiperpigmentasyon", "Hiponatremi", "Karın Ağrısı"], "t": "Kortizol + ACTH Testi", "ted": "IV Hidrokortizon 100mg + SF."},
    "Miksödem Koması": {"b": ["Bradikardi", "Konfüzyon", "Soğuk İntoleransı", "Bilateral Ödem"], "t": "TSH + fT4", "ted": "IV L-Tiroksin + IV Steroid."},
    "Feokromositoma": {"b": ["Ani Baş Ağrısı", "Çarpıntı", "Terleme", "Hipotansiyon"], "t": "İdrar Metanefrinleri", "ted": "Alfa Bloker -> Beta Bloker."},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria", "Hiperglisemi", "Hipotansiyon"], "t": "DEX Baskılama Testi", "ted": "Cerrahi Müdahale."},
    "Diabetes Insipidus": {"b": ["Poliüri", "Polidipsi", "Hipernatremi"], "t": "Susuzluk Testi", "ted": "Desmopressin."},
    "Hiperkalsemik Kriz": {"b": ["Hiperkalsemi", "Konfüzyon", "Poliüri", "Bradikardi"], "t": "PTH + Ca", "ted": "SF Hidrasyon + Zoledronik Asit."},
    "Akromegali": {"b": ["El-Ayak Büyümesi", "Disfaji", "Ani Baş Ağrısı"], "t": "IGF-1 + MR", "ted": "Cerrahi + Somatostatin."},
    "Hipoglisemi Koması": {"b": ["Konfüzyon", "Terleme", "Taşikardi", "Nöbet"], "t": "Kan Şekeri < 50", "ted": "IV %10-20 Dekstroz Bolus."},
    "Primer Hiperaldosteronizm": {"b": ["Hipotansiyon", "Kas Güçsüzlüğü", "Poliüri"], "t": "Aldosteron/Renin Oranı", "ted": "Spironolakton / Cerrahi."},
    "Hipoparatiroidi": {"b": ["Kas Spazmı", "Nöbet", "Parezi"], "t": "Düşük Ca + Düşük PTH", "ted": "Kalsiyum + Vitamin D."},
    "Prolaktinoma": {"b": ["Galaktore", "Ani Baş Ağrısı", "Görme Bozukluğu"], "t": "Prolaktin + MR", "ted": "Kabergolin / Bromokriptin."},
    "SIADH": {"b": ["Hiponatremi", "Konfüzyon", "Nöbet", "Bulantı"], "t": "İdrar Sodyumu / Ozmolarite", "ted": "Sıvı Kısıtlaması + Tolvaptan."},
    "Hashimoto Tiroiditi": {"b": ["Halsizlik", "Soğuk İntoleransı", "Bilateral Ödem", "Kabızlık"], "t": "Anti-TPO + TSH", "ted": "Levotiroksin."},
    "TTP": {"b": ["Trombositopeni", "Anemi", "Konfüzyon", "Peteşi", "LDH Yüksekliği"], "t": "Şistosit + ADAMTS13", "ted": "Acil Plazmaferez + Steroid."},
    "Multipl Miyelom": {"b": ["Kemik Ağrısı", "Böbrek Hasarı", "Hiperkalsemi", "Anemi"], "t": "M-Spike + KİB", "ted": "VCD Protokolü + Bisfosfonat."},
    "AML": {"b": ["Anemi", "Lökositoz", "Trombositopeni", "Kemik Ağrısı", "Ateş (>38)"], "t": "KİB + Akım Sitometrisi", "ted": "Kemoterapi (7+3)."},
    "Lenfoma": {"b": ["Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Ateş (>38)"], "t": "Lenf Nodu Biyopsisi", "ted": "R-CHOP / ABVD."},
    "PNH": {"b": ["Hemoptizi", "Anemi", "Karın Ağrısı", "Trombositopeni"], "t": "CD55/CD59", "ted": "Eculizumab."},
    "DIC": {"b": ["Peteşi", "Diş Eti Kanaması", "Trombositopeni", "LDH Yüksekliği"], "t": "D-Dimer + Fibrinojen", "ted": "TDP + Trombosit + Neden Tedavisi."},
    "Polisitemia Vera": {"b": ["Polisitemi", "Splenomegali", "Kaşıntı", "Ani Baş Ağrısı"], "t": "JAK2 Mutasyonu", "ted": "Flebotomi + Aspirin."},
    "İTP": {"b": ["Trombositopeni", "Peteşi", "Diş Eti Kanaması"], "t": "Tanı Dışlama", "ted": "Steroid + IVIG."},
    "Aplastik Anemi": {"b": ["Anemi", "Lökopeni", "Trombositopeni", "Halsizlik"], "t": "Kemik İliği Biyopsisi", "ted": "Kök Hücre Nakli / ATG."},
    "B12 Eksikliği": {"b": ["Anemi", "Ataksi", "Dizartri", "Konfüzyon"], "t": "B12 Düzeyi", "ted": "IM B12 Enjeksiyonu."},
    "Hemofili A/B": {"b": ["Eklem Kanaması", "Ekimoz", "Diş Eti Kanaması"], "t": "Faktör Düzeyi + aPTT", "ted": "Faktör Replasmanı."},
    "Von Willebrand Hastalığı": {"b": ["Peteşi", "Burun Kanaması", "Diş Eti Kanaması"], "t": "vWF Aktivitesi", "ted": "Desmopressin / Faktör."},
    "Miyelodisplastik Sendrom (MDS)": {"b": ["Anemi", "Lökopeni", "Enfeksiyon Sıklığı", "Halsizlik"], "t": "KİB (Displazi)", "ted": "Azasitidin / Destek."},
    "Esansiyel Trombositemi": {"b": ["Trombositoz (>600k)", "Eritromelalji", "Ani Baş Ağrısı"], "t": "JAK2 / CALR Mutasyonu", "ted": "Hidroksiüre + Aspirin."},
    "Miyelofibrozis": {"b": ["Splenomegali", "Anemi", "Kilo Kaybı", "Kemik Ağrısı"], "t": "Kemik İliği (Kuru Aspirasyon)", "ted": "Ruxolitinib / Nakil."},
    "SLE (Lupus)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Böbrek Hasarı", "Lökopeni"], "t": "ANA + Anti-dsDNA", "ted": "Steroid + MMF + Plaquenil."},
    "Behçet Hastalığı": {"b": ["Ağızda Aft", "Uveit", "Paterji Reaksiyonu", "Eklem Ağrısı"], "t": "HLA-B51", "ted": "Kolşisin + Azatioprin."},
    "Ankilozan Spondilit": {"b": ["Bel Ağrısı (İnflamatuar)", "Sabah Sertliği", "Uveit"], "t": "HLA-B27 + MR", "ted": "NSAİİ + Anti-TNF."},
    "GPA (Wegener)": {"b": ["Hemoptizi", "Böbrek Hasarı", "Kuru Öksürük", "Burun Kanaması"], "t": "c-ANCA", "ted": "Rituksimab + Steroid."},
    "Sjögren Sendromu": {"b": ["Göz Kuruluğu", "Ağız Kuruluğu", "Artralji", "Lenfadenopati"], "t": "Anti-SSA/SSB + Schirmer Testi", "ted": "Suni Gözyaşı + Plaquenil."},
    "Skleroderma": {"b": ["Deri Sertleşmesi", "Raynaud", "Disfaji", "Nefes Darlığı"], "t": "Anti-Scl-70", "ted": "MMF + Kalsiyum Kanal Blokeri."},
    "Dermatomiyozit": {"b": ["Parezi", "Kelebek Döküntü", "KC Hasarı", "Artralji"], "t": "CK + Kas Biyopsisi", "ted": "Yüksek Doz Steroid."},
    "Gut Artriti": {"b": ["Eklem Ağrısı", "Ateş (>38)", "Lökositoz"], "t": "Ürik Asit + Eklem Sıvısı", "ted": "Kolşisin + NSAİİ."},
    "Romatoid Artrit": {"b": ["Eklem Ağrısı", "Sabah Sertliği", "Halsizlik"], "t": "RF + Anti-CCP", "ted": "Metotreksat + Steroid."},
    "Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon", "Taşikardi"], "t": "Laktat > 2 + Kültür", "ted": "30ml/kg SF + Norepinefrin + Antibiyotik."},
    "Bakteriyel Menenjit": {"b": ["Ense Sertliği", "Ateş (>38)", "Ani Baş Ağrısı", "Fotofobi"], "t": "Lomber Ponksiyon", "ted": "IV Seftriakson + Vankomisin."},
    "Goodpasture": {"b": ["Hemoptizi", "Böbrek Hasarı", "Nefes Darlığı", "Anemi"], "t": "Anti-GBM Antikoru", "ted": "Plazmaferez + Steroid."},
    "Miyastenia Gravis": {"b": ["Parezi", "Disfaji", "Pitozis", "Nefes Darlığı"], "t": "Anti-AChR + Tensilon", "ted": "Piridostigmin + IVIG."},
    "Bruselloz": {"b": ["Ateş (>38)", "Eklem Ağrısı", "Terleme", "Splenomegali"], "t": "Rose Bengal + Wright", "ted": "Doksisiklin + Rifampisin."},
    "Sıtma": {"b": ["Ateş (>38)", "Sarılık", "Splenomegali", "Trombositopeni"], "t": "Kalın Damla Yayma", "ted": "Artemisin."},
    "KBY (Evre 5)": {"b": ["Böbrek Hasarı", "Bilateral Ödem", "Hipotansiyon", "Anemi"], "t": "eGFR < 15", "ted": "Acil Diyaliz + Sıvı Kısıtlaması."},
    "Nefrotik Sendrom": {"b": ["Bilateral Ödem", "Böbrek Hasarı", "Halsizlik"], "t": "24s Protein > 3.5g", "ted": "Steroid + ACE İnhibitörü."},
    "Piyelonefrit": {"b": ["Karın Ağrısı", "Ateş (>38)", "Bulantı", "Lökositoz"], "t": "İdrar Kültürü", "ted": "IV Siprofloksasin / Seftriakson."},
    "İnterstisyel Akciğer Hastalığı": {"b": ["Nefes Darlığı", "Kuru Öksürük", "Ral", "Çomak Parmak"], "t": "HRCT (BT)", "ted": "Steroid + Nintedanib."},
    "Sarkoidoz": {"b": ["Nefes Darlığı", "Lenfadenopati", "Uveit", "Kuru Öksürük"], "t": "ACE + Akciğer Grafisi", "ted": "Oral Steroid."},
}

# ANALİZİ BAŞLAT
if st.button("🚀 ANALİZİ BAŞLAT"):
    if not b:
        st.error("Klinik veri girişi yapılmadı!")
    else:
        results = []
        for ad, v in master_db.items():
            matches = set(b).intersection(set(v["b"]))
            if matches:
                score = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": score, "v": v, "m": list(matches)})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        c1, c2 = st.columns([1.8, 1])
        with c1:
            st.markdown("### 🏛️ Teşhis ve Tedavi Paneli")
            for r in results:
                st.markdown(f"""
                <div class='clinical-card'>
                    <div style='font-size:3rem; font-weight:800; color:#000;'>{r['ad']} (%{r['puan']})</div>
                    <p style='color:#DC2626; font-weight:700;'>KRİTİK BULGULAR: {", ".join(r['m'])}</p>
                    <hr style='border: 2px solid #DC2626;'>
                    <p>🧪 <b>İleri Tetkik:</b> {r['v']['t']}</p>
                    <p style='background:#FFF4F4; padding:25px; border-radius:30px; border-left:20px solid #DC2626;'>
                        💊 <b>DETAYLI TEDAVİ:</b> {r['v']['ted']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            if results and not st.session_state.top_tani_seslendirildi:
                top = results[0]
                tts_text = f"En yüksek ön tanı {top['ad']} yüzde {top['puan']}"
                try:
                    tts = gTTS(text=tts_text, lang='tr')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3", autoplay=True)
                    st.success(f"🔊 En yüksek ön tanı otomatik seslendiriliyor: {top['ad']} (%{top['puan']})")
                    st.session_state.top_tani_seslendirildi = True
                except:
                    st.warning("Seslendirme şu anda kullanılamıyor.")

        with c2:
            st.markdown("### 📝 EPİKRİZ VE AI ANALİZİ")
            st.info("🤖 Gemini AI Klinik Yorumu:")
            
            if st.session_state.ai_klinik_yorum is None:
                try:
                    with st.spinner("Gemini analiz ediliyor..."):
                        vaka_data = f"""
Hasta: {yas}y {cinsiyet}. Ad Soyad: {p_no}. GCS: {gcs_skor}, Wells: {wells_score}.
Lab: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}, eGFR {egfr}, AKŞ {glu}.
Semptomlar: {', '.join(b)}.
Lütfen bu verileri uzman bir dahiliyeci gözüyle analiz et.
"""
                        contents = [vaka_data]
                        if up_file:
                            img = Image.open(up_file)
                            contents.append(img)

                        ai_res = model.generate_content(
                            contents,
                            generation_config=genai.GenerationConfig(max_output_tokens=1200, temperature=0.25)
                        )
                        st.session_state.ai_klinik_yorum = ai_res.text
                except Exception as e:
                    st.session_state.ai_klinik_yorum = f"❌ AI Hatası: {str(e)}\n\n30-60 saniye bekleyip tekrar deneyin."
            
            if st.session_state.ai_klinik_yorum:
                if "❌" in st.session_state.ai_klinik_yorum:
                    st.error(st.session_state.ai_klinik_yorum)
                else:
                    st.markdown(f"<div style='background:#f0f2f6; padding:15px; border-radius:10px;'>{st.session_state.ai_klinik_yorum}</div>", unsafe_allow_html=True)

            st.divider()
            epi = f"""DAHİLİYE KLİNİK KARAR ROBOTU\n---------------------------\nAD SOYAD: {p_no}\nHASTA CİNSİYETİ: {cinsiyet}\nTARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}\nLAB: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}\nGCS: {gcs_skor}, Wells: {wells_score}\neGFR: {egfr} ml/dk\n\nBELİRTİLER:\n{", ".join(b)}\n\nÖN TANI LİSTESİ:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in results[:15]])}\n\nGELİŞTİRİCİ: İSMAİL ORHAN\n---------------------------"""
            st.markdown(f"<pre style='background:white; padding:40px; border-radius:45px; border:10px solid #DC2626; color:#000; font-size:14px; white-space: pre-wrap;'>{epi}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Epikrizi İndir", epi, file_name=f"{p_no}_V30.txt")

st.markdown("---")
st.caption("GELİŞTİRİCİ: İSMAİL ORHAN GEMLİK 2026")
