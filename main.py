from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import io
import requests
from fastapi.staticfiles import StaticFiles
from search_engine import ImageSearchEngine
import os


app = FastAPI()

# Sert les images
images_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
print("Serving images from:", images_path)
app.mount("/images", StaticFiles(directory="images"), name="images")

engine = ImageSearchEngine("index_standford_cars.faiss")


@app.post("/search")
async def search_image(
    file: UploadFile = File(None),
    image_url: str = Form(None)):
    if file is None and image_url is None:
        return {"error": "Provide either a file or an image URL"}

    # Cas 1 : image upload
    if file is not None:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Cas 2 : image URL
    else:
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
        except:
            return {"error": "Invalid image URL"}

    # distances, indices = engine.search(image)
    res = engine.search(image)

    return {
        "results": res
        # "indices": indices.tolist(),
        # "distances": distances.tolist()
    }

