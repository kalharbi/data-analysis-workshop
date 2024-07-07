import jupyterlab
import pandas as pd
import matplotlib.pyplot as plt
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('http://google.com')
    print(page.title())
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
