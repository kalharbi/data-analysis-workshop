from playwright.sync_api import sync_playwright
from datetime import date
import pandas as pd

def write_to_csv(products, prices, dates):
    data = {"date": dates, "name": products, "price": prices}
    df = pd.DataFrame(data)
    df.to_csv('danube-data.csv')


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    keyword = "pasta"
    page.goto("https://danube.sa/en/search?query="+keyword, wait_until="domcontentloaded")
    # Wait for the popup dialog with an id of store-selector
    page.locator("#store-selector").wait_for()
    # Find the button and click it
    page.locator(".d-store-selector__apply-btn").click()
    page.wait_for_load_state()

    page.locator(".d-search-page__results").wait_for()
    page.pause()
    products = page.locator(".product-box__name").all_inner_texts()
    prices = page.locator(".product-price__current-price").all_text_contents()

    pricesCleaned = []
    for p in prices:
        current_price = p.split('SAR')[1].strip()
        pricesCleaned.append(current_price)
    
    today = date.today().strftime("%d/%m/%Y")
    dateValues =[today] * len(pricesCleaned)
    write_to_csv(products, pricesCleaned, dateValues)



    browser.close()
