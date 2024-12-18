import pytest
from app import create_app
from config.config import Config

class TestConfig(Config):
    TESTING = True
    # Test database connection
    DB_SERVER = 'test_server'
    DB_DATABASE = 'test_database'
    DB_USERNAME = 'test_user'
    DB_PASSWORD = 'test_password'
    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
