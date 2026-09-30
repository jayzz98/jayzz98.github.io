import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.goto("file:///D:/AI%20Insights/landing_flattened.html")
        await page.screenshot(path="assets/ai_app_screenshot.png")
        await browser.close()

asyncio.run(main())
