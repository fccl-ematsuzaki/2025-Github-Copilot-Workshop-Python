import pytest
from app import create_app


def pytest_configure(config):
    """
    カスタムマーカーの登録
    """
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()
