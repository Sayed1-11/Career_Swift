import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Login first
        await page.goto("http://127.0.0.1:8000/login/")
        # Use our activated user jane.upload5@demo.com
        await page.fill('input[name="username"]', 'jane.upload5@demo.com')
        await page.fill('input[name="password"]', 'StrongPassword123!')
        await page.click('button[type="submit"]')
        
        await page.wait_for_timeout(1000)
        
        # Go to profile
        await page.goto("http://127.0.0.1:8000/profile/")
        await page.screenshot(path="before_upload.png")

        # Create a dummy pdf
        with open("dummy_test_resume.pdf", "wb") as f:
            f.write(b"%PDF-1.4\n% dummy content")

        # Set input files
        await page.set_input_files('input#resumeUpload', 'dummy_test_resume.pdf')
        await page.wait_for_timeout(500)
        await page.screenshot(path="after_file_set.png")

        # Get all forms with 'enctype="multipart/form-data"'
        # and click its submit button
        # Form 2 is likely the resume, as form 1 is profile picture, form 0 is personal info.
        # But wait, we can just click the button inside the form containing #resumeUpload
        upload_button = page.locator('input#resumeUpload').locator("xpath=ancestor::form").locator('button[type="submit"]')
        await upload_button.click()
        
        await page.wait_for_timeout(2000)
        await page.screenshot(path="after_upload_submit.png")
        
        # Print status of page
        print("Final URL:", page.url)
        content = await page.content()
        if "Resume uploaded successfully" in content:
            print("SUCCESS message found in HTML!")
        else:
            print("FAILURE. Check after_upload_submit.png")
            # print forms
            
        await browser.close()

asyncio.run(main())
