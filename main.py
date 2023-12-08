# --Prerequisites before run the code. 
    # sudo apt-get update
    # sudo apt-get install -y xvfb
    # pip install pandas playwright tqdm pyvirtualdisplay 
    # playwright install 
    # playwright install-deps

import re 
import random
import string
import asyncio
import warnings
import pandas as pd 
from tqdm import tqdm 
from pyvirtualdisplay import Display
from playwright.async_api import Playwright, async_playwright, expect
warnings.filterwarnings("ignore")


display = Display(visible=1, size=(1024, 768), backend ="xvfb") 
display.start()

names = pd.read_csv("https://raw.githubusercontent.com/Aspersh-Upadhyay/Scrape-Linkedin-Blog/main/names.csv",index_col=0)
def generate_random_password():
    """Generate a random password with randomized length between 8 and 25 characters."""
    length = random.randint(8, 25)
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        
        # to fix the password requirements 
        if any(char.islower() for char in password) and \
           any(char.isupper() for char in password) and \
           any(char.isdigit() for char in password) and \
           any(char in string.punctuation for char in password):
            return password
        
async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://gamma.app/signup?r=ayec3135mc29xx5")

    page1 = await context.new_page()
    await page1.goto("https://internxt.com/temporary-email")
    await page1.get_by_role("button", name="Copy email").click()
    await page.get_by_label("Email").click()
    await page.get_by_label("Email").press("Control+V")
    await page.get_by_label("Email").press("Enter")
    await page.wait_for_timeout(5000)  # Wait for 5 seconds
    await page1.locator(".overflow-hidden > div > div:nth-child(3) > div > div > div > .cursor-pointer").click()
    await page1.wait_for_timeout(3000)
    await page1.locator(".overflow-hidden > div > div:nth-child(3) > div > div > div > .cursor-pointer").click()
    await page1.wait_for_timeout(3000)
    await page1.click("#__next > div.z-50.flex.flex-col.overflow-hidden.pt-\[64px\].md\:pt-\[54px\] > section.overflow-hidden.bg-gradient-to-b.from-white.to-gray-1.pt-32.pb-20 > div > div.flex.h-\[512px\].w-full.max-w-3xl.flex-row.space-y-2.overflow-hidden.rounded-xl.border.border-gray-10.shadow-subtle-hard > div:nth-child(1) > div > div.flex.w-full.flex-col.overflow-y-scroll > button > div")
    await page1.get_by_role('button', name="pm_bounces@pm-bounces.gamma.app").click()

    link_element = await page1.get_by_role("link", name="Verify your email address").get_attribute("href")
    page2 = await context.new_page()
    await page2.goto(link_element)
    # print("Done👍")

    first_name = random.choices(list(names.FirstName))[0]
    last_name = random.choices(list(names.Surname))[0]
    password = generate_random_password()
    await page2.get_by_label("First name").fill(first_name)
    await page2.get_by_label("Last name").fill(last_name)
    await page2.get_by_label("Password", exact=True).fill(password)
    await page2.get_by_label("Password", exact=True).press("Enter")

    await page2.wait_for_timeout(5000)
    await page2.fill("#field-\:ru\:", f"{first_name}'s Workspace")
    # await page2.get_by_label("Workspace name").fill(f"{first_name}'s Workspace")
    await page2.wait_for_timeout(3000)
    await page2.press("#field-\:ru\:", "Tab")
    await page2.keyboard.press("Enter")

    await page2.wait_for_timeout(4000)  # Wait for 4 seconds
    use = ["For personal use","For Work","For School"]
    rand_use = random.choices(use)[0]
    
    await page2.locator("label").filter(has_text=rand_use).locator("span").first.click()
    # Randomly select an index
    if rand_use != "For School":
        random_index = random.randint(0, 8)
        await page2.get_by_role("combobox", name="What kind of work do you do?").select_option(index=random_index)

    # where you here about us 
    options = ["Facebook","Twitter","Instagram","LinkedIn","YouTube","WhatsApp","Telegram",
            "Snapchat","Pinterest","Reddit","Google Chrome","Mozilla Firefox","Safari",
            "Microsoft Edge","Opera","Skype","Slack","Zoom","Microsoft Teams","Discord",
                "Friend"
            ]

    random_option = random.choice(options)
    await page2.get_by_label("How did you hear about us?").click()
    await page2.get_by_label("How did you hear about us?").fill(random_option)
    await page2.locator("div").filter(has_text=re.compile(r"^Continue$")).nth(1).click()
    # await page2.get_by_role("button", name="Presentation").click()


    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)

def run_with_retry(max_attempts=100):
    for i in tqdm(range(1000)):
        attempt = 0
        while attempt < max_attempts:
            try:
                asyncio.run(main())
                break  # If no error occurs, break out of the retry loop
            except Exception as e:
                attempt += 1
                print(f"Error occurred in iteration {i + 1}, retrying ({attempt}/{max_attempts}): {e}")

run_with_retry()

display.stop()  