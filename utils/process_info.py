import csv
from datetime import datetime

def process_info(file_name):
  with open(file_name, 'r') as file:
    reader = csv.DictReader(file)
    conversations = []
    last_date = None
    for row in reader:
      time_string = row['Date'].replace('p.m.', 'PM').replace('a.m.', 'AM')
      datetime_object = datetime.strptime(time_string, '%d/%m/%Y %I:%M%p')
      if last_date is None:
        last_date = datetime_object
        storage = [row]
      else:
        difference = (datetime_object - last_date).total_seconds() // 3600
        if difference > 5:
          #means that have passed 5 hours since the last message, so it's a new conversation
          #have to save the whole conversation
          last_date = datetime_object
          if len(str(storage)) < 3500:
            conversations.append(storage)
          storage = [row]
        else:
          last_date = datetime_object
          storage.append(row)

  return conversations