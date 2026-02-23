from datetime import datetime, timedelta

today = datetime.today()

print((today - timedelta(days=1)).date())
print(today.date())
print((today + timedelta(days=1)).date())