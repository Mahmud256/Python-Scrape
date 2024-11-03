import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL for the course page
url = 'https://ostad.app/course/laravel'

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the course title
    title_tag = soup.find('p', class_="text-h4 md:!text-h3 text-center md:!text-start text-ostad-black-100")  # Adjust this class if it differs
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    
    # Extract the course price
    price_tag = soup.find('p', class_="text-h3 text-ostad-black-100")  # Adjust if necessary
    price = price_tag.get_text(strip=True) if price_tag else "Free"  # Set to "Free" if no price

    # Print the extracted data
    print("Course Title:", title)
    print("Price:", price)
    
    # Create a DataFrame to save the data
    df = pd.DataFrame([{"Course Title": title, "Price": price}])
    
    # Save the DataFrame to a CSV file
    df.to_csv("single_course_details.csv", index=False)
    print("Course details have been saved to 'single_course_details.csv'")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
