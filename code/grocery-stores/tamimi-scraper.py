from playwright.sync_api import sync_playwright
from datetime import date
import pandas as pd

def write_to_csv(products, prices, dates):
    data = {"date": dates, "name": products, "price": prices}
    df = pd.DataFrame(data)
    df.to_csv('tamimi-data.csv')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page()
    keyword = "pasta"
    url = "https://shop.tamimimarkets.com/en/search?query="+keyword
    page.goto(url, wait_until="domcontentloaded")
    # Wait for results to load
    page.get_by_test_id("product-collection").wait_for()
    # Find the description (name and price)
    product_names = page.locator('css=[class^=Product__StyledTitle]').all_text_contents()
    product_prices = page.locator('css=[class^=Product__PriceAndSaveButton]').locator('span span').all_text_contents()
    
    # remove whitespaces from text
    prices_cleaned = []
    for p in product_prices:
        parts = p.split('SAR')
        if len(parts) == 2:
            price = parts[1].strip()
            prices_cleaned.append(price)
    
    browser.close()
    today = date.today().strftime("%d/%m/%Y")
    date_values =[today] * len(prices_cleaned)

    write_to_csv(product_names, prices_cleaned, date_values)

    
