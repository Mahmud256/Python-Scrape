import pandas as pd
import json

# Load the CSV file
df = pd.read_csv("Tv.csv")

# Convert the DataFrame to JSON as a string
json_str = df.to_json(orient="records", indent=4)

# Remove escaping of slashes
json_str = json_str.replace("\\/", "/")

# Save the modified JSON string to a file
with open("Tv.json", "w") as json_file:
    json_file.write(json_str)

print("CSV file has been converted to JSON and saved as 'Tv.json'")
