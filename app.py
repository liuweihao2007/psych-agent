import gradio as gr
from agent import agent_chat

def chat(message, history):
    return agent_chat(message, history)

demo = gr.ChatInterface(
    fn=chat,
    title="心理支持助手",
    description="输入感受，我会调用工具帮你记录和管理。高风险请拨12356。"
)
demo.launch(inbrowser=True)