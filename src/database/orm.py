from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from database.schema.request import CreateToDoRequest

Base = declarative_base()  # SQLAlchemy의 선언적 베이스 클래스를 생성합니다. 이 클래스는 ORM 모델의 기본 클래스가 됩니다.


class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(255), nullable=False)
    is_done = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Todo(id={self.id}, contents={self.contents}, is_done={self.is_done})>"
    # __repr__ 메서드는 객체의 문자열 표현을 정의합니다. 디버깅이나 로깅에 유용합니다.

    @classmethod
    def create(cls, request: CreateToDoRequest):
        return cls(
            contents=request.contents,
            is_done=request.is_done,

        ) # Create 메서드는 CreateToDoRequest 객체를 받아 ToDo 객체를 생성합니다.

    def done(self): # 데이터를 변경하는 경우에는 이렇게 메서드를 정의해서 사용합니다.
        self.is_done = True
        return self

    def undone(self):
        self.is_done = False
        return self