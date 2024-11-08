import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_flipkart():
    try:
        # Get page range and CSV file name from user inputs
        start_page = int(start_page_entry.get())
        end_page = int(end_page_entry.get())
        csv_file_name = csv_file_entry.get()

        if start_page < 1 or end_page < start_page:
            messagebox.showerror("Input Error", "Please enter a valid page range.")
            return
        if not csv_file_name:
            messagebox.showerror("Input Error", "Please enter a valid CSV file name.")
            return

        # Set up the Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # base_url = 'https://www.flipkart.com/search?p%5B%5D=facets.brand%255B%255D%3DSamsung&sid=tyy%2F4io&sort=recency_desc&wid=1.productCard.PMU_V2_1&page='

        base_url = 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&page='
        all_products = []

        for page in range(start_page, end_page + 1):
            url = f"{base_url}{page}"
            driver.get(url)
            time.sleep(5)

            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.find_all('div', class_='tUxRFH')

            for product in products:
                title_tag = product.find('div', class_="KzDlHZ")
                title = title_tag.get_text(strip=True) if title_tag else "No Title"

                # Find the image tag
                image_tag = product.find('img', class_="DByuf4")
            
                # Get the image URL from the 'src' attribute
                image = image_tag['src'] if image_tag else "No Image"

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

                all_products.append({
                    "Mobile Name": title,
                    "Mobile Image": image,
                    "Discount Price": discount_price,
                    "Original Price": og_price,
                    "Percent": percent,
                    "Rating": rating,
                    "Customer": customer
                })

        df = pd.DataFrame(all_products)
        csv_file_path = f"{csv_file_name}.csv"  # Add .csv extension if not provided
        df.to_csv(csv_file_path, index=False)
        messagebox.showinfo("Success", f"Product details have been saved to '{csv_file_path}'")
        driver.quit()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers for page range.")
        return

# Setting up the Tkinter window
root = tk.Tk()
root.title("Flipkart Scraper")
root.geometry("400x300")

# Labels and entries for page range
tk.Label(root, text="Start Page:").pack(pady=5)
start_page_entry = tk.Entry(root)
start_page_entry.pack()

tk.Label(root, text="End Page:").pack(pady=5)
end_page_entry = tk.Entry(root)
end_page_entry.pack()

# Label and entry for CSV file name
tk.Label(root, text="CSV File Name:").pack(pady=5)
csv_file_entry = tk.Entry(root)
csv_file_entry.pack()

# Button to start scraping
scrape_button = tk.Button(root, text="Scrape Samsung Phones", command=scrape_flipkart)
scrape_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
