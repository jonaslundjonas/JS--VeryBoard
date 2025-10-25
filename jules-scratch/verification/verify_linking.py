from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Listen for console events and print them
    page.on("console", lambda msg: print(f"Browser console: {msg.text}"))

    page.goto("http://localhost:8000")

    # 1. Double-click the first card to open the editor
    first_card = page.locator(".kanban-card").first
    first_card.dblclick()

    # 2. Open the linked cards dropdown
    linked_cards_select = page.locator("#linked-cards")
    expect(linked_cards_select).to_be_visible()
    linked_cards_select.click()

    # 3. Select the "Add Drag and Drop" card to link it
    option_to_select = page.locator("md-select-option", has_text="Add Drag and Drop")
    expect(option_to_select).to_be_visible()
    option_to_select.click()

    # 4. Click the body to close the dropdown
    page.locator("body").click()

    # 5. Save the card
    page.locator('md-filled-button[form="card-form"][value="save"]').click()

    # 6. Verify the linked card badge is now visible on the card
    linked_badge = first_card.locator(".linked-card-badge")
    expect(linked_badge).to_have_text("Add Drag and Drop")

    # 7. Take a screenshot for visual confirmation
    page.screenshot(path="jules-scratch/verification/verification.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
