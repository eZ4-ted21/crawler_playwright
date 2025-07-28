from playwright.sync_api import sync_playwright
from sync_strategy import Execute
from model import DataModel
url = 'https://urbangadgets.ph/category/aerial-photography/drone/?srsltid=AfmBOoq2ykFbvAeqBvZOAVZN9OA0nx_RoFbIeE_uoKCTS55CkxhBEHbf'

with sync_playwright() as playwright:
    _data : list = Execute().run(playwright, url)
    print(_data)