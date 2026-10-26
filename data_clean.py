import pandas as pd
import re, os

os.makedirs("data/processed", exist_ok=True)

# 读取我们刚刚生成的模拟数据
df = pd.read_csv("data/raw/counselchat-data.csv")

# 删掉问题和回答里有空值的行
df = df.dropna(subset=["questionText", "answerText"])

# 清洗函数：把多余的空格、换行符都变成单个空格
def clean(t):
    return re.sub(r'\s+', ' ', str(t)).strip()

df["questionText"] = df["questionText"].apply(clean)
df["answerText"] = df["answerText"].apply(clean)

# 把问题和答案拼在一起，作为一条“知识”
df["knowledge"] = df["questionText"] + "\n" + df["answerText"]

# 过滤掉太短的（少于50个字符的没意义）
df = df[df["knowledge"].str.len() > 50]

# 保存到 processed 文件夹
df.to_csv("data/processed/knowledge.csv", index=False)
print("清洗完成，共", len(df), "条")