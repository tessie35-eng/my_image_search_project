# CBIR Project (Content-Based Image Retrieval)

This project implements a Content-Based Image Retrieval engine using **CLIP embeddings** and **FAISS**.  
Users can search for images by **uploading** them or entering a **URL** via a **Streamlit** interface.

 ![Top 5 Example](img/ex2.png)

## Installation

1. Cloner the project :
  ```bash
  git clone https://github.com/tessie35-eng/my_image_search_project.git
  cd my_image_search_project
  ```
2. Create a new environment :
  ```
conda create -n cbir_env python=3.10
conda activate cbir_env
pip install -r requirements.txt
  ```
3. Download Dataset :
Dataset is from Hugging Face but you can download them
```
python download_image.py
```
5. Run FASTAPI :
```
uvicorn main:app --reload
```

6. Run the streamlit interface :
```
streamlit run app.py
```

  
   
