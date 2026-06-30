from abc import ABC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config


class BasePage(ABC):
    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver, Config.explicit_wait)

    def find(self, locator, timeout: int = None):
        w = WebDriverWait(self._driver, timeout) if timeout else self._wait
        return w.until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout: int = None):
        w = WebDriverWait(self._driver, timeout) if timeout else self._wait
        w.until(EC.element_to_be_clickable(locator)).click()
