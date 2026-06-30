import urllib.request

from appium.webdriver.appium_service import AppiumService

from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class AppiumServer:
    _instance = None
    _service: AppiumService | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start(self):
        if self._reachable():
            return
        self._service = AppiumService()
        self._service.start(args=["--log", "appium.log"], timeout_ms=30000)
        logger.info("Appium server started")

    def stop(self):
        if self._service:
            self._service.stop()
            self._service = None

    def _reachable(self) -> bool:
        try:
            urllib.request.urlopen(f"{Config.appium_url}/status", timeout=2)
            return True
        except Exception:
            return False
