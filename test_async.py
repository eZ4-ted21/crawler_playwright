import asyncio
from playwright.async_api import async_playwright
from async_strategy import Execute

url = 'https://urbangadgets.ph/category/aerial-photography/drone/?srsltid=AfmBOoq2ykFbvAeqBvZOAVZN9OA0nx_RoFbIeE_uoKCTS55CkxhBEHbf'

async def main():
    async with async_playwright() as playwright:
        _data : list = await Execute().run(playwright, url)
        print(_data)
asyncio.run(main())