from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"status": "ok"}


todo_data ={
    1: {"id": 1, "contents": "Buy ", "is_done": True},
    2: {"id": 2, "contents": "groceries", "is_done": False},
    3: {"id": 3, "contents": "Buy groceries", "is_done": True},

}

@app.get("/todos")
def get_todos_handler(order: str | None = None):
    ret = list(todo_data.values())
    if order == "desc":
        return ret[::-1]
    return ret

@app.get("/todos/{todo_id}")
def get_todo_handler(todo_id: int): # int값 불러오라고 해놓고 todo_data는 srt한 바보
    return todo_data.get(todo_id, {})

