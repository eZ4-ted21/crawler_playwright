from playwright.sync_api import Playwright
from base_schema import fields


class Execute():
    def __init__(self):
        self._data = fields

    def setBrowser(self, playwright: Playwright):
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(headless=False)
        return browser

    def run(self, playwright: Playwright, url : str):
        browser = self.setBrowser(playwright)
        page = browser.new_page()
        page.goto(url)
        self.get_data(page, url)
        browser.close()
        return self._data
    
    def get_data(self, page, url: str):
        self._data['url'] = url
        self._data['title'] = self.getTitle(page)
    
    def getTitle(self, page):
        titleElement = page.locator('div.HomePageSearchContainer_homePageSearchContainer_heading__DhWmd')
        return titleElement.text_content()