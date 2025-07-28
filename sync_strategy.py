from playwright.sync_api import Playwright
from model import DataModel

class Execute():
    def __init__(self):
        self._nextUrl = None
        self._rank = 1
        self._page = 1

    def setBrowser(self, playwright: Playwright):
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(headless=False)
        return browser

    def run(self, playwright: Playwright, url : str) -> list:
        dataForAllPages = []
        browser = self.setBrowser(playwright)
        page = browser.new_page()
        self._nextUrl = url
        while True:
            page.goto(self._nextUrl)
            dataPerPage = self.getDataPerPage(page)
            if not dataPerPage:
                break
            dataForAllPages.append({f'Page : {self._page}' : dataPerPage})
            self._page+=1
            self._nextUrl = self.getNextUrl(page)
            if not self._nextUrl:
                break
        browser.close()
        return dataForAllPages
    
    def getNextUrl(self, page) -> str:
        next_url = None
        nextUrlTag = page.query_selector('a.next.page-number')
        if nextUrlTag and nextUrlTag.get_attribute("href") is not None:
            next_url = nextUrlTag.get_attribute("href")
        return next_url
    
    def getDataPerPage(self, page) -> list:
        data_per_page : list = []
        items : list = page.query_selector_all('div.product-small.box')
        for item in items:
            data_per_page.append({f'Rank : {self._rank}' : self.getDataPerRank(item)})
            self._rank+=1
       
        return data_per_page
    
    def getDataPerRank(self, item) -> dict:
        fields = self.validate_data_type(item)
        data_per_rank = {
            'Title' : fields.title,
            'Url' : fields.url,
            'Price' : fields.price
        }
        return data_per_rank
    
    def validate_data_type(self, item) -> DataModel:
        data = DataModel(
            title=self.getTitle(item),
            url=self.getUrl(item),
            price=self.getPrice(item)
        )
        return data
    
    def getTitle(self, item) -> str:
        try:
            title : str = 'Not Found'
            titleElement = item.query_selector('p.name.product-title.woocommerce-loop-product__title')
            if titleElement:
                title = titleElement.text_content()
        except Exception as e:
            print(f'[x] Exception encountered in fetching Title : {e}')
        return title
    
    def getUrl(self, item) -> str:
        try:
            url : str = 'Not Found'
            url_element = item.query_selector('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link')
            if url_element and url_element.get_attribute('href') is not None:
                url = url_element.get_attribute('href')
            pass
        except Exception as e:
            print(f'[x] Exception encountered in fetchin URL : {e}')
        return url
    
    def getPrice(self, item) -> str:
        try:
            price : str = '0.00'
            price_element = item.query_selector('span.price')
            if price_element:
                price = price_element.text_content()
        except Exception as e:
            print(f'[x] Exception encountered in fetching Price : {e}')
        return price