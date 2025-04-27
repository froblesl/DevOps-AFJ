import pytest
from main import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

# ✅ Simula que el token siempre es válido
@pytest.fixture(autouse=True)
def mock_validar_token(monkeypatch):
    monkeypatch.setattr('blueprints.operations.validar_token', lambda: True)

def test_healthcheck(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_create_blacklist_missing_fields(client):
    response = client.post('/blacklists', json={})
    assert response.status_code == 400
    assert "Faltan campos requeridos" in response.json["msg"]

def test_create_blacklist_invalid_uuid(client):
    response = client.post('/blacklists', json={
        "email": "test@example.com",
        "app_uuid": "no-es-uuid",
        "blocked_reason": "spam"
    })
    assert response.status_code == 400
    assert "UUID válido" in response.json["msg"]

def test_check_blacklist_entry_not_found(client, monkeypatch):
    # ✅ Mock completo para db.session.query().filter_by().first() => None
    class FakeQuery:
        def filter_by(self, **kwargs):
            class Result:
                def first(self):
                    return None
            return Result()

    class FakeSession:
        def query(self, *args, **kwargs):
            return FakeQuery()

    monkeypatch.setattr('blueprints.operations.db', type('FakeDB', (), {'session': FakeSession()})())

    response = client.get('/blacklists/test@example.com')
    assert response.status_code == 200
    assert response.json["blacklisted"] is False
    assert response.json["reason"] is None
