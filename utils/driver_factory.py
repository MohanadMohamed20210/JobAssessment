import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options

from config import Config
from utils.appium_server import AppiumServer


def create_browser():
    if Config.browser == "firefox":
        opts = FirefoxOptions()
        if Config.headless:
            opts.add_argument("-headless")
        return webdriver.Firefox(options=opts)
    opts = ChromeOptions()
    if Config.headless:
        opts.add_argument("--headless=new")
    if sys.platform == "linux":
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=opts)


def create_appium_driver() -> appium_webdriver.Remote:
    AppiumServer().start()
    opts = UiAutomator2Options()
    opts.device_name = Config.device_name
    opts.platform_version = Config.platform_version
    opts.app_package = Config.app_package
    opts.app_activity = Config.app_activity
    opts.no_reset = True
    return appium_webdriver.Remote(Config.appium_url, options=opts)
