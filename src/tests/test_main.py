def test_main(test_app) -> None:
    response = test_app.get('/')
    assert response.status_code == 200
    assert response.json() == {"status": "Working"}
