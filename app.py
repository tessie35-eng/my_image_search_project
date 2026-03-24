import streamlit as st
import requests

st.title("🔍 Image Search (CLIP + FAISS)")

mode = st.radio("Select the input type", ["Upload", "URL"])

response = None

# 📁 Upload
if mode == "Upload":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Query Image")

        response = requests.post(
            "http://127.0.0.1:8000/search",
            files={"file": uploaded_file.getvalue()}
        )

# 🌐 URL
else:
    image_url = st.text_input("Input an image URL")

    if image_url:
        st.image(image_url, caption="Query Image")

        response = requests.post(
            "http://127.0.0.1:8000/search",
            data={"image_url": image_url}
        )

# 🎯 Résultats
if response:
    results = response.json()["results"]

    st.subheader("Top 5 results")

    cols = st.columns(5)

    for i, res in enumerate(results):
        with cols[i]:
            st.image("http://127.0.0.1:8000" + res["image"], width=150)
            st.write(f"Score: {res['distance']:.3f}")


