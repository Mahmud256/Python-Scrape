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
base_url = 'https://www.vertech.com.bd/category/laptop?page='

# List to store all product details
all_products = []

# Loop through the specified number of pages
for page in range(1, 11):  # Example: Scrape pages 1-9
    url = f"{base_url}{page}"
    driver.get(url)

    # Allow the page to load
    time.sleep(5)

    # Scroll to load all products on the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', class_='grid grid-cols-2 sm:grid-cols-3 2xl:grid-cols-4 3xl:grid-cols-5 gap-4 mt-4 lg:mt-8 print:mt-4 print:sm:grid-cols-5 print:gap-1')

    # Extract product information
    for product in products:
        # Extract product link
        link = product.find('a', href=True)['href'] if product.find('a', href=True) else None
        if link:
            # Make the link absolute if it's relative
            if not link.startswith("http"):
                link = "https://www.vertech.com.bd" + link
            
            try:
                # Open the product link in the browser
                driver.get(link)
                time.sleep(3)  # Wait for the product page to load

                # Parse the product page
                product_soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Extract details
                title = product_soup.find('h1', class_="font-semibold text-base md:text-xl")
                title = title.get_text(strip=True) if title else "No Title"

                brand = product_soup.find('a', class_="hover:text-primary duration-300")
                brand = brand.get_text(strip=True) if brand else "No Title"

                description = product_soup.find('div', class_='decription-order-list')
                description = description.get_text(strip=True) if description else "N/A"

                current_price_tag = product_soup.find('span', class_='font-medium text-primary text-2xl')
                current_price = current_price_tag.get_text(strip=True) if current_price_tag else "N/A"


                category = product_soup.find('a', class_='hover:text-primary duration-300')
                category = category.get_text(strip=True) if category else "N/A"

                # Collect Multiple Photos
                
                # # Find the photos tag
                # photos_tags = product_soup.find_all("img", class_="image-gallery-image")  # Use find_all to get all images
                
                # # Extract the 'src' attributes from all photo tags
                # photos = [tag["src"] for tag in photos_tags if "src" in tag.attrs]
                
                # # If no photos are found, assign a default value
                # photos = photos if photos else ["No photos"]
                 
                
                # Collect Only One Photos
                # Find the photos tag (first image)
                photos_tag = product_soup.find("img", class_="image-gallery-image")
                
                # Extract the 'src' attribute if the tag exists
                # photos = photos_tag["src"] if photos_tag and "src" in photos_tag.attrs else "No photo"

                photos = [photos_tag["src"]] if photos_tag and "src" in photos_tag.attrs else ["No photo"]
                
                # If no photos are found, assign a default value
                photos = photos if photos else ["No photos"]



                # Append details to the list
                all_products.append({
                    "name": title,
                    "brand": brand,
                    "description": description,
                    "price": current_price,
                    "category": category,
                    # "photos": ", ".join(photos), # Collect Multiple Photos
                    "photos": ", ".join(photos) # Collect Only One Photos
                    # "link": link
                })

                # Go back to the main page
                driver.back()
                time.sleep(3)  # Wait for the main page to reload

            except Exception as e:
                print(f"Error processing product: {e}")
                continue

# Create a DataFrame to save the data
df = pd.DataFrame(all_products)

# Save the DataFrame to a CSV file
df.to_csv("Laptop.csv", index=False)
print("Product details have been saved to 'Laptop.csv'")

# Close the browser
driver.quit()
