
from database.orm import ToDo





def test_health_check(client):
    response= client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}  

def test_get_todos(client, mocker ):

    mocker.patch("main.get_todos",return_value=[
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ]) #실제로 동작하지는 않지만 동작하는 것처럼
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {'todos': [
    {'id': 1,'contents': 'FastAPI Section 0',  'is_done': True},
    {'id': 2,'contents': 'FastAPI Section 1', 'is_done': False},

]} # 실제 데이터의 모든 값들을 다 넣어줘야 함 vscod에서 실험관 모형에서 test 해볼 수 있음(테스트를 위한 db또는 모킹을 만들어야 함)
    # order=DESC로 요청하면 역순으로 정렬된 결과를 반환하는지 확인
    response = client.get("/todos?order=desc") # main.py에서 get_todos_handler 함수가 호출됨

    assert response.status_code == 200
    assert response.json() == {'todos': [
    {'id': 2,'contents': 'FastAPI Section 1', 'is_done': False},
    {'id': 1,'contents': 'FastAPI Section 0',  'is_done': True},
        ]
        } # 위쪽에 문제가 생기면 여기까지 테스트 안됨 