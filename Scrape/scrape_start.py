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

        base_url = "https://www.startech.com.bd/component?page="
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

            soup = BeautifulSoup(driver.page_source, "html.parser")
            products = soup.find_all("div", class_="p-item-inner")

            for product in products:
                title_tag = product.find("h4", class_="p-item-name")
                title = title_tag.get_text(strip=True) if title_tag else "No Title"

                description_tag = product.find("div", class_="short-description")
                description = (
                    description_tag.get_text(strip=True)
                    if description_tag
                    else "No Description"
                )

                # Find the image tag
                image_tag = product.find("div", class_="p-item-img")

                # Check if the image container exists and then find the img tag within it
                if image_tag:
                    img_tag = image_tag.find("img")
                    image = img_tag["src"] if img_tag else "No Image"

                og_price_tag = product.find("div", class_="p-item-price")
                if og_price_tag:
                    og_price = (
                        og_price_tag.find("span")
                        .get_text(strip=True)
                        .replace("৳", "")
                        .strip()
                        if og_price_tag
                        else "00"
                    )
                # og_price = og_price_tag.get_text(strip=True).replace('৳', '').strip() if og_price_tag else "00"

                old_price_tag = product.find("span", class_="price-old")
                old_price = (
                    old_price_tag.get_text(strip=True).replace("৳", "").strip()
                    if old_price_tag
                    else "00"
                )

                all_products.append(
                    {
                        "product name": title,
                        "product image": image,
                        "product description": description,
                        "Old Price": old_price,
                        "Original Price": og_price,
                        # "Original Price2": og_price2,
                    }
                )

        df = pd.DataFrame(all_products)
        csv_file_path = f"{csv_file_name}.csv"  # Add .csv extension if not provided
        df.to_csv(csv_file_path, index=False)
        messagebox.showinfo(
            "Success", f"Product details have been saved to '{csv_file_path}'"
        )
        driver.quit()

    except ValueError:
        messagebox.showerror(
            "Input Error", "Please enter valid integers for page range."
        )
        return


# Setting up the Tkinter window
root = tk.Tk()
root.title("Startech Component Scraper")
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
scrape_button = tk.Button(
    root, text="Scrape Startech Component", command=scrape_flipkart
)
scrape_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
