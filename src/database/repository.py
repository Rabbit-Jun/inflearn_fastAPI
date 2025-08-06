from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database.orm import ToDo
from typing import List

def get_todos(session: Session) -> list[ToDo]:

    return list(session.scalars(select(ToDo)))

def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))


def create_todo(session: Session, todo: ToDo) -> ToDo: # 생성한 orm 객체를 session에 추가하고 커밋합니다.
    session.add(instance =todo)
    session.commit() # db save
    session.refresh(instance=todo)  # db read 이 시점에 todo_id가 할당됨
    return todo


def update_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit() 
    session.refresh(instance=todo)
    return todo

def delete_todo(session: Session, todo_id: int) -> None:
    session.execute(delete(ToDo).where(ToDo.id == todo_id))  # delete 쿼리를 실행합니다.
    session.commit()  # 커밋을 통해 변경 사항을 데이터베이스에 반영합니다.
