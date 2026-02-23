from datetime import datetime

today = datetime.today()

no_micro = today.replace(microsecond=0)
print(no_micro)
