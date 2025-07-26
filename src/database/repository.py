from sqlalchemy.orm import Session
from sqlalchemy import select
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
