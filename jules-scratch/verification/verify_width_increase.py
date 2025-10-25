
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Serve the index.html file
        await page.goto('file://' + __file__.replace('jules-scratch/verification/verify_width_increase.py', 'index.html'))

        # Open the editor for the first card
        await page.dblclick('.kanban-card[data-card-id="card-1"]')
        await page.wait_for_selector('#card-modal[open]')

        # Take a screenshot of the card editor modal
        await page.screenshot(path='jules-scratch/verification/card_editor_widened_500px.png')

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
