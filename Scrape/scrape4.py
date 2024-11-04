from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Base URL for Flipkart's search page, excluding the `page` parameter
base_url = 'https://www.flipkart.com/search?p%5B%5D=facets.brand%255B%255D%3DSamsung&sid=tyy%2F4io&sort=recency_desc&wid=1.productCard.PMU_V2_1&page='

# List to store all products across pages
all_products = []

# Loop through a specific number of pages
for page in range(10, 11):  # show example(1-9 page)
    url = f"{base_url}{page}"
    driver.get(url)

    # Allow the page to load
    time.sleep(5)

    # Scroll to load all products on the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new products to load

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Exit if no more products are loaded
        last_height = new_height

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', class_='tUxRFH')  # Adjust this class if it differs

    # Extract product information
    for product in products:
        title_tag = product.find('div', class_="KzDlHZ")  # Adjust this class if it differs
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        
        og_price_tag = product.find('div', class_="yRaY8j")
        og_price = og_price_tag.get_text(strip=True).replace('₹', '').strip() if og_price_tag else "00"
        
        dis_price_tag = product.find('div', class_="Nx9bqj")
        discount_price = dis_price_tag.get_text(strip=True).replace('₹', '').strip() if dis_price_tag else "00"
        
        percent_tag = product.find('div', class_="UkUFwK")
        percent = percent_tag.get_text(strip=True) if percent_tag else "00"
        
        rating_tag = product.find('div', class_="XQDdHH")
        rating = rating_tag.get_text(strip=True) if rating_tag else "00"
        
        customer_tag = product.find('span', class_="Wphh3N")
        customer = customer_tag.get_text(strip=True) if customer_tag else "00"

        # Append product details to the list
        all_products.append({
            "Mobile Name": title,
            "Discount Price": discount_price,
            "Original Price": og_price,
            "Percent": percent,
            "Rating": rating,
            "Customer": customer
        })

# Create a DataFrame to save the data
df = pd.DataFrame(all_products)

# Save the DataFrame to a CSV file
df.to_csv("Samsung_Phone2.csv", index=False)
print("Product details have been saved to 'Samsung_Phone.csv'")

# Close the browser
driver.quit()
