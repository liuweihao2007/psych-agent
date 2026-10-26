import json

with open("chroma_db/data.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

query = "焦虑失眠怎么办"
# 找出包含“焦虑”或“失眠”的句子
results = [t for t in texts if "焦虑" in t or "失眠" in t]

print("检索到的相关内容：")
if results:
    for doc in results[:3]:
        print(doc[:200])
        print("---")
else:
    print("没有找到相关内容")