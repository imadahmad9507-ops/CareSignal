"""Compare the live Vercel and local chart rendering with Playwright."""

from pathlib import Path
import json
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright


PROJECT_DIR = Path(__file__).resolve().parent
LIVE_URL = "https://caresignal-firstcommit.vercel.app"
LOCAL_URL = "http://127.0.0.1:5000"
LIVE_SCREENSHOT = PROJECT_DIR / "screenshots" / "live-ahmed-detail.png"


def is_ready(url):
    try:
        with urllib.request.urlopen(f"{url}/patients/1", timeout=2) as response:
            return response.status == 200
    except OSError:
        return False


def start_local_if_needed():
    if is_ready(LOCAL_URL):
        return None
    return subprocess.Popen(
        [sys.executable, "-c", "from app import app; app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)"],
        cwd=PROJECT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def wait_for_local(server):
    if server is None:
        return
    deadline = time.time() + 15
    while time.time() < deadline:
        if is_ready(LOCAL_URL):
            return
        time.sleep(0.25)
    raise RuntimeError("Local Flask server did not become ready on port 5000.")


def inspect_site(browser, name, base_url, screenshot_path=None):
    page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
    console_messages = []
    network_messages = []
    failed_requests = []

    page.on("console", lambda message: console_messages.append({"type": message.type, "text": message.text}))
    page.on("requestfailed", lambda request: failed_requests.append({"url": request.url, "error": request.failure}))
    page.on(
        "response",
        lambda response: network_messages.append(
            {"status": response.status, "url": response.url, "resource": response.request.resource_type}
        )
    )

    page.goto(f"{base_url}/patients/1", wait_until="networkidle")
    page.locator("#trendChart").wait_for(state="visible")
    chart_state = page.evaluate(
        """() => {
          const canvas = document.querySelector('#trendChart');
          const chart = canvas && window.Chart && Chart.getChart(canvas);
          const context = canvas && canvas.getContext('2d');
          let nonTransparentPixels = 0;
          if (canvas && context) {
            const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
            for (let i = 3; i < pixels.length; i += 4) {
              if (pixels[i] > 0) nonTransparentPixels += 1;
            }
          }
          return {
            canvasExists: Boolean(canvas),
            canvasWidth: canvas ? canvas.width : 0,
            canvasHeight: canvas ? canvas.height : 0,
            cssWidth: canvas ? canvas.getBoundingClientRect().width : 0,
            cssHeight: canvas ? canvas.getBoundingClientRect().height : 0,
            chartJsLoaded: Boolean(window.Chart),
            chartInstanceCreated: Boolean(chart),
            datasetCount: chart ? chart.data.datasets.length : 0,
            observationCount: Array.isArray(window.trendData) ? window.trendData.length : 0,
            nonTransparentPixels
          };
        }"""
    )
    if screenshot_path:
        page.screenshot(path=screenshot_path, full_page=True)

    bad_responses = [item for item in network_messages if item["status"] >= 400]
    result = {
        "site": name,
        "url": base_url,
        "console": console_messages,
        "network": network_messages,
        "failed_requests": failed_requests,
        "bad_responses": bad_responses,
        "chart": chart_state,
        "screenshot": str(screenshot_path) if screenshot_path else None,
    }
    page.close()
    return result


def print_report(result):
    print(f"\n=== {result['site']} ({result['url']}) ===")
    print("Chart state:")
    print(json.dumps(result["chart"], indent=2))
    print("Console messages:")
    print(json.dumps(result["console"], indent=2) if result["console"] else "[]")
    print("Full network log:")
    print(json.dumps(result["network"], indent=2) if result["network"] else "[]")
    print("Failed requests:")
    print(json.dumps(result["failed_requests"], indent=2) if result["failed_requests"] else "[]")
    print("HTTP responses with status >= 400:")
    print(json.dumps(result["bad_responses"], indent=2) if result["bad_responses"] else "[]")
    if result["screenshot"]:
        print(f"Screenshot: {result['screenshot']}")


def main():
    local_server = start_local_if_needed()
    try:
        wait_for_local(local_server)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            results = [
                inspect_site(browser, "LIVE Vercel", LIVE_URL, LIVE_SCREENSHOT),
                inspect_site(browser, "LOCAL Flask", LOCAL_URL),
            ]
            browser.close()
        for result in results:
            print_report(result)
        failed = any(
            result["failed_requests"]
            or result["bad_responses"]
            or not result["chart"]["canvasExists"]
            or not result["chart"]["chartJsLoaded"]
            or not result["chart"]["chartInstanceCreated"]
            or result["chart"]["nonTransparentPixels"] == 0
            for result in results
        )
        print(f"\nVERDICT: {'FAIL' if failed else 'PASS'}")
        return 1 if failed else 0
    finally:
        if local_server is not None:
            local_server.terminate()
            local_server.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
