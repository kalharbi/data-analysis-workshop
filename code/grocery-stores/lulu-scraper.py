from playwright.sync_api import sync_playwright
from datetime import date
import pandas as pd

def write_to_csv(products, prices, dates):
    data = {"date": dates, "name": products, "price": prices}
    df = pd.DataFrame(data)
    df.to_csv('lulu-data.csv')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    keyword = "pasta"
    url = "https://www.luluhypermarket.com/en-sa/search/?text="+keyword
    page.goto(url, wait_until="domcontentloaded")
    # Wait for results to load
    page.locator("#moreLoadedProducts").wait_for()
    # Find the description (name and price)
    product_items = page.locator('.product-desc').all_text_contents()
    names_cleaned = []
    prices_cleaned = []
    for p in product_items:
        parts = p.split('SAR')
        if len(parts) == 2:
            name = parts[0].strip()
            price = parts[1].strip()
            names_cleaned.append(name)
            prices_cleaned.append(price)
    
    page.screenshot(path='lulu-pasta-search.png', full_page=True)
    browser.close()
    today = date.today().strftime("%d/%m/%Y")
    date_values =[today] * len(prices_cleaned)

    write_to_csv(names_cleaned, prices_cleaned, date_values)

    
