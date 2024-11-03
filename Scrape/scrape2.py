from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define the URL for the course page
category = 'fresh-fruit'
url = f'https://chaldal.com/{category}'
driver.get(url)

# Allow the page to load
time.sleep(5)

# Scroll to load more products
last_height = driver.execute_script("return document.body.scrollHeight")
all_products = []

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new products to load

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Exit if no more products are loaded
    last_height = new_height

# Now you can scrape the products
soup = BeautifulSoup(driver.page_source, 'html.parser')
products = soup.find_all('div', class_='product')  # Adjust this class if it differs

for product in products:
    title_tag = product.find('div', class_="name")  # Adjust this class if it differs
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    dis_price_tag = product.find('div', class_="discountedPrice")
    discount_price = dis_price_tag.get_text(strip=True).replace('৳', '').strip() if dis_price_tag else "00"

    og_price_tag = product.find('div', class_="price")
    og_price = og_price_tag.get_text(strip=True).replace('৳', '').strip() if og_price_tag else "Free"

    # Append product details to the list
    all_products.append({"Product Title": title, "Discount_price": discount_price, "Original_price": og_price})

# Create a DataFrame to save the data 
df = pd.DataFrame(all_products)

# Save the DataFrame to a CSV file
df.to_csv("fruit_products_details.csv", index=False)
print("Product details have been saved to 'products_details.csv'")

# Close the browser
driver.quit()
