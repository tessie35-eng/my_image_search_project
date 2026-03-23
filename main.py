from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

from search_engine import ImageSearchEngine

app = FastAPI()

engine = ImageSearchEngine("index_standford_cars.faiss")


@app.post("/search")
async def search_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # distances, indices = engine.search(image)
    res = engine.search(image)

    return {
        "results": res
        # "indices": indices.tolist(),
        # "distances": distances.tolist()
    }