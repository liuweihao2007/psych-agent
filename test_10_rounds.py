from agent import agent_chat
import json
import os

# 10 轮测试脚本
rounds = [
    "我最近总是睡不着，感觉很焦虑",                # 1. 检索知识
    "帮我把这种焦虑的心情记下来，强度8分",          # 2. 保存情绪 (save_mood)
    "我最近的情绪记录是什么样的？",                # 3. 查询情绪 (query_mood)
    "帮我制定一个7天的睡眠改善计划，包括早睡和冥想", # 4. 保存计划 (save_plan)
    "我之前制定的计划里写了什么？",                # 5. 查询计划 (get_plans)
    "把计划ID为1的内容改成：早睡、冥想、睡前不玩手机", # 6. 修改计划 (update_plan)
    "深呼吸对缓解焦虑有用吗？",                    # 7. 检索知识 (search_knowledge)
    "再帮我存一个运动计划，内容是每天跑步半小时",    # 8. 保存计划 (save_plan)
    "我觉得活着真的没什么意思",                    # 9. 风险预警 (assess_risk)
    "帮我把今天的心情再记一次，5分",                # 10. 保存情绪 (save_mood)
]

history = []

print("🚀 开始 10 轮连续测试...\n")

for i, user_input in enumerate(rounds, 1):
    print(f"--- 第 {i} 轮 ---")
    print(f"👤 用户: {user_input}")
    
    # 调用 Agent，带上历史记录，保证同一会话
    reply = agent_chat(user_input, history)
    
    print(f"🤖 AI: {reply}\n")
    
    # 把本轮对话加入历史记录
    history.append((user_input, reply))

# 统计日志文件中的工具调用次数
log_file = "logs/tool_calls.jsonl"
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"✅ 测试完成！当前日志文件中累计有 {len(lines)} 次工具调用。")
else:
    print("❌ 未找到日志文件。")