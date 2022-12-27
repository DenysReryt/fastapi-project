import json

from src.app.users.user_crud import crud


def test_create_user(test_app, monkeypatch) -> None:
    test_request_payload = {'first_name': 'som', 'last_name': 'som', 'email': 'som@gmail.com',
                            'password': 'som', 'role': 'som', 'verified': False}
    test_response_payload = {'id': 1, 'first_name': 'som', 'last_name': 'som', 'role': 'som',
                             'email': 'som@gmail.com', 'created_at': 'som', 'updated_at': 'som'}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, 'create_user', mock_post)

    response = test_app.post('/create', data=json.dumps(test_request_payload))

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_create_invalid_json(test_app):
    response = test_app.post('/create', data=json.dumps({'first_name': 'som'}))
    assert response.status_code == 404
