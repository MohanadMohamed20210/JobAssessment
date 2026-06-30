def test_reviews_ok(client, mock_workflow):
    assert client.get("/reviews").status_code == 200


def test_reviews_shape(client, mock_workflow):
    data = client.get("/reviews").get_json()
    assert "query" in data and "results" in data


def test_reviews_returns_three(client, mock_workflow):
    assert len(client.get("/reviews").get_json()["results"]) == 3


def test_result_fields(client, mock_workflow):
    for item in client.get("/reviews").get_json()["results"]:
        assert {"author", "description", "video_url"} <= item.keys()


def test_lookup_error_returns_404(client, mocker):
    mocker.patch("app.ReviewWorkflow.run", side_effect=LookupError("No results"))
    assert client.get("/reviews").status_code == 404


def test_generic_error_returns_502(client, mocker):
    mocker.patch("app.ReviewWorkflow.run", side_effect=Exception("boom"))
    assert client.get("/reviews").status_code == 502
