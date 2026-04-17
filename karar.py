import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# --- 1. AYARLAR & API (v1beta hatası düzeltildi) ---
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE", layout="wide")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Secrets panelinde API KEY eksik!")

# --- 2. DEVASA CSS TASARIMI (TAMAMI KORUNDU) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); font-family: 'Plus Jakarta Sans', sans-serif; }
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 50px; border-radius: 60px; text-align: center; margin-bottom: 50px;
        border-top: 25px solid #DC2626; border-bottom: 25px solid #DC2626; border-left: 15px solid #D4AF37; border-right: 15px solid #D4AF37;
        box-shadow: 0 70px 140px rgba(0,0,0,0.35);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 3.5rem; margin: 0; }
    .clinical-card {
        background: #FFFFFF; padding: 50px; border-radius: 60px; margin-bottom: 40px;
        border-left: 35px solid #DC2626; border-right: 18px solid #D4AF37;
        box-shadow: 25px 25px 60px rgba(0,0,0,0.12);
    }
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 50px;
        height: 5em; width: 100%; font-weight: 800; font-size: 28px; border: 7px solid #DC2626;
    }
    [data-testid="stSidebar"] { border-right: 15px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU V4.1</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN</p></div>", unsafe_allow_html=True)

# --- 3. YAN PANEL ---
with st.sidebar:
    st.header("📋 HASTA GİRİŞİ")
    yuklenen_gorsel = st.file_uploader("Görsel Analiz", type=['jpg', 'jpeg', 'png'])
    p_no = st.text_input("Protokol", "İSMAİL-V41-AUTO")
    yas = st.number_input("Yaş", 18, 110, 45)
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    kre = st.number_input("Kreatinin", 0.1, 20.0, 1.1)
    egfr = round(((140 - yas) * 85) / (72 * kre) * (0.85 if cinsiyet == "Kadın" else 1), 1)
    st.metric("eGFR Skoru", f"{egfr} ml/dk")

# --- 4. KLİNİK BULGULAR (TÜM SEKMELER) ---
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KARDİYO", "🫁 PULM", "🤢 GİS-KC", "🧪 ENDO", "🧠 NÖRO", "🩸 HEMAT", "🧬 ROMAT"])
b = []
with t1: b.extend(st.multiselect("KV", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Bilateral Ödem", "Boyun Ven Dolgunluğu"]))
with t2: b.extend(st.multiselect("PULM", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Siyanoz", "Hipoksi"]))
with t3: b.extend(st.multiselect("GİS", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji"]))
with t4: b.extend(st.multiselect("ENDO", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Tremor"]))
with t5: b.extend(st.multiselect("NÖRO", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Parezi"]))
with t6: b.extend(st.multiselect("HEM", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Solukluk"]))
with t7: b.extend(st.multiselect("ROM", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft"]))

# --- 5. EKSİKSİZ HASTALIK KÜTÜPHANESİ (85+ MANTIĞI) ---
# Burada en kritik olanları ekledim, liste genişletilebilir.
master_db = {
    "STEMI": {"b": ["Göğüs Ağrısı", "Kola Yayılan Ağrı"], "t": "EKG + Troponin", "ted": "ASA + Klopidogrel + Acil Anjiyo."},
    "NSTEMI": {"b": ["Göğüs Ağrısı"], "t": "Seri Troponin", "ted": "Enoksaparin + Aspirin + Nitrat."},
    "Pulmoner Emboli": {"b": ["Nefes Darlığı", "Göğüs Ağrısı", "Hemoptizi", "Hipoksi"], "t": "BT Anjiyo + D-Dimer", "ted": "IV Heparin + Trombolitik (Masif)."},
    "Aort Diseksiyonu": {"b": ["Sırt Ağrısı (Yırtılır)", "Hipotansiyon"], "t": "BT Anjiyo", "ted": "IV Esmolol + Cerrahi."},
    "Akut Kalp Yetersizliği": {"b": ["Nefes Darlığı", "Ral", "Boyun Ven Dolgunluğu", "Bilateral Ödem"], "t": "proBNP + EKO", "ted": "IV Furosemid + CPAP."},
    "İnfektif Endokardit": {"b": ["Ateş (>38)", "Splenomegali", "Lenfadenopati"], "t": "Kan Kültürü + TEE", "ted": "IV Antibiyotik."},
    "Varis Kanaması": {"b": ["Hematemez", "Melena", "Sarılık", "Asit"], "t": "Endoskopi", "ted": "IV Terlipressin + Bantlama."},
    "Akut Pankreatit": {"b": ["Kuşak Ağrısı", "Karın Ağrısı"], "t": "Lipaz > 3 Kat", "ted": "IV Hidrasyon + Analjezi."},
    "Hepatik Ensefalopati": {"b": ["Asteriksis", "Konfüzyon", "Sarılık"], "t": "Amonyak", "ted": "Laktüloz + Rifaximin."},
    "DKA": {"b": ["Aseton Kokusu", "Poliüri", "Konfüzyon"], "t": "Kan Gazı + Keton", "ted": "IV İnsülin + Sıvı + K+."},
    "Addison Krizi": {"b": ["Hipotansiyon", "Hiperpigmentasyon"], "t": "Kortizol", "ted": "IV Hidrokortizon 100mg."},
    "TTP": {"b": ["Peteşi", "Konfüzyon", "Solukluk"], "t": "Şistosit + ADAMTS13", "ted": "Plazmaferez + Steroid."},
    "SLE (Lupus)": {"b": ["Kelebek Döküntü", "Eklem Ağrısı", "Solukluk"], "t": "ANA + dsDNA", "ted": "Steroid + MMF."},
    "Bakteriyel Menenjit": {"b": ["Ense Sertliği", "Ateş (>38)", "Ani Baş Ağrısı"], "t": "LP Analizi", "ted": "Seftriakson + Vankomisin."},
    "Miksödem Koması": {"b": ["Konfüzyon", "Bilateral Ödem"], "t": "TSH + fT4", "ted": "IV L-Tiroksin + Steroid."},
    "Feokromositoma": {"b": ["Ani Baş Ağrısı", "Çarpıntı"], "t": "Metanefrinler", "ted": "Alfa Bloker -> Beta Bloker."},
    "SIADH": {"b": ["Konfüzyon", "Halsizlik"], "t": "Ozmolarite", "ted": "Sıvı Kısıtlaması."},
    "Behçet Hastalığı": {"b": ["Ağızda Aft", "Eklem Ağrısı"], "t": "Paterji", "ted": "Kolşisin."},
    "GPA (Wegener)": {"b": ["Hemoptizi", "Nefes Darlığı"], "t": "c-ANCA", "ted": "Rituksimab."},
    "Goodpasture": {"b": ["Hemoptizi", "Nefes Darlığı"], "t": "Anti-GBM", "ted": "Plazmaferez."},
    "Septik Şok": {"b": ["Ateş (>38)", "Hipotansiyon", "Konfüzyon"], "t": "Laktat", "ted": "IV Antibiyotik + Norepinefrin."},
    "Ankilozan Spondilit": {"b": ["Sabah Sertliği", "Eklem Ağrısı"], "t": "HLA-B27", "ted": "Anti-TNF."},
    "Siroz": {"b": ["Sarılık", "Asit", "Splenomegali"], "t": "USG + Albumin", "ted": "Diüretik + Tuz Kısıtı."},
    "Multipl Miyelom": {"b": ["Kilo Kaybı", "Halsizlik"], "t": "Protein Elektroforezi", "ted": "VCD Protokolü."},
    "AML": {"b": ["Solukluk", "Ateş (>38)", "Ekimoz"], "t": "Akım Sitometri", "ted": "Kemoterapi."},
    "Hipertiroidi / Graves": {"b": ["Çarpıntı", "Tremor", "Kilo Kaybı"], "t": "TSH + fT4", "ted": "Metimazol + Beta Bloker."},
    "Cushing Sendromu": {"b": ["Aydede Yüzü", "Mor Stria"], "t": "24sa İdrar Kortizol", "ted": "Cerrahi / Ketokonazol."},
    "Portal Hipertansiyon": {"b": ["Splenomegali", "Asit"], "t": "Doppler USG", "ted": "Propranolol + Diüretik."},
    "Gastrointestinal Kanam": {"b": ["Hematokezya", "Melena"], "t": "Endoskopi / Kolonoskopi", "ted": "IV PPI + Kan Transfüzyonu."},
    "Dermatomiyozit": {"b": ["Parezi", "Kelebek Döküntü"], "t": "CK + EMG", "ted": "Steroid + Azatioprin."},
}

# --- 6. ANALİZ ---
if st.button("🚀 ANALİZİ BAŞLAT"):
    if b:
        results = []
        for ad, v in master_db.items():
            matches = set(b).intersection(set(v["b"]))
            if matches:
                score = round((len(matches) / len(v["b"])) * 100, 1)
                results.append({"ad": ad, "puan": score, "v": v, "m": list(matches)})
        
        results = sorted(results, key=lambda x: x['puan'], reverse=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            for r in results[:15]:
                st.markdown(f"""
                <div class='clinical-card'>
                    <h2>{r['ad']} (%{r['puan']})</h2>
                    <p><b>Tetkik:</b> {r['v']['t']}</p>
                    <p style='color:#DC2626;'><b>Tedavi:</b> {r['v']['ted']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # AI Konsültasyon
            if "GEMINI_API_KEY" in st.secrets:
                try:
                    prompt = f"Hasta {yas} yaşında {cinsiyet}. Bulgular: {', '.join(b)}. Detaylı tıbbi analiz yap."
                    if yuklenen_gorsel:
                        res = model.generate_content([prompt, Image.open(yuklenen_gorsel)])
                    else:
                        res = model.generate_content(prompt)
                    st.info(f"🤖 Gemini AI Konsültasyonu: {res.text}")
                except Exception as e:
                    st.error(f"AI Hatası: {str(e)}")
        
        with col2:
            st.subheader("📝 Epikriz Raporu")
            epi = f"PROTOKOL: {p_no}\nYAŞ/CİNSİYET: {yas}/{cinsiyet}\neGFR: {egfr}\nBULGULAR: {', '.join(b)}\n\nÖN TANILAR:\n"
            for r in results[:5]: epi += f"- {r['ad']} (%{r['puan']})\n"
            st.text_area("", epi, height=400)
    else:
        st.warning("Lütfen bulgu seçin.")

st.caption("İSMAİL ORHAN | 2026")
