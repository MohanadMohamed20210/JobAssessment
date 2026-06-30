from config import Config
from services.google_search import GoogleSearchService
from services.youtube_app import YoutubeAppService


class ReviewWorkflow:
    def run(self) -> dict:
        urls = GoogleSearchService().search(Config.search_query, Config.results_count)
        if not urls:
            raise LookupError("No YouTube results found")
        with YoutubeAppService() as yt:
            results = [yt.extract_video_data(url) for url in urls]
        return {"query": Config.search_query, "results": results}
