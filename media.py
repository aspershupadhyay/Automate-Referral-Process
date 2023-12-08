# sudo apt-get update
# sudo apt-get install -y xvfb
# pip install pandas playwright tqdm pyvirtualdisplay 
# playwright install 
# playwright install-deps

import re 
import random
import string
import asyncio
from tqdm import tqdm 
import pandas as pd 
from playwright.async_api import Playwright, async_playwright, expect
import warnings
warnings.filterwarnings("ignore")
from pyvirtualdisplay import Display

display = Display(visible=1, size=(1024, 768), backend ="xvfb") 
display.start()


names = pd.read_csv("https://raw.githubusercontent.com/Aspersh-Upadhyay/Scrape-Linkedin-Blog/main/names.csv",index_col=0)
def generate_random_password():
    """Generate a random password with randomized length between 8 and 25 characters."""
    length = random.randint(8, 25)
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        
        # to fix the the password requirements 
        if any(char.islower() for char in password) and \
           any(char.isupper() for char in password) and \
           any(char.isdigit() for char in password):
            return password

async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.mediafire.com/upgrade/?r=0c5n001")
    await page.wait_for_timeout(3000)

    await page.get_by_role("button", name="GET BASIC").click()
    await page.wait_for_timeout(5000)
    await page.wait_for_load_state('networkidle')


    first_name = random.choices(list(names.FirstName))[0]
    last_name = random.choices(list(names.Surname))[0]
    password = generate_random_password()
    await page.get_by_placeholder("First Name").fill(first_name)
    await page.get_by_placeholder("Last Name").fill(last_name)
    await page.wait_for_timeout(5000)
    page1 = await context.new_page()
    await page1.goto("https://internxt.com/temporary-email")
    await page1.get_by_role("button", name="Copy email").click()
    await page.get_by_label("Email").click()
    await page.get_by_label("Email").press("Control+V")
    await page.get_by_placeholder("Password").fill(password)
    await page.wait_for_timeout(5000)
    await page.get_by_label("I have read and agree to the Privacy Policy and Terms of Service.").check()
    await page.wait_for_timeout(4000)
    await page.wait_for_selector('iframe[title="reCAPTCHA"]')
        # Get the CAPTCHA iframe element
    
    # captcha_iframe = await page.query_selector('iframe[title="reCAPTCHA"]')
    # captcha_iframe.click()1
    await page.frame_locator("iframe[title='reCAPTCHA']").get_by_role("checkbox", name="I'm not a robot").click()
    await page.get_by_role("button", name="Create Account & Continue").click()    
    await page.wait_for_timeout(50000)

    # await page.wait_for_timeout(5000)  # Wait for 5 seconds
    # await page1.locator(".overflow-hidden > div > div:nth-child(3) > div > div > div > .cursor-pointer").click()
    # await page1.wait_for_timeout(3000)
    # await page1.locator(".overflow-hidden > div > div:nth-child(3) > div > div > div > .cursor-pointer").click()
    # await page1.wait_for_timeout(3000)
    # await page1.click("#__next > section.overflow-hidden.bg-gradient-to-b.from-white.to-gray-1.pb-20.pt-44 > div > div.flex.h-\[512px\].w-full.max-w-3xl.flex-row.space-y-2.overflow-hidden.rounded-xl.border.border-gray-10.shadow-subtle-hard > div.flex.flex-col > div > div.flex.w-full.flex-col.overflow-y-scroll > button > div > p.flex-row.text-sm.font-semibold.line-clamp-2")


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)

for i in tqdm(range(30)):
    asyncio.run(main())

display.stop()