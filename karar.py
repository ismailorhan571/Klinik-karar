import streamlit as st
from datetime import datetime
from PIL import Image
from google import genai   # ✅ YENİ SDK

# --- CONFIG ---
st.set_page_config(page_title="İSMAİL ORHAN DAHİLİYE ROBOTU", page_icon="💊", layout="wide")

# --- API ---
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Secrets'da GEMINI_API_KEY yok!")

# --- HEADER ---
st.title("🏥 DAHİLİYE KLİNİK KARAR ROBOTU")

# --- SIDEBAR ---
with st.sidebar:
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.radio("Cinsiyet", ["Erkek", "Kadın"])
    hb = st.number_input("Hb", 3.0, 25.0, 14.0)
    wbc = st.number_input("WBC", 0, 500000, 8500)
    plt = st.number_input("PLT", 0, 2000000, 245000)
    kre = st.number_input("Kreatinin", 0.1, 20.0, 1.1)

# --- SEMPTOM ---
b = st.multiselect("Semptomlar", [
    "Göğüs Ağrısı", "Nefes Darlığı", "Ateş (>38)",
    "Hipotansiyon", "Taşikardi", "Konfüzyon", "Öksürük"
])

# --- IMAGE ---
up_file = st.file_uploader("Görüntü yükle", type=["jpg", "png", "jpeg"])

# --- ANALİZ ---
if st.button("🚀 ANALİZİ BAŞLAT"):

    if not b:
        st.error("Semptom seç!")
    else:
        st.markdown("### 📝 EPİKRİZ VE AI ANALİZİ")
        st.info("🤖 Gemini AI Klinik Yorumu:")

        try:
            vaka_data = f"""
            SEN BİR DAHİLİYE UZMANISIN.

            HASTA:
            Yaş: {yas}
            Cinsiyet: {cinsiyet}

            LAB:
            Hb: {hb}, WBC: {wbc}, PLT: {plt}, Kreatinin: {kre}

            SEMPTOMLAR:
            {b}

            GÖREV:
            - En olası 3 tanı
            - Risk seviyesi (Düşük/Orta/Yüksek)
            - Mortalitenin % tahmini
            - Acil yapılması gerekenler
            - Kritik uyarılar

            KISA ve NET yaz.
            """

            # ✅ GÖRSEL VARSA
            if up_file:
                img = Image.open(up_file)

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[vaka_data, img]
                )
            else:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=vaka_data
                )

            st.success("Analiz tamamlandı")
            st.markdown(
                f"<div style='background:#f0f2f6; padding:20px; border-radius:15px;'>"
                f"{response.text}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"AI Hatası: {e}")

# --- EPİKRİZ ---
st.divider()

epi = f"""
DAHİLİYE KLİNİK RAPORU
---------------------------
TARİH: {datetime.now().strftime('%d/%m/%Y %H:%M')}
HASTA: {yas} / {cinsiyet}

LAB:
Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}

SEMPTOMLAR:
{b}
"""

st.download_button("📥 Epikriz indir", epi)
