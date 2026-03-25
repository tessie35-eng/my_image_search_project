import torch
import numpy as np
import faiss
from transformers import AutoProcessor, CLIPModel, AutoTokenizer
from datasets import load_dataset
import base64
import io

class ImageSearchEngine:
    def __init__(self, index_path):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.index = faiss.read_index(index_path)
        #self.dataset = load_dataset("Donghyun99/Stanford-Cars")["train"]
        #self.tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-base-patch32")

    def encode_image(self, image):
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs)
            features = outputs.pooler_output

        embedding = features.detach().cpu().numpy().astype("float32")
        #embedding = embedding[0]
        embedding = np.array(embedding).astype("float32")
        print(embedding.shape)
        faiss.normalize_L2(embedding)

        return embedding

    # def image_to_base64(self, img):
    #     # sécurité : convertir en RGB
    #     img = img.convert("RGB")
    #
    #     buffer = io.BytesIO()
    #     img.save(buffer, format="JPEG")
    #
    #     return base64.b64encode(buffer.read()).decode("utf-8")

    def search(self, image, k=5):
        query = self.encode_image(image)
        print("Index total vectors:", self.index.ntotal)
        print("Index dimension:", self.index.d)
        print("Query shape:", query.shape)
        distances, indices = self.index.search(query, k)

        results = []
        for i, d in zip(indices[0], distances[0]):
            #img = self.dataset[int(i)]["image"]
            #print(img)
            print(i)
            print(d)
            results.append({
                "index": int(i),
                "distance": float(d),
                "image": f"/images/{i}.jpg"
            })
            print(results)

        return results



        # return distances, indices