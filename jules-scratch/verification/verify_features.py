
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

    # 3. Verify the new rich text editor for the description
    modal = page.locator("#card-modal")
    expect(modal).to_be_visible()

    description_editor = modal.locator("#card-description")
    description_editor.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.keyboard.type("This is a bold test.")
    page.keyboard.press("Control+A")
    modal.locator("#description-toolbar [data-command='bold']").click()

    # 4. Save the card to a file
    # Start waiting for the download before clicking the button
    with page.expect_download() as download_info:
        modal.locator("#save-card-button").click()
    download = download_info.value
    download.save_as("jules-scratch/verification/test-card.vbcard")

    # 5. Close the modal and delete the card to ensure a clean slate for loading
    modal.get_by_role("button", name="Cancel").click()
    page.get_by_role("heading", name="Implement Kanban Board").dblclick()
    modal.locator("#delete-button").click()

    # 6. Load the card from the file
    page.locator("#card-loader").set_input_files("jules-scratch/verification/test-card.vbcard")

    # 7. Verify the card was loaded correctly
    expect(page.locator(".kanban-card", has_text="Implement Kanban Board")).to_be_visible()

    # 8. Verify the rich text content was loaded
    page.get_by_role("heading", name="Implement Kanban Board").dblclick()
    expect(modal.locator("#card-description strong")).to_have_text("This is a bold test.")

    # 9. Take a screenshot for verification
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)
