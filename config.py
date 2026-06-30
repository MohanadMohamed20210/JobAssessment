import json
from pathlib import Path

_cfg = json.loads((Path(__file__).parent / "config.json").read_text())


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
