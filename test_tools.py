from database import init_db
from tools import save_mood, query_mood

init_db()
print(save_mood("u1", "焦虑", 7, "睡不着"))
print(query_mood("u1"))