from base_schema import fields
import time
from playwright.async_api import Playwright


class Execute():
    def __init__(self):
        self._data = fields

    async def setBrowser(self, playwright : Playwright):
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = await chromium.launch(headless=False)
        return browser


    async def run(self, playwright: Playwright, url: str):
        browser = await self.setBrowser(playwright)
        page = await browser.new_page()
        await page.goto(url)
        time.sleep(5)
        await self.getData(page, url)
        await browser.close()
        return self._data


    async def getData(self, page, url: str):
        self._data['url'] = url
        self._data['title'] = await self.getTitle(page)


    async def getTitle(self, page):
        titleElement = page.locator('div.HomePageSearchContainer_homePageSearchContainer_heading__DhWmd')
        title = await titleElement.text_content()
        return title
