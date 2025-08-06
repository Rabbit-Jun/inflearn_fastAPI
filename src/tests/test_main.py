
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

def test_get_todo(client, mocker):
    mocker.patch("main.get_todo_by_todo_id", return_value=ToDo(id=1, contents="todo", is_done=True))
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'contents': 'todo', 'is_done': True}

    #404
    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}

def test_create_todo(client, mocker):
    create_spy = mocker.spy(ToDo, "create") # main.py에서 create_todo_handler 함수를 실제로 실행하면서 감시
    mocker.patch("main.create_todo", return_value=ToDo(id=1, contents="todo", is_done=False))
    body ={
        "contents": "test",
        "is_done": False,
    } # mocking이랑 달라도 테스트 통과됨
    response = client.post("/todos", json= body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {'id': 1, 'contents': 'todo', 'is_done': False}

def test_update_todo(client, mocker):
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

def test_update_todo(client, mocker):
    mocker.patch("main.get_todo_by_todo_id", return_value=ToDo(id=1, contents="todo", is_done=True))
    undone = mocker.patch.object(ToDo, "undone")
    mocker.patch("main.update_todo", return_value=ToDo(id=1, contents="todo", is_done=False))
    response = client.patch("/todos/1", json={"is_done": False})

    undone.assert_called_once_with()  # undone 메서드가 호출되었는지 확인

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'contents': 'todo', 'is_done': False}

    #404
    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.patch("/todos/1", json={"is_done": True})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}

def test_delete_todo(client, mocker):
    #204
    mocker.patch("main.get_todo_by_todo_id", return_value=ToDo(id=1, contents="todo", is_done=True))
    mocker.patch("main.delete_todo", return_value=None)  # delete_todo 함수가 실제로 동작하지 않도록 Mock
    response = client.delete("/todos/1")
    assert response.status_code == 204
    

    #404
    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}