from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Base URL for the search page
base_url = 'https://www.startech.com.bd/television-shop?page='

# List to store all product details
all_products = []

# Loop through a specific number of pages
for page in range(1, 10):  # Example: pages 1 to 9
    url = f"{base_url}{page}"
    driver.get(url)

    # Allow the page to load
    time.sleep(5)

    # Scroll to load all products on the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new products to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', class_='p-item')  # Adjusted class for product items

    # Extract product links
    for product in products:
        link = product.find('a', href=True)
        if link:
            product_url = link['href']
            if not product_url.startswith("http"):
                product_url = "https://www.startech.com.bd" + product_url

            try:
                # Open the product link
                driver.get(product_url)
                time.sleep(3)  # Allow the product page to load

                # Parse the product page
                product_soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Extract details
                title = product_soup.find('h1', class_="product-name")
                title = title.get_text(strip=True) if title else "No Title"

                brand = product_soup.find('td', class_="product-info-data product-brand")
                brand = brand.get_text(strip=True) if brand else "No Brand"

                description_tag = product_soup.find('p')
                description = description_tag.get_text(strip=True) if description_tag else "No Description"

                current_price_tag = product_soup.find('ins') or product_soup.find('td', class_='product-info-data product-price')
                current_price = current_price_tag.get_text(strip=True) if current_price_tag else "N/A"

                photos_tag = product_soup.find("img", class_="main-img")
                photos = photos_tag["src"] if photos_tag and "src" in photos_tag.attrs else "No Photo"

                # Append details to the list
                all_products.append({
                    "name": title,
                    "brand": brand,
                    "description": description,
                    "price": current_price,
                    "category": "office equipment",
                    "photos": photos,
                    "link": product_url
                })

            except Exception as e:
                print(f"Error processing product {product_url}: {e}")
                continue

# Create a DataFrame to save the data
df = pd.DataFrame(all_products)

# Save the DataFrame to a CSV file
df.to_csv("Tv.csv", index=False)
print("Product details have been saved to 'Tv.csv'")

# Close the browser
driver.quit()
