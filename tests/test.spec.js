const { test, expect } = require('@playwright/test');

test.describe('VeryBoard App', () => {
  let server;

  test.beforeAll(async () => {
    // This is a workaround to make this test work in the cloud environment
    // We need to kill the previous server if it exists
    try {
      const kill = require('kill-port');
      await kill(8000, 'tcp');
    } catch (e) {
      // Ignore errors if port is not in use
    }
  });

  test.beforeEach(async ({ page }) => {
    // Start a local server to host the HTML file
    await new Promise(resolve => {
        const http = require('http');
        const fs = require('fs');
        const path = require('path');
        server = http.createServer((req, res) => {
            const filePath = path.join(__dirname, '..', 'index.html');
            fs.readFile(filePath, (err, data) => {
                if (err) {
                    res.writeHead(500);
                    res.end(`Error loading ${filePath}`);
                    return;
                }
                res.writeHead(200);
                res.end(data);
            });
        }).listen(8000, resolve);
    });
    await page.goto('http://localhost:8000');
  });

  test.afterEach(async () => {
    await new Promise(resolve => server.close(resolve));
  });

  test('should allow creating a card with a category and linking it to another card', async ({ page }) => {
    // 1. Open the 'Create New Card' modal for the 'idea' lane
    await page.click('.new-card-button[data-lane-id="idea"]');
    await page.waitForSelector('md-dialog[open]');

    // 2. Fill in the title for the new card
    await page.locator('#card-title').click();
    await page.keyboard.type('My New Epic');

    // 3. Change the category to "Epic"
    await page.locator('#card-category').click();
    await page.locator('md-select-option[value="Epic"]').click();
    await page.locator('body').click(); // Click away to ensure change event fires

    // 4. Click save
    await page.click('md-filled-button[form="card-form"][value="save"]');

    // 5. Verify the new epic card is on the board
    await expect(page.locator('.kanban-card h3:has-text("My New Epic")')).toBeVisible();

    // 6. Create a second card, a "Story"
    await page.click('.new-card-button[data-lane-id="idea"]');
    await page.waitForSelector('md-dialog[open]');
    await page.locator('#card-title').click();
    await page.keyboard.type('My New Story');
    await page.locator('#card-category').click();
    await page.locator('md-select-option[value="Story"]').click();
    await page.locator('body').click(); // Click away to ensure change event fires

    // 7. Link the story to the epic
    await page.locator('#linked-cards').click();
    // Wait for the option to appear and click it
    await page.locator('md-select-option:has-text("My New Epic")').click();

    // Click outside the select to close it
    await page.locator('body').click();

    // 8. Save the story card
    await page.click('md-filled-button[form="card-form"][value="save"]');

    // 9. Verify the story card is on the board and has the linked epic badge
    const storyCard = page.locator('.kanban-card:has-text("My New Story")');
    await expect(storyCard).toBeVisible();

    const linkedBadge = storyCard.locator('.linked-card-badge:has-text("My New Epic")');
    await expect(linkedBadge).toBeVisible();

    // Take a screenshot
    await page.screenshot({ path: 'screenshot.png' });
  });
});
