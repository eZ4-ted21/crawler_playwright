import asyncio
from playwright.async_api import async_playwright
from async_strategy import Execute
from model import DataModel

url = 'https://geeksforgeeks.org'

async def main():
    async with async_playwright() as playwright:
        _data = await Execute().run(playwright, url)
        scrapedData = DataModel(
            url = _data['url'],
            title = _data['title']
        )
        print(scrapedData)
asyncio.run(main())