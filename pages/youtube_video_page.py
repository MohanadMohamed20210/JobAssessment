import os
import time
import datetime

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from config import Config
from pages.base_page import BasePage

_PKG = Config.app_package


class YoutubeVideoPage(BasePage):
    _WATCH_PLAYER      = (AppiumBy.ID,    f"{_PKG}:id/watch_player")
    _SUBSCRIBE_BTN     = (AppiumBy.XPATH, "//*[contains(@content-desc, 'ubscribe to ')]")
    _CHANNEL_INFO      = (AppiumBy.XPATH, "//*[contains(@content-desc, ' subscribers')]")
    _PERMISSION_DENY   = (AppiumBy.ID,    "com.android.permissioncontroller:id/permission_deny_button")
    _AD_INDICATOR      = (AppiumBy.ID,    f"{_PKG}:id/ad_progress_text")
    _SKIP_AD           = (AppiumBy.ID,    f"{_PKG}:id/skip_ad_button")
    _SEE_MORE          = (AppiumBy.XPATH, "//*[@content-desc='See more']")
    _DESCRIPTION_PANEL = (AppiumBy.XPATH,
                          "//*[@resource-id='com.google.android.youtube:id/engagement_panel_wrapper']"
                          "//android.widget.TextView")
    _DESC_CARD         = (AppiumBy.ANDROID_UIAUTOMATOR,
                          f'new UiSelector().resourceId("{_PKG}:id/watch_list")'
                          '.childSelector(new UiSelector().clickable(true).instance(0))')

    def open_video(self, url: str):
        try:
            self._driver.terminate_app(_PKG)
            time.sleep(1)
        except Exception:
            pass
        self._driver.execute_script("mobile: deepLink", {"url": url, "package": _PKG})
        self._wait.until(lambda d: d.current_package == _PKG)
        self.find(self._WATCH_PLAYER)
        self._dismiss_permission()
        self._skip_ad()
        time.sleep(5)

    def get_channel_name(self) -> str:
        try:
            btn = self.find(self._SUBSCRIBE_BTN, timeout=10)
            label = btn.get_attribute("content-desc") or ""
            for prefix in ("Subscribed to ", "Subscribe to "):
                if label.startswith(prefix):
                    return label.removeprefix(prefix).split(" with")[0].rstrip(".,")
        except Exception:
            pass
        try:
            row = self.find(self._CHANNEL_INFO, timeout=5)
            label = row.get_attribute("content-desc") or ""
            return label.rsplit(" ", 2)[0]
        except Exception:
            return ""

    def get_description(self) -> str:
        try:
            self.click(self._DESC_CARD, timeout=8)
            WebDriverWait(self._driver, 8).until(
                lambda d: any(e.text.strip() for e in d.find_elements(*self._DESCRIPTION_PANEL))
            )
        except Exception:
            return ""

        try:
            self.click(self._SEE_MORE, timeout=2)
            time.sleep(1)
        except Exception:
            pass

        elems = self._driver.find_elements(*self._DESCRIPTION_PANEL)
        texts = [e.text.strip() for e in elems if e.text.strip()]
        return max(texts, key=len) if texts else ""

    def take_screenshot(self, label: str) -> str:
        os.makedirs(Config.screenshots_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(Config.screenshots_dir, f"{label}_{ts}.png")
        self._driver.save_screenshot(path)
        return path

    def _dismiss_permission(self):
        try:
            self.click(self._PERMISSION_DENY, timeout=2)
        except Exception:
            pass

    def _skip_ad(self):
        try:
            self.find(self._AD_INDICATOR, timeout=2)
        except Exception:
            return
        try:
            self.click(self._SKIP_AD, timeout=10)
        except Exception:
            WebDriverWait(self._driver, 30).until_not(
                lambda d: d.find_elements(*self._AD_INDICATOR)
            )
