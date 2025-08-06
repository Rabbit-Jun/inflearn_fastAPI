from fastapi.testclient import TestClient

from  main import app


client = TestClient(app=app) # main.py에서 FastAPI 인스턴스를 가져와서 테스트 클라이언트 생성


def test_health_check():
    response= client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}  

def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {'todos': [
    {'contents': 'FastAPI Section 0', 'id': 1, 'is_done': True},
    {'contents': 'FastAPI Section 1', 'id': 2, 'is_done': True},
    {'contents': 'FastAPI Section 2', 'id': 3, 'is_done': False},
    {'contents': 'test', 'id': 5, 'is_done': True},
    {'contents': 'testg', 'id': 6, 'is_done': True}
]} # 실제 데이터의 모든 값들을 다 넣어줘야 함 vscod에서 실험관 모형에서 test 해볼 수 있음
    # order=DESC로 요청하면 역순으로 정렬된 결과를 반환하는지 확인
    response = client.get("/todos?order=desc") # main.py에서 get_todos_handler 함수가 호출됨
    assert response.status_code == 200
    assert response.json() == {'todos': [
        {'contents': 'testg', 'id': 6, 'is_done': True},
        {'contents': 'test', 'id': 5, 'is_done': True},
        {'contents': 'FastAPI Section 2', 'id': 3, 'is_done': False},
        {'contents': 'FastAPI Section 1', 'id': 2, 'is_done': True},
        {'contents': 'FastAPI Section 0', 'id': 1, 'is_done': True},
        ]
        } # 위쪽에 문제가 생기면 여기까지 테스트 안됨 