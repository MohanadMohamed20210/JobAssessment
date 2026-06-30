from urllib.parse import urlparse, parse_qs, unquote

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


def _youtube_url(href: str) -> str | None:
    if not href:
        return None
    if "google.com/url" in href:
        href = unquote(parse_qs(urlparse(href).query).get("q", [""])[0])
    if "youtube.com/watch" not in href:
        return None
    video_id = parse_qs(urlparse(href).query).get("v", [None])[0]
    return f"https://www.youtube.com/watch?v={video_id}" if video_id else None


class GoogleSearchPage(BasePage):
    _URL = "https://www.google.com"
    _SEARCH_BOX = (By.NAME, "q")
    _RESULTS = (By.ID, "search")

    def open(self):
        self._driver.get(self._URL)

    def search(self, query: str):
        self.find(self._SEARCH_BOX).send_keys(query + Keys.ENTER)
        self.find(self._RESULTS)
        self._select_videos_tab()
        logger.info("Searched: %r", query)

    def get_youtube_urls(self, count: int) -> list[str]:
        try:
            container = self._driver.find_element(*self._RESULTS)
        except Exception:
            container = self._driver
        urls = []
        for a in container.find_elements(By.TAG_NAME, "a"):
            url = _youtube_url(a.get_attribute("href") or "")
            if url and url not in urls:
                urls.append(url)
                if len(urls) == count:
                    break
        return urls

    def _select_videos_tab(self):
        current = self._driver.current_url
        if "tbm=vid" not in current:
            self._driver.get(current + "&tbm=vid")
            self.find(self._RESULTS)
