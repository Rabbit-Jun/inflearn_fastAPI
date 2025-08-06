import pytest

from fastapi.testclient import TestClient
from main import app


@pytest.fixture # 여러곳에서 사용 가능하게 만듬
def client():
    return TestClient(app=app)
