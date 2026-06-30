from config import Config
from pages.youtube_video_page import YoutubeVideoPage
from utils.driver_factory import create_appium_driver
from utils.logger import get_logger

logger = get_logger(__name__)


class YoutubeAppService:
    def __init__(self):
        self._driver = None

    def __enter__(self):
        self._driver = create_appium_driver()
        return self

    def __exit__(self, *_):
        if self._driver:
            try:
                self._driver.terminate_app(Config.app_package)
            except Exception:
                pass
            self._driver.quit()
            self._driver = None

    def extract_video_data(self, url: str) -> dict:
        page = YoutubeVideoPage(self._driver)
        try:
            page.open_video(url)
            author = page.get_channel_name()
            description = page.get_description()
            return {
                "author": author,
                "description": description,
                "video_url": url,
            }
        except Exception as exc:
            logger.error("Failed for %s: %s", url, exc)
            screenshot = None
            try:
                screenshot = page.take_screenshot(f"fail_{url[-20:].replace('/', '_')}")
            except Exception:
                pass
            return {"author": None, "description": None, "video_url": url, "error": str(exc), "screenshot": screenshot}
