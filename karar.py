import streamlit as st
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="DAHİLİYE ROBOTU", page_icon="💊", layout="wide")

# --- API KEY ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("GEMINI_API_KEY bulunamadı!")

# --- HEADER ---
st.title("🏥 Dahiliye Klinik Karar Robotu")

# --- SIDEBAR ---
with st.sidebar:
    yas = st.number_input("Yaş", 0, 120, 45)
    cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
    hb = st.number_input("Hb", 3.0, 25.0, 14.0)
    wbc = st.number_input("WBC", 0, 500000, 8500)
    plt = st.number_input("PLT", 0, 2000000, 245000)
    kre = st.number_input("Kreatinin", 0.1, 20.0, 1.1)

# --- SEMPTOM ---
b = st.multiselect("Semptomlar", [
    "Göğüs Ağrısı", "Nefes Darlığı", "Ateş (>38)", "Hipotansiyon",
    "Taşikardi", "Konfüzyon", "Öksürük"
])

# --- IMAGE ---
up_file = st.file_uploader("Görüntü yükle", type=["jpg", "png", "jpeg"])

# --- ANALYZE ---
if st.button("🚀 ANALİZ"):
    if not b:
        st.error("Semptom seç!")
    else:
        st.subheader("🤖 AI Klinik Yorum")

        try:
            # ✅ MODEL FALLBACK
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
            except:
                model = genai.GenerativeModel("gemini-1.5-pro-latest")

            # ✅ GELİŞMİŞ PROMPT
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

            # ✅ GÖRSEL DESTEK
            if up_file:
                image_bytes = up_file.getvalue()

                ai_res = model.generate_content({
                    "parts": [
                        {"text": vaka_data},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_bytes
                            }
                        }
                    ]
                })
            else:
                ai_res = model.generate_content(vaka_data)

            st.success("Analiz tamamlandı")
            st.write(ai_res.text)

        except Exception as e:
            st.error(f"Hata: {e}")

# --- EPİKRİZ ---
st.divider()

epi = f"""
DAHİLİYE RAPORU
------------------------
Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Hasta: {yas} / {cinsiyet}

LAB:
Hb {hb}, WBC {wbc}, PLT {plt}, Kre {kre}

Semptomlar:
{b}
"""

st.download_button("📥 Epikriz indir", epi)
