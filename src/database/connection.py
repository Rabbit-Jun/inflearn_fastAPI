from sqlalchemy import create_engine #sql에 접속하기 위한 엔진을 생성하는 모듈
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://root:todos@127.0.1:3306/todos"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True는 SQLAlchemy가 실행하는 SQL 쿼리를 로그로 출력합니다.
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 세션 팩토리를 생성합니다. 이 팩토리는 데이터베이스와의 세션을 관리합니다.


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
# get_db 함수는 FastAPI의 의존성 주입 시스템에서 사용할 수 있는 데이터베이스 세션을 생성합니다.