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
        # Get CSV file name from user input
        csv_file_name = csv_file_entry.get()

        if not csv_file_name:
            messagebox.showerror("Input Error", "Please enter a valid CSV file name.")
            return

        # Set up the Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Base URL for the products
        base_url = "https://www.shwapno.com/food?tags=66408497827cb85359666bcf"
        all_products = []

        # Open the URL
        driver.get(base_url)
        time.sleep(5)

        # Scroll to the bottom to load all products
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Parse the page source
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("div", class_="product-box")

        # Extract product details
        for product in products:
            title_tag = product.find("h2", class_="product-box-title")
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            og_price_tag = product.find("div", class_="product-price")
            og_price = (
                og_price_tag.find("span").get_text(strip=True).replace("৳", "").strip()
                if og_price_tag
                else "00"
            )

            all_products.append(
                {
                    "product name": title,
                    "original Price": og_price,
                    "category": "food",
                    "tags": "Bakery Products",
                }
            )

        # Save the data to CSV
        df = pd.DataFrame(all_products)
        csv_file_path = f"{csv_file_name}.csv"
        df.to_csv(csv_file_path, index=False)
        messagebox.showinfo(
            "Success", f"Product details have been saved to '{csv_file_path}'"
        )
        driver.quit()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid CSV file name.")
        return


# Setting up the Tkinter window
root = tk.Tk()
root.title("Swapno Bakery Product Scraper")
root.geometry("400x300")

# Label and entry for CSV file name
tk.Label(root, text="CSV File Name:").pack(pady=5)
csv_file_entry = tk.Entry(root)
csv_file_entry.pack()

# Button to start scraping
scrape_button = tk.Button(
    root, text="Scrape Swapno Bakery Product", command=scrape_flipkart
)
scrape_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
