
import os
from playwright.sync_api import sync_playwright, expect

def run_verification(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # 1. Navigate to the application
    file_path = f"file://{os.path.abspath('index.html')}"
    page.goto(file_path)

    # 2. Open a card for editing
    page.get_by_role("heading", name="Implement Kanban Board").dblclick()

    # 3. Verify the rich text editor is now on the comment field
    modal = page.locator("#card-modal")
    expect(modal).to_be_visible()

    comment_editor = modal.locator("#card-comment")
    comment_editor.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.keyboard.type("This is a bold test.")
    page.keyboard.press("Control+A")
    modal.locator("#comment-toolbar [data-command='bold']").click()

    # 4. Save the changes to the board
    modal.get_by_role("button", name="Save to Board").click()

    # 5. Re-open the card and verify the rich text content was saved
    page.get_by_role("heading", name="Implement Kanban Board").dblclick()
    expect(modal.locator("#card-comment strong")).to_have_text("This is a bold test.")

    # 6. Take a screenshot for verification
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)
