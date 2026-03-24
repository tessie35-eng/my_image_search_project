import streamlit as st
import requests

st.title("🔍 Recherche d'images (CLIP + FAISS)")

mode = st.radio("Choisir le type d'entrée", ["Upload", "URL"])

response = None

# 📁 Upload
if mode == "Upload":
    uploaded_file = st.file_uploader("Upload une image", type=["jpg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Image requête")

        response = requests.post(
            "http://localhost:8000/search",
            files={"file": uploaded_file.getvalue()}
        )

# 🌐 URL
else:
    image_url = st.text_input("Entrer une URL d'image")

    if image_url:
        st.image(image_url, caption="Image requête")

        response = requests.post(
            "http://localhost:8000/search",
            data={"image_url": image_url}
        )

# 🎯 Résultats
if response:
    results = response.json()["results"]

    st.subheader("Top 5 résultats")

    cols = st.columns(5)

    for i, res in enumerate(results):
        with cols[i]:
            st.image("http://localhost:8000" + res["image"])
            st.write(f"Score: {res['distance']:.3f}")