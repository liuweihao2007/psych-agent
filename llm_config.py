import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 专门针对智谱 AI 的配置
client = OpenAI(
    api_key=os.getenv("ZHIPU_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)