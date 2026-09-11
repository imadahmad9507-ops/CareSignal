"""Capture the four FirstCommit submission screenshots from a local Flask app."""

from pathlib import Path
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright


PROJECT_DIR = Path(__file__).resolve().parent
SCREENSHOT_DIR = PROJECT_DIR / "screenshots"
BASE_URL = "http://127.0.0.1:5001"


def wait_for_server(url, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.25)
    raise RuntimeError(f"Flask did not start at {url} within {timeout} seconds.")


def main():
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    server = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "from app import app; app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)",
        ],
        cwd=PROJECT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_for_server(f"{BASE_URL}/")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
            views = {
                "dashboard": f"{BASE_URL}/",
                "ahmed-detail": f"{BASE_URL}/patients/1",
                "patient-report": f"{BASE_URL}/patients/1/report",
                "about-safety": f"{BASE_URL}/about",
            }
            for name, url in views.items():
                page.goto(url, wait_until="networkidle")
                if name == "ahmed-detail":
                    page.locator("#trendChart").wait_for(state="visible")
                page.screenshot(path=SCREENSHOT_DIR / f"{name}.png", full_page=True)
                print(f"Captured {name}.png")
            browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()
    print(f"Saved screenshots to {SCREENSHOT_DIR}")


if __name__ == "__main__":
    main()