import json, os, time
from llm_config import client
from tools import (save_mood, query_mood, save_plan, get_plans,
                   update_plan, assess_risk, search_knowledge)

# 把工具函数和名字对应起来，方便AI调用
tools_map = {
    "save_mood": save_mood, "query_mood": query_mood,
    "save_plan": save_plan, "get_plans": get_plans,
    "update_plan": update_plan, "assess_risk": assess_risk,
    "search_knowledge": search_knowledge,
}

# 告诉AI有哪些工具可用，以及每个工具需要什么参数
tools_schema = [
    {"type":"function","function":{"name":"save_mood","description":"保存情绪记录","parameters":{"type":"object","properties":{"mood":{"type":"string"},"score":{"type":"integer"},"note":{"type":"string"}},"required":["mood","score"]}}},
    {"type":"function","function":{"name":"query_mood","description":"查询情绪记录","parameters":{"type":"object","properties":{}}}},
    {"type":"function","function":{"name":"save_plan","description":"保存行动计划","parameters":{"type":"object","properties":{"title":{"type":"string"},"steps":{"type":"string"}},"required":["title","steps"]}}},
    {"type":"function","function":{"name":"get_plans","description":"查询计划","parameters":{"type":"object","properties":{}}}},
    {"type":"function","function":{"name":"update_plan","description":"修改计划","parameters":{"type":"object","properties":{"plan_id":{"type":"integer"},"new_steps":{"type":"string"}},"required":["plan_id","new_steps"]}}},
    {"type":"function","function":{"name":"assess_risk","description":"检测心理危机风险","parameters":{"type":"object","properties":{"text":{"type":"string"}},"required":["text"]}}},
    {"type":"function","function":{"name":"search_knowledge","description":"检索心理知识","parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}}},
]

os.makedirs("logs", exist_ok=True)

# 记录每一次工具调用的日志
def log_tool(name, args, result, status="success", latency=0):
    with open("logs/tool_calls.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"tool": name, "args": args, "result": str(result)[:200], "status": status, "latency_ms": latency}, ensure_ascii=False) + "\n")

SYSTEM = "你是心理支持助手。根据用户需求调用工具。高风险时引导拨打12356。用户ID固定为u1。"

def agent_chat(user_input, history=None):
    try:
        messages = [{"role":"system","content":SYSTEM}]
        if history:
            for h in history:
                if isinstance(h, dict):
                    messages.append({"role": h["role"], "content": h["content"]})
                else:
                    messages.append({"role":"user","content":h[0]})
                    messages.append({"role":"assistant","content":h[1]})
        messages.append({"role":"user","content":user_input})

        # 最多循环5次，防止AI死循环
        for _ in range(5):
            resp = client.chat.completions.create(
                model="glm-4-flash", messages=messages,
                tools=tools_schema, temperature=0.3
            )
            msg = resp.choices[0].message
            messages.append(msg)

            # 如果AI没调用工具，直接返回它的回复
            if not msg.tool_calls:
                return msg.content

            # 如果AI调用了工具，挨个执行
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                # 自动补上用户ID，不用AI传
                if name in ["save_mood","query_mood","save_plan","get_plans"]:
                    args["user_id"] = "u1"
                
                # 执行工具，并记录耗时和状态
                start = time.time()
                try:
                    result = tools_map[name](**args)
                    log_tool(name, args, result, "success", int((time.time()-start)*1000))
                except Exception as e:
                    log_tool(name, args, str(e), "fail", int((time.time()-start)*1000))
                    result = f"工具失败：{e}"
                
                # 把工具的执行结果塞回给AI，让它继续生成最终回复
                messages.append({"role":"tool","tool_call_id": tc.id,"content": str(result)})
        
        return "处理超时，请再说一次。"
    except Exception as e:
        # 记录整体崩溃日志，保证程序不闪退
        with open("logs/failures.log", "a", encoding="utf-8") as f:
            f.write(f"{user_input} 失败: {e}\n")
        return "抱歉，系统刚才出了点问题，请再说一次。"