from datetime import datetime

today = datetime.today()

date1 = datetime.strptime(input(),"%Y-%m-%d")
date2 = datetime.strptime(input(),"%Y-%m-%d")
diff_seconds = (date2 - date1).total_seconds()
print(date1.date())
print(date2.date())
print(f"{diff_seconds:.0f}")

