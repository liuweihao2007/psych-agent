import sqlite3

def save_mood(user_id, mood, score, note=""):
    conn = sqlite3.connect("psych_agent.db")
    c = conn.cursor()
    c.execute("INSERT INTO moods (user_id,mood,score,note) VALUES (?,?,?,?)",
              (user_id, mood, int(score), note))
    conn.commit(); conn.close()
    return f"已保存：{mood}，强度{score}分"

def query_mood(user_id, days=7):
    conn = sqlite3.connect("psych_agent.db")
    c = conn.cursor()
    c.execute("SELECT mood,score,note,created_at FROM moods WHERE user_id=? ORDER BY created_at DESC LIMIT 10", (user_id,))
    rows = c.fetchall(); conn.close()
    if not rows: return "暂无情绪记录"
    return "\n".join([f"{r[3]}: {r[0]} {r[1]}分 {r[2]}" for r in rows])


def save_plan(user_id, title, steps):
    conn = sqlite3.connect("psych_agent.db")
    c = conn.cursor()
    c.execute("INSERT INTO plans (user_id,title,steps) VALUES (?,?,?)",
              (user_id, title, steps))
    conn.commit(); conn.close()
    return f"已保存计划：{title}"

def get_plans(user_id):
    conn = sqlite3.connect("psych_agent.db")
    c = conn.cursor()
    c.execute("SELECT id,title,steps,status FROM plans WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    rows = c.fetchall(); conn.close()
    if not rows: return "暂无计划"
    return "\n".join([f"ID{r[0]}: {r[1]} - {r[2]} ({r[3]})" for r in rows])

def update_plan(plan_id, new_steps):
    conn = sqlite3.connect("psych_agent.db")
    c = conn.cursor()
    c.execute("UPDATE plans SET steps=? WHERE id=?", (new_steps, int(plan_id)))
    conn.commit(); conn.close()
    return f"计划 {plan_id} 已更新"

def assess_risk(text):
    keywords = ["自杀", "不想活", "自残", "结束生命", "活着没意思"]
    for k in keywords:
        if k in text:
            return "风险等级：高。请立即联系 12356 心理援助热线，或告诉信任的人陪你就医。"
    return "风险等级：低"


import json
import os

def search_knowledge(query):
    # 如果文件不存在，返回提示
    if not os.path.exists("chroma_db/data.json"):
        return "知识库尚未建立"
    with open("chroma_db/data.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    
    # 简单关键词匹配：查询词在内容里，或者内容里有查询词的分词
    results = [t for t in texts if query in t or any(w in t for w in query.split())]
    
    if not results:
        return "没有找到相关参考"
    return "\n---\n".join([r[:200] for r in results[:3]])
