# YouTube Mobile Reviews

## Demo & Code Walkthrough

A short video demonstrating the complete end-to-end workflow and explaining the project structure and implementation:

https://drive.google.com/file/d/1Bm6XjHd-7rhtyFgRgw8OlSEcy15uSoYh/view?usp=sharing

> **Note:** Idempotency-Id support was added after the video was recorded and is not shown in the demo.

---

A Flask API that searches Google for YouTube mobile-review videos, opens each result in the YouTube Android app via Appium, extracts the video's author, description, and URL, and returns them as JSON.

Compatible with **Windows** and **Linux**.

---

## Prerequisites

- Python 3.12+
- Google Chrome (ChromeDriver is handled automatically by Selenium Manager)
- [Appium 2/3](https://appium.io) + UiAutomator2 driver

  ```bash
  npm install -g appium
  appium driver install uiautomator2
  ```

- Android SDK with `adb` available in `PATH`
- An Android emulator or a physical Android device
- YouTube app (`com.google.android.youtube`) installed on the device

---

## Installation

```bash
python -m venv .venv

# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Running

Start the Flask API:

```bash
python app.py
```

Call the endpoint:

```bash
curl -H "Idempotency-Id: abc123" http://localhost:5000/reviews
```

> **Note:** Change the `Idempotency-Id` value on every new request. Reusing the same ID returns the cached response and skips the workflow.

---

## Tests

All external dependencies are mocked, so no browser, emulator, or Android device is required.

```bash
pytest
```

---

## Docker

> **Known limitation:** The Docker image builds successfully and runs the Flask/Selenium components correctly. However, reliably connecting the container to a locally running Appium server across different operating systems proved inconsistent. I experimented with `host.docker.internal` and `extra_hosts`, but the solution was not portable, so the Docker configuration has been left in the repository for reference.

```bash
docker compose up --build
```

---

## Project Structure

```
app.py                - Flask entry point, exposes GET /reviews
config.py             - Loads config.json into a Config class
config.json           - All runtime settings (Appium, browser, Flask, search)

pages/
  base_page.py          - Shared Selenium/Appium helpers
  google_search_page.py - Google Search locators and actions
  youtube_video_page.py - YouTube Android app locators and actions

services/
  google_search.py      - Performs the Google search and returns video URLs
  youtube_app.py        - Opens each URL in YouTube and extracts video information
  workflow.py           - Coordinates the complete workflow

utils/
  driver_factory.py     - Creates Selenium and Appium driver instances
  appium_server.py      - Starts and stops the local Appium server
  retry.py              - Exponential backoff retry decorator
  logger.py             - Shared application logger

tests/
  test_reviews.py       - Mocked end-to-end workflow tests
  conftest.py           - Pytest fixtures

logs/
  workflow.log          - Runtime log written on every run (errors, failures)
  response.json         - Last API response saved for inspection
```

---
