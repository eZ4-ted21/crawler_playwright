import time
from model import DataModel
from playwright.async_api import Playwright


class Execute():
    def __init__(self):
        self._nextUrl = None
        self._rank = 1
        self._page = 1

    async def setBrowser(self, playwright : Playwright):
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = await chromium.launch(headless=False)
        return browser


    async def run(self, playwright: Playwright, url: str) ->list:
        dataForAllPages : list = []
        browser = await self.setBrowser(playwright)
        page = await browser.new_page()
        self._nextUrl = url
        while True:
            await page.goto(self._nextUrl)
            time.sleep(3)
            dataPerPage = await self.getDataPerPage(page)
            if not dataPerPage:
                break
            dataForAllPages.append({f'Page : {self._page}' : dataPerPage})
            self._page+=1
            self._nextUrl = await self.getNextUrl(page)
            if not self._nextUrl:
                break
        await browser.close()
        return dataForAllPages


    async def getNextUrl(self, page) -> str:
        next_url = None
        nextUrlTag = await page.query_selector('a.next.page-number')
        if nextUrlTag and await nextUrlTag.get_attribute("href") is not None:
            next_url = await nextUrlTag.get_attribute("href")
        return next_url
    
    async def getDataPerPage(self, page) ->list:
        data_per_page = []
        items = await page.query_selector_all('div.product-small.box')
        for item in items:
            data_per_page.append({f'Rank : {self._rank}' : await self.getDataPerRank(item)})
            self._rank+=1
       
        return data_per_page
    
    async def getDataPerRank(self, item) -> dict:
        fields = await self.validate_data_type(item)
        data_per_rank = {
            'Title' : fields.title,
            'Url' : fields.url,
            'Price' : fields.price
        }
        return data_per_rank
    
    async def validate_data_type(self, item) -> DataModel:
        data = DataModel(
            title = await self.getTitle(item),
            url = await self.getUrl(item),
            price = await self.getPrice(item)
        )
        return data
    
    async def getTitle(self, item) -> str:
        try:
            title : str = 'Not Found'
            titleElement = await item.query_selector('p.name.product-title.woocommerce-loop-product__title')
            if titleElement:
                title = await titleElement.text_content()
        except Exception as e:
            print(f'[x] Exception encountered in fetching Title : {e}')
        return title
    
    async def getUrl(self, item) -> str:
        try:
            url : str = 'Not found'
            url_element = await item.query_selector('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link')
            if url_element and await url_element.get_attribute('href') is not None:
                url = await url_element.get_attribute('href')
            pass
        except Exception as e:
            print(f'[x] Exception encountered in fetchin URL : {e}')
        return url
    
    async def getPrice(self, item) -> str:
        try:
            price : str = 'Not Found'
            price_element = await item.query_selector('span.price')
            if price_element:
                price = await price_element.text_content()
        except Exception as e:
            print(f'[x] Exception encountered in fetching Price : {e}')
        return price