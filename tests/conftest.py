import pytest
from app import app as flask_app

_FAKE_RESULT = {
    "query": "Mobile review youtube",
    "results": [
        {"author": "Channel A", "description": "Review one.", "video_url": "https://www.youtube.com/watch?v=abc"},
        {"author": "Channel B", "description": "Review two.", "video_url": "https://www.youtube.com/watch?v=def"},
        {"author": "Channel C", "description": "Review three.", "video_url": "https://www.youtube.com/watch?v=ghi"},
    ],
}


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def mock_workflow(mocker):
    return mocker.patch("app.ReviewWorkflow.run", return_value=_FAKE_RESULT)
