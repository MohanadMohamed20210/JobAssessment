import json
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent / "config.json"


def _load_cfg() -> dict:
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))


_cfg = _load_cfg()


class Config:
    appium_url: str = _cfg["appium"]["server_url"]
    device_name: str = _cfg["appium"]["device_name"]
    platform_version: str = _cfg["appium"]["platform_version"]
    app_package: str = _cfg["appium"]["app_package"]
    app_activity: str = _cfg["appium"]["app_activity"]

    browser: str = _cfg["browser"]["name"]
    headless: bool = _cfg["browser"]["headless"]

    search_query: str = _cfg["search"]["query"]
    results_count: int = _cfg["search"]["results_count"]

    host: str = _cfg["flask"]["host"]
    port: int = _cfg["flask"]["port"]
    debug: bool = _cfg["flask"]["debug"]

    explicit_wait: int = _cfg["explicit_wait"]
    screenshots_dir: str = _cfg["screenshots_dir"]

    @classmethod
    def reload(cls) -> None:
        """Re-read config.json and update all class attributes."""
        cfg = _load_cfg()
        cls.appium_url = cfg["appium"]["server_url"]
        cls.device_name = cfg["appium"]["device_name"]
        cls.platform_version = cfg["appium"]["platform_version"]
        cls.app_package = cfg["appium"]["app_package"]
        cls.app_activity = cfg["appium"]["app_activity"]
        cls.browser = cfg["browser"]["name"]
        cls.headless = cfg["browser"]["headless"]
        cls.search_query = cfg["search"]["query"]
        cls.results_count = cfg["search"]["results_count"]
        cls.host = cfg["flask"]["host"]
        cls.port = cfg["flask"]["port"]
        cls.debug = cfg["flask"]["debug"]
        cls.explicit_wait = cfg["explicit_wait"]
        cls.screenshots_dir = cfg["screenshots_dir"]
