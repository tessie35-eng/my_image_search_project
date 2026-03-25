import torch
from transformers import AutoProcessor, CLIPModel, AutoTokenizer
from PIL import Image
import pandas as pd
from datasets import load_dataset
import faiss
import numpy as np

dataset = load_dataset("Donghyun99/Stanford-Cars")

import os

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_features(example):
    inputs = processor(images=example["image"], return_tensors="pt")

    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
        features = outputs.pooler_output
    embedding = features.detach().cpu().numpy().astype("float32")
    example["embedding"] = embedding[0]
    return example

# image_features = dataset["train"].map(extract_features)

# embeddings = image_features["embedding"]
# embeddings = np.array(embeddings).astype("float32")
# print(embeddings.shape)
#np.save("embeddings.npy", embeddings)
embeddings = np.load("embeddings.npy")
print(embeddings.shape)
dim = embeddings.shape[1]
print(dim)
d= dim #dimension des embeddings

faiss.normalize_L2(embeddings)
index = faiss.IndexFlatL2(d)
print(f"Index entraîné: {index.is_trained}")
index.add(embeddings)
#faiss.write_index(index, "index_standford_cars.faiss")

#index.add(embeddings)

#index = faiss.read_index("index_standford_cars.faiss")