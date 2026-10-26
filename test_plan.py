from tools import save_plan, get_plans, update_plan, assess_risk

print(save_plan("u1", "睡眠计划", "1.早睡;2.冥想"))
print(get_plans("u1"))
print(update_plan(1, "1.早睡;2.冥想;3.不看手机"))
print(get_plans("u1"))
print(assess_risk("我不想活了"))