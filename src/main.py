from typing import List
from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.repository import create_todo, delete_todo, get_todo_by_todo_id, get_todos, update_todo
from database.orm import ToDo
from database.schema.response import ListToDoResponse, ToDoSchema
from database.schema.request import CreateToDoRequest


app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}



@app.get("/todos", status_code=200) # status_code는 200이 기본값이라 생략 가능
def get_todos_handler(order: str | None = None,
                      session: Session = Depends(get_db)): # str | None = None 하면 값을 필수적으로 안 넣어도 됨
    
    todos: List[ToDo] = get_todos(session=session)

    if order == "desc":
        return ListToDoResponse(todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]])
    return ListToDoResponse(todos=[ToDoSchema.model_validate(todo) for todo in todos]) # ListToDoResponse는 Pydantic 모델로, todos를 리스트로 감싸서 반환

@app.get("/todos/{todo_id}")
def get_todo_handler(todo_id: int,
                     session: Session = Depends(get_db)) -> ToDoSchema: # todo_id는 경로 매개변수로 받음, Depends()가 뭔지 모르겠네
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id) # get_todo_by_todo_id는 데이터베이스에서 todo를 가져오는 함수
    
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo not found") # HTTPException을 사용해서 에러를 발생시킬 수 있음



@app.post("/todos", status_code=201) # status_code는 201 Created로 설정
def create_todo_handler(request: CreateToDoRequest,
                        session: Session = Depends(get_db)) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request) # id = None이므로, 데이터베이스에 저장할 때 id가 자동으로 할당됨
    todo: ToDo = create_todo(session=session, todo=todo) # id 에 int가 할당됨


    return ToDoSchema.model_validate(todo) # Pydantic 모델로 변환해서 반환


@app.patch("/todos/{todo_id}") # 라우트 경로의 시작은 항상 /로 시작해야 함
def update_todo_handler(todo_id: int,
                        is_done: bool =Body(..., embed=True),
                        session: Session =Depends(get_db)): # 하나의 값을 받을 수 있음
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id) # get_todo_by_todo_id는 데이터베이스에서 todo를 가져오는 함수
    
    if todo:
        todo.done() if is_done else todo.undone() # 삼항연산자
        todo: ToDo = update_todo(session=session, todo=todo)

        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo not found") 
 

@app.delete("/todos/{todo_id}", status_code=204) # 204 No Content 응답을 보내고 싶을 때 사용
def delete_todo_handler(todo_id: int,
                        session: Session = Depends(get_db)):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id) # get_todo_by_todo_id는 데이터베이스에서 todo를 가져오는 함수
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    delete_todo(session=session, todo_id=todo_id) # delete_todo는 데이터베이스에서 todo를 삭제하는 함수

