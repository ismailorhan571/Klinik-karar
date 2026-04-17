import streamlit as st
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# --- 1. PREMIUM UI ARCHITECTURE (İSMAİL ORHAN | V30 TITANIC-GENDER) ---
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE ROBOTU", page_icon="💊", layout="wide")

# AI Yapılandırması (Eklendi)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Secrets'da 'GEMINI_API_KEY' bulunamadı!")

# === YENİ: CACHE İÇİN (Rate limit koruması) ===
if 'ai_klinik_yorum' not in st.session_state:
    st.session_state.ai_klinik_yorum = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #FDFCF0 0%, #E8E2D2 100%); color: #1A1A1A; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .main-header {
        background: rgba(255, 255, 255, 0.98); padding: 40px; border-radius: 50px; text-align: center; margin-bottom: 40px;
        border-top: 20px solid #DC2626; border-bottom: 20px solid #DC2626; border-left: 12px solid #D4AF37; border-right: 12px solid #D4AF37;
        box-shadow: 0 60px 120px rgba(0,0,0,0.3);
    }
    .main-header h1 { color: #000; font-weight: 800; font-size: 3.2rem; margin: 0; }
    .main-header p { color: #DC2626; font-size: 1.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 5px; margin-top: 15px; }

    .clinical-card { 
        background: #FFFFFF; padding: 50px; border-radius: 60px; margin-bottom: 40px;
        border-left: 35px solid #DC2626; border-right: 18px solid #D4AF37;
        box-shadow: 25px 25px 60px rgba(0,0,0,0.12);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000 0%, #333 100%); color: #FFF; border-radius: 50px;
        height: 7em; width: 100%; font-weight: 800; font-size: 35px; border: 7px solid #DC2626;
    }
    .stButton>button:hover { background: #DC2626; transform: scale(1.01); color: white; }
    
    [data-testid="stSidebar"] { background-color: #F8F7EB; border-right: 15px solid #DC2626; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>DAHİLİYE KLİNİK KARAR ROBOTU</h1><p>GELİŞTİRİCİ: İSMAİL ORHAN </p></div>", unsafe_allow_html=True)

# 2. LABORATUVAR TERMİNALİ (V30 + YENİ SKORLAMALAR)
with st.sidebar:
    st.markdown("### 🏛️ LABORATUVAR VERİ MERKEZİ")
    p_no = st.text_input("Protokol No", "İSMAİL-V30-FINAL")
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    yas = st.number_input("Yaş", 0, 120, 45)
    kilo = st.number_input("Kilo (kg)", 5, 250, 85)
    st.divider()
    
    # EKLENTİ 1: GKS DEĞERLENDİRMELİ (Sadece sonuç değil, klinik seçimli)
    st.subheader("🧠 GKS DEĞERLENDİRMESİ")
    g_e = st.selectbox("Göz (E)", [4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Ağrıyla','Sesle','Spontan'][x-1]}")
    g_v = st.selectbox("Sözel (V)", [5, 4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Anlamsız Ses','Uygunsuz Kelime','Konfüze','Oryante'][x-1]}")
    g_m = st.selectbox("Motor (M)", [6, 5, 4, 3, 2, 1], format_func=lambda x: f"{x}: {['Yok','Ekstansiyon','Fleksiyon','Ağrıdan Kaçar','Ağrıyı Lokalize','Emre Uyar'][x-1]}")
    gcs_skor = g_e + g_v + g_m
    st.info(f"Toplam GCS: {gcs_skor}")

    st.divider()
    # EKLENTİ 2: WELLS SKORLAMASI
    st.subheader("📊 WELLS SKORU")
    w_inputs = [
        st.checkbox("Aktif Kanser (+1)"), st.checkbox("Paralizi/İmmobilizasyon (+1)"),
        st.checkbox("Yatak Bağımlılığı >3 Gün (+1)"), st.checkbox("Venöz Hassasiyet (+1)"),
        st.checkbox("Tüm Bacakta Şişlik (+1)"), st.checkbox("Baldır Şişliği >3cm (+1)"),
        st.checkbox("Gode Bırakan Ödem (+1)"), st.checkbox("Kollateral Venler (+1)"),
        st.checkbox("Alternatif Tanı Olasılığı Düşük (+1)")
    ]
    wells_score = sum(w_inputs)
    st.warning(f"Wells Skoru: {wells_score}")

    st.divider()
    kre = st.number_input("Kreatinin", 0.1, 45.0, 1.1)
    hb = st.number_input("Hemoglobin (Hb)", 3.0, 25.0, 14.0)
    wbc = st.number_input("WBC (Lökosit)", 0, 500000, 8500)
    plt = st.number_input("PLT (Trombosit)", 0, 2000000, 245000)
    glu = st.number_input("AKŞ (Glukoz)", 0, 3000, 105)
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

# 3. KLİNİK BULGU SEÇİMİ (Senin Orijinal Tab Yapın)
st.subheader("🔍 Klinik Semptom ve Fizik Muayene Bulguları")
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["🫀 KARDİYO", "🫁 PULMONER", "🤢 GİS-KC", "🧪 ENDOKRİN", "🧠 NÖROLOJİ", "🩸 HEMATO-ONKO", "🧬 ROMATO-ENF"])

b = []
with t1: b.extend(st.multiselect("KV", ["Göğüs Ağrısı", "Sırt Ağrısı (Yırtılır)", "Kola Yayılan Ağrı", "Çarpıntı", "Hipotansiyon", "Senkop", "Bilateral Ödem", "Boyun Ven Dolgunluğu", "S3/S4 Sesi", "Bradikardi", "Taşikardi", "Üfürüm"]))
with t2: b.extend(st.multiselect("PULM", ["Nefes Darlığı", "Hemoptizi", "Kuru Öksürük", "Balgamlı Öksürük", "Ral", "Ronküs", "Wheezing", "Stridor", "Plevritik Ağrı", "Siyanoz", "Ortopne", "Hipoksi"]))
with t3: b.extend(st.multiselect("GİS", ["Hematemez", "Melena", "Hematokezya", "Sarılık", "Asit", "Hepatomegali", "Splenomegali", "Kuşak Ağrısı", "Disfaji", "Asteriksis", "Murphy Belirtisi", "Karın Ağrısı", "Rebound", "Kabızlık", "İshal", "Mide Bulantısı"]))
with t4: b.extend(st.multiselect("ENDO", ["Poliüri", "Polidipsi", "Aseton Kokusu", "Aydede Yüzü", "Mor Stria", "Hiperpigmentasyon", "Ekzoftalmi", "Boyunda Şişlik", "Tremor", "Soğuk İntoleransı", "Sıcak İntoleransı", "El-Ayak Büyümesi", "Galaktore"]))
with t5: b.extend(st.multiselect("NÖRO", ["Konfüzyon", "Ense Sertliği", "Nöbet", "Dizartri", "Ataksi", "Ani Baş Ağrısı", "Fotofobi", "Parezi", "Pupil Eşitsizliği", "Dengesizlik", "Pitozis"]))
with t6: b.extend(st.multiselect("HEM", ["Peteşi", "Purpura", "Ekimoz", "Lenfadenopati", "Kilo Kaybı", "Gece Terlemesi", "Kaşıntı", "Solukluk", "Kemik Ağrısı", "Diş Eti Kanaması", "B Semptomları"]))
with t7: b.extend(st.multiselect("ROM", ["Ateş (>38)", "Eklem Ağrısı", "Sabah Sertliği", "Kelebek Döküntü", "Raynaud", "Ağızda Aft", "Göz Kuruluğu", "Deri Sertleşmesi", "Uveit", "Paterji Reaksiyonu", "Bel Ağrısı (İnflamatuar)"]))

# Otomatik Lab Değerlendirme (Senin Mantığın)
if kre > 1.3: b.append("Böbrek Hasarı")
if hb < 11: b.append("Anemi")
if wbc > 12000: b.append("Lökositoz")
if plt < 140000: b.append("Trombositopeni")
if glu > 180: b.append("Hiperglisemi")
if na < 135: b.append("Hiponatremi")
if ast_alt: b.append("KC Hasarı")
if trop: b.append("Kardiyak İskemi")

# EKLENTİ 3: GÖRÜNTÜ YÜKLEME ALANI
st.divider()
st.subheader("📸 RADYOLOJİK/KARDİYOLOJİK GÖRÜNTÜ ANALİZİ (AI)")
up_file = st.file_uploader("EKG, Röntgen veya Laboratuvar Sonucu Yükle", type=["jpg", "png", "jpeg"])

# 4. MASTER 85+ HASTALIK VERİTABANI (Senin Orijinal Listen - Tek Satırına Dokunulmadı)
master_db = { ... }  # (Tamamen aynı, burayı kısalttım ama kodunda aynı kalacak)

# 5. FINAL ANALİZ MOTORU + AI GÜCÜ
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

        with c2:
            st.markdown("### 📝 EPİKRİZ VE AI ANALİZİ")
            
            # === YENİ: AI CACHE + RATE LIMIT KORUMASI (Sadece burası değişti) ===
            st.info("🤖 Gemini AI Klinik Yorumu:")
            
            if st.session_state.ai_klinik_yorum is None:
                try:
                    with st.spinner("Gemini analiz ediliyor... (Kota koruması aktif - 15-30 sn bekleyebilirsiniz)"):
                        model = genai.GenerativeModel('gemini-2.5-flash-lite')   # ← Daha yüksek kota
                        vaka_data = f"""
                        Hasta: {yas}y {cinsiyet}. GCS: {gcs_skor}, Wells: {wells_score}.
                        Lab: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}, eGFR {egfr}.
                        Semptomlar: {b}. 
                        Lütfen bu verileri uzman bir dahiliyeci gözüyle analiz et.
                        """
                        if up_file:
                            img = Image.open(up_file)
                            ai_res = model.generate_content([vaka_data, img])
                        else:
                            ai_res = model.generate_content(vaka_data)
                        st.session_state.ai_klinik_yorum = ai_res.text
                except Exception as e:
                    st.session_state.ai_klinik_yorum = f"❌ AI Hatası: {str(e)}\n\n💡 İpucu: 30-60 saniye bekleyip tekrar 'ANALİZİ BAŞLAT' butonuna basın."
            
            # Sonucu göster (orijinal stil korunarak)
            if st.session_state.ai_klinik_yorum:
                if "❌" in st.session_state.ai_klinik_yorum:
                    st.error(st.session_state.ai_klinik_yorum)
                else:
                    st.markdown(f"<div style='background:#f0f2f6; padding:15px; border-radius:10px;'>{st.session_state.ai_klinik_yorum}</div>", unsafe_allow_html=True)

            st.divider()
            epi = f"""DAHİLİYE KLİNİK KARAR ROBOTU\n---------------------------\nPROTOKOL: {p_no}\nHASTA CİNSİYETİ: {cinsiyet}\nTARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}\nLAB: Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}\nGCS: {gcs_skor}, Wells: {wells_score}\neGFR: {egfr} ml/dk\n\nBELİRTİLER:\n{", ".join(b)}\n\nÖN TANI LİSTESİ:\n{chr(10).join([f"- {x['ad']} (%{x['puan']})" for x in results[:15]])}\n\nGELİŞTİRİCİ: İSMAİL ORHAN\n---------------------------"""
            st.markdown(f"<pre style='background:white; padding:40px; border-radius:45px; border:10px solid #DC2626; color:#000; font-size:14px; white-space: pre-wrap;'>{epi}</pre>", unsafe_allow_html=True)
            st.download_button("📥 Epikrizi İndir", epi, file_name=f"{p_no}_V30.txt")

st.markdown("---")
st.caption("GELİŞTİRİCİ: İSMAİL ORHAN GEMLİK 2026")
