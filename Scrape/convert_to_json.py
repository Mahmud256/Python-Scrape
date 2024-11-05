# Create a DataFrame to save the data
df = pd.DataFrame(all_products)

# Save the DataFrame to a JSON file
df.to_json("Samsung_Phone_37.json", orient="records", indent=4)
print("Product details have been saved to 'Samsung_Phone_37.json'")

# Close the browser
driver.quit()
