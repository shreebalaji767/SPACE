import asyncio
import os
from playwright.async_api import async_playwright

BASE = os.environ.get("VOID_SPACE_URL", "http://127.0.0.1:5000")
SIZES = [
    (320, 568, True),
    (360, 740, True),
    (390, 844, True),
    (430, 932, True),
    (768, 1024, False),
    (1024, 768, False),
    (1366, 768, False),
    (1920, 1080, False),
    (844, 390, True),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        failures = []
        for width, height, touch in SIZES:
            context = await browser.new_context(
                viewport={"width": width, "height": height},
                is_mobile=touch,
                has_touch=touch,
                device_scale_factor=1,
            )
            page = await context.new_page()
            page_errors = []
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            await page.goto(BASE, wait_until="domcontentloaded")
            await page.wait_for_selector("#voidUniverseLanding", state="visible")
            await page.wait_for_timeout(180)
            await page.locator("#voidUniverseLanding").click()
            await page.wait_for_selector("#voidUniverse.open", state="visible")
            for tab in ("galaxy", "fleet", "station", "war", "missions", "chronicle"):
                await page.locator(f'[data-vtab="{tab}"]').click()
                await page.wait_for_timeout(30)
            metrics = await page.evaluate("""() => ({
                width: innerWidth,
                documentWidth: document.documentElement.scrollWidth,
                bodyWidth: document.body.scrollWidth,
                modalWidth: document.querySelector('.vu-shell').getBoundingClientRect().width,
                canvasWidth: document.querySelector('#game').width
            })""")
            if metrics["documentWidth"] > width + 2 or metrics["bodyWidth"] > width + 2:
                failures.append(f"{width}x{height}: horizontal overflow {metrics}")
            if metrics["canvasWidth"] < 1:
                failures.append(f"{width}x{height}: canvas has no backing width")
            await page.locator("#vuClose").click()
            await page.locator("#landingPlayButton").click()
            await page.wait_for_timeout(250)
            controls = await page.evaluate("""() => ({
                touch: getComputedStyle(document.querySelector('#touchControls')).display,
                dock: getComputedStyle(document.querySelector('#gameControls')).display,
                hud: getComputedStyle(document.querySelector('#hud')).display
            })""")
            if touch and controls["touch"] != "block":
                failures.append(f"{width}x{height}: touch controls not enabled in run: {controls}")
            if not touch and width >= 701 and controls["dock"] != "grid":
                failures.append(f"{width}x{height}: desktop control dock not enabled: {controls}")
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(80)
            if touch:
                hidden = await page.evaluate("getComputedStyle(document.querySelector('#touchControls')).display")
                if hidden != "none":
                    failures.append(f"{width}x{height}: touch controls remain visible while paused ({hidden})")
            if page_errors:
                failures.append(f"{width}x{height}: uncaught browser errors: {page_errors}")
            print(f"PASS {width}x{height} touch={touch} metrics={metrics} controls={controls}")
            await context.close()
        await browser.close()
        if failures:
            raise SystemExit("\\n".join(failures))
        print("All responsive and command-hub browser checks passed.")

asyncio.run(main())
