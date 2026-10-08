import pandas as pd

csv  = "data.csv"

columns = ["booking_id", "audi_name" ,"user_name", "date", "start_time", "end_time"]

df = pd.DataFrame(columns = columns)

df.to_csv(csv , index = False)

