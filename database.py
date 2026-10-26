import sqlite3

def init_db():
    conn = sqlite3.connect("psych_agent.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS moods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, mood TEXT, score INTEGER, note TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, title TEXT, steps TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()
    print("数据库初始化完成")

if __name__ == "__main__":
    init_db()