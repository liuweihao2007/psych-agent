import pandas as pd
import json
import os

df = pd.read_csv("data/processed/knowledge.csv")
texts = df["knowledge"].tolist()

# 直接存成一个简单的 JSON 文件，不用向量数据库了
os.makedirs("chroma_db", exist_ok=True)
with open("chroma_db/data.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False)

print("数据存储完成，共", len(texts), "条")