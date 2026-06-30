from pages.google_search_page import GoogleSearchPage
from utils.driver_factory import create_browser
from utils.logger import get_logger
from utils.retry import retry

logger = get_logger(__name__)


class GoogleSearchService:
    @retry(max_attempts=2, delay=3.0, exceptions=(Exception,))
    def search(self, query: str, count: int) -> list[str]:
        driver = create_browser()
        try:
            page = GoogleSearchPage(driver)
            page.open()
            page.search(query)
            return page.get_youtube_urls(count)
        finally:
            driver.quit()
