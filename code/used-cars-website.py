
from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime


def clean_prices(prices_list):    
    cleaned_prices = []
    for price in prices_list:
        # Remove the currency part "SAR"
        price_without_currency = price.replace(' SAR', '')
        # Remove commas
        price_without_commas = price_without_currency.replace(',', '')
        # Convert string to a float
        price_as_float = float(price_without_commas)
        cleaned_prices.append(price_as_float)
    return cleaned_prices


def clean_mileage(mileages_list):
    cleaned_mileages = []
    for mileage in mileages_list:
        # Remove the " km" part
        mileage_without_km = mileage.replace(' KM', '')
        # Remove commas
        mileage_without_commas = mileage_without_km.replace(',', '')
        # Convert string to a float
        mileage_as_float = float(mileage_without_commas)
        cleaned_mileages.append(mileage_as_float)
    return cleaned_mileages

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    url = "https://cpit490.gitlab.io/demos/online-store/"
    page.goto(url)
    cars = page.locator("h2.title").all_text_contents()
    mileages = page.locator("p.mileage").all_text_contents()
    prices = page.locator("p.price").all_text_contents()
    
    # clean the raw data
    cleaned_prices = clean_prices(prices)
    cleaned_mileages = clean_mileage(mileages)

    # Store the data in a data frame
    df = pd.DataFrame({
        'Car': cars,
        'Mileage': cleaned_mileages,
        'Price': cleaned_prices,
        'Date': [datetime.now().date()] * len(cars)  # Add current date for all entries
    })
    # Convert the DataFrame to a CSV file
    csv_file_path = 'cars_data.csv'
    df.to_csv(csv_file_path, index=False)
    browser.close()
    

