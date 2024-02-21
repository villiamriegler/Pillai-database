import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer

from os.path import isdir, join
from os import listdir, walk

from json import load

from tqdm import tqdm

class MedicalDataset(Dataset):
    def _get_texts(self, key_page, key_value):
        texts = []
        RELATIVE_PATH = "../scrapers/data/products"

        if not isdir(RELATIVE_PATH):
            raise LookupError(f"Data path can't be found in: {RELATIVE_PATH}")

        filenames = listdir(RELATIVE_PATH)
        print(f"Reading files with key={key_page}:{key_value}")
        for file in tqdm(filenames):
            with open(join(RELATIVE_PATH, file), "r") as json_file:
                content = load(json_file)

            if key_page not in content.keys() or key_value not in content[key_page].keys(): continue

            texts.append(content[key_page][key_value])

        return texts


    def __init__(self, data_page, data_key, model_ID="mistralai/Mixtral-8x7B-Instruct-v0.1"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_ID)

        self.data = self.tokenizer(
            self._get_texts(data_page, data_key),
            return_tensors="pt"
        )

        print(self.data)


a = MedicalDataset("bipacksedel", "pregnancy")

        
