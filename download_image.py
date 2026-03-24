from datasets import load_dataset
import os

dataset = load_dataset("Donghyun99/Stanford-Cars")["train"]

os.makedirs("images", exist_ok=True)

for i, item in enumerate(dataset):
    item["image"].save(f"images/{i}.jpg")