import pandas as pd

# Load the CSV file
df = pd.read_csv("Samsung_Phone_37.csv")

# Convert the DataFrame to JSON and save it to a file
df.to_json("Samsung_Phone_37.json", orient="records", indent=4)
print("CSV file has been converted to JSON and saved as 'Samsung_Phone_37.json'")
