import asyncio
import sys
from playwright.async_api import async_playwright

APPS = [
    {
        "name": "AI BI Copilot",
        "url": "https://ai-bi-copilot-wr2adpymchahht5scekfzz.streamlit.app/"
    },
    {
        "name": "Data Lie Detector",
        "url": "https://data-lie-detector-jhb8hfd45evqe7h7auqt4u.streamlit.app/"
    }
]

async def check_and_wake(app, p):
    name = app["name"]
    url = app["url"]
    print(f"\n==========================================")
    print(f" Checking: {name}")
    print(f" URL: {url}")
    print(f"==========================================")
    
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    
    try:
        # Navigate to the app with a generous timeout
        response = await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        print(f"HTTP Status: {response.status if response else 'Unknown'}")
        
        # Wait a moment for Streamlit React app / hydration
        await asyncio.sleep(6)
        
        content = await page.content()
        title = await page.title()
        print(f"Page Title: {title}")
        
        # Check if the app is in sleep mode
        wake_button = await page.query_selector('button:has-text("Yes, get this app back up")')
        
        if wake_button:
            print(f"[STATUS] '{name}' was ASLEEP! Found 'Yes, get this app back up' button.")
            print("Action: Clicking wake-up button...")
            await wake_button.click()
            print("Clicked! Waiting 20 seconds for boot sequence...")
            await asyncio.sleep(20)
            
            # Check status again
            content_after = await page.content()
            if "Yes, get this app back up" not in content_after:
                print(f"[SUCCESS] '{name}' has been successfully awakened!")
            else:
                print(f"[INFO] '{name}' wake command sent; container is spinning up.")
        elif "This app has gone to sleep" in content or "Zzzz" in content:
            print(f"[STATUS] '{name}' shows sleep message, attempting to locate and click any button...")
            buttons = await page.query_selector_all("button")
            for btn in buttons:
                txt = await btn.inner_text()
                if "wake" in txt.lower() or "back up" in txt.lower():
                    await btn.click()
                    print(f"Clicked button with text: '{txt}'")
                    break
        else:
            print(f"[SUCCESS] '{name}' is ACTIVE & AWAKE! Inactivity timer refreshed.")
            # Remain on page briefly to ensure Streamlit registers active session
            await asyncio.sleep(5)
            
    except Exception as e:
        print(f"[ERROR] Failed checking '{name}': {e}", file=sys.stderr)
    finally:
        await browser.close()

async def main():
    print("Starting Streamlit Apps Keep-Alive check...")
    async with async_playwright() as p:
        for app in APPS:
            await check_and_wake(app, p)
    print("\nKeep-Alive routine completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
