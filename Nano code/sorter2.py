import pandas as pd
import datetime

# Load the CSV file into a DataFrame
df = pd.read_csv('/var/www/output.csv')

# Convert the 'date' column to datetime format for accurate sorting
df['date'] = pd.to_datetime(df['date'], format='ISO8601')

# Sort the DataFrame by 'id' and 'date' in descending order
df_sorted = df.sort_values(by=['id', 'date'], ascending=[True, False])

# Drop duplicates keeping only the first occurrence (which is the most recent)
df_most_recent = df_sorted.drop_duplicates(subset='id', keep='first')
df_most_recent = df_most_recent.drop(columns=['date'])

date = datetime.datetime.now()
t = date.strftime('%Y-%m-%d %H:%M')

line = str(t) + ","


# Print each row one at a time
for index, row in df_most_recent.iterrows():
    temp = row.to_dict()["temperature"]
    line+=str(temp) + ","

# Print each row one at a time
for index, row in df_most_recent.iterrows():
    voltage = row.to_dict()["voltage"]
    line+=str(voltage) + ","
line = line[:-1]
line+= "\n"
with open("/var/www/graph2.csv", "a") as f:
    f.write(line)

with open("/var/www/graph2.csv", "r") as g:
    l = g.readlines()

trimmed = l[-2016:]
with open("/var/www/graph2.csv", "w") as f:
    for item in trimmed:
        f.write(item)
