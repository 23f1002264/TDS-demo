import asyncio
import re
from playwright.async_api import async_playwright

BASE = "https://sanand0.github.io/tdsdata/tables/?seed="
SEEDS = list(range(60, 70))

def extract_numbers(text):
    nums = re.findall(r'-?\d+\.?\d*', text.replace(',', ''))
    return [float(n) for n in nums]

async def get_seed_sum(page, seed):
    url = BASE + str(seed)
    print(f"Opening {url}")

    await page.goto(url, wait_until="networkidle", timeout=60000)
    await page.wait_for_selector("table", timeout=20000)

    cells = await page.eval_on_selector_all(
        "table",
        """tables => tables.flatMap(t =>
            Array.from(t.querySelectorAll("th, td"))
                .map(c => c.innerText)
        )"""
    )

    numbers = []
    for text in cells:
        numbers.extend(extract_numbers(text))

    seed_sum = sum(numbers)
    print(f"Seed {seed} sum = {seed_sum}")
    return seed_sum

async def main():
    total = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for seed in SEEDS:
            total += await get_seed_sum(page, seed)

        await browser.close()

    print("\nFINAL TOTAL =", total)

asyncio.run(main())
