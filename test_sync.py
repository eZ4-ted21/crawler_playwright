from playwright.sync_api import sync_playwright
from sync_strategy import Execute
from model import DataModel

url = "https://geeksforgeeks.org"
with sync_playwright() as playwright:
    _data = Execute().run(playwright, url)
    final_data = DataModel(
        url = _data['url'],
        title = _data['title']
    )
    print(final_data)
