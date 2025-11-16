"""
Library yang digunakan untuk membuat streamlit, memanggil path model
load fungsi dari file preprocessing.py
"""
import re
import streamlit as st
import joblib
from sentence_transformers import SentenceTransformer
from preprocessing import load_slang_dict, preprocessing_text


st.set_page_config(page_title="Analisis Sentimen Produk Tokopedia", layout="centered")

# Model dan kamus hanya diload sekali saja
@st.cache_resource
def load_models_and_utils():
    """
    Load model classifier, model sentence_transformer, 
    kamus slang, dan label invers 
    """
    # load model sentence_transfomer
    encoder = SentenceTransformer("Model/sentence_transformer")

    # load model classifier
    classifier = joblib.load("Model/model_classifier.joblib")

    # Load kamus slang
    kamus_baku = load_slang_dict()
    kamus_baku = {re.escape(k): v for k, v in kamus_baku.items()}

    # Labeling inverse
    label_map = {
        2: "positif",
        1: "netral",
        0: "negatif"
    }

    return encoder, classifier, kamus_baku, label_map

# Panggil fungsi
encoder, classifier, kamus_baku, label_map = load_models_and_utils()

# Set Streamlit
st.title("🤔 Analisis Sentimen Produk Tokopedia")
st.markdown("Masukkan ulasan produk (bahasa indonesia) untuk memprediksi sentimennya")

# Area input teks
text_input = st.text_area("Masukkan ulasan anda: ",
                          height=150,
                          placeholder="Contoh: Barang bagus, pengirimannya cepat sekali")

# Tombol prediksi
if st.button("Prediksi", type='primary'):
    if text_input:
        clean_text = preprocessing_text(text_input, kamus_baku)

        if not clean_text:
            st.warning("Teks input tidak mengandung kata yang valid")
        else:
            # Embedding kalimat input
            embedding = encoder.encode([clean_text])

            # Prediksi kalimat
            prediction = classifier.predict(embedding)[0]

            # Label hasil prediksi
            prediction_str = label_map.get(prediction, "Tidak Dikenali")

            # Hasil
            if prediction_str == "positif":
                st.success(f"**Hasil prediksi: {prediction_str.upper()}** (Kode: {prediction})")
            elif prediction_str == "negatif":
                st.error(f"**Hasil prediksi: {prediction_str.upper()} (Kode: {prediction})")
            else:
                st.info(f"**Hasil Prediksi: {prediction_str.upper()} (Kode: {prediction})")

            with st.expander("Proses"):
                st.write(f"Teks Awal: {text_input}")
                st.write(f"Teks Akhir: {clean_text}")
    else:
        st.warning("Masukkan teks review terlebih dahulu!")
