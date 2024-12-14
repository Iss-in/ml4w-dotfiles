import datetime

date = datetime.datetime.now()
new_date = date - datetime.timedelta(0,3) # days, seconds, then other fields.
minutes = int(new_date.strftime("%M"))%3
seconds = new_date.strftime("%S")

# old_minutes = int(date.strftime("%M"))%3
# old_seconds = date.strftime("%S")

print(f"{minutes}:{seconds}")
# print(f"{old_minutes}:{old_seconds}")
