from fastapi import *
from sqlalchemy.orm import *
from database import *
from models import *
from pydantic import *
from typing import *
from fastapi.encoders import *
import models
from datetime import datetime


# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# -------------------------------
# Pydantic models
# -------------------------------
class TodoBase(BaseModel):
    task_body: str
    due_day: int
    due_month: str
    due_year: int
    priority: str = "medium"
    category: str = "general"

class TodoCreate(BaseModel):
    task_body: str
    due_day: int
    due_month: str
    due_year: int

# ----------------------pydant---------
# POST: Create a new todo
# -------------------------------
@app.post("/todos/", response_model=TodoBase, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoBase, db: Session = Depends(get_db)):
    if todo.due_year == 0:
        todo.due_year = 2025
    new_todo = models.Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# -------------------------------
# GET: Fetch all todos
# -------------------------------
@app.get("/todos/", response_model=List[TodoBase], status_code=status.HTTP_200_OK)
def list_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoBase)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_item

# -------------------------------
# PUT: Update a todo by ID
# -------------------------------
@app.put("/todos/{todo_id}", response_model=TodoBase)
def update_todo(todo_id: int, todo_request: TodoBase, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id)
    if not db_todo.first():
        raise HTTPException(status_code=404, detail="Todo not found")
    update_data = todo_request.dict(exclude_unset=True)
    if update_data.get("due_year") == 0:
        update_data["due_year"] = 2025
    db_todo.update(update_data, synchronize_session=False)
    db.commit()
    return db_todo.first()

# -------------------------------
# DELETE: Remove a todo by ID
# -------------------------------
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id)
    if not db_todo.first():
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"Todo with ID {todo_id} deleted successfully"}

# -------------------------------
# Filter todos
# -------------------------------
@app.get("/todos/filter/", response_model=List[TodoBase])
def filter_todos(priority: str = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Todo)
    if priority:
        query = query.filter(models.Todo.priority == priority)
    if category:
        query = query.filter(models.Todo.category == category)
    return query.all()

# -------------------------------
# Mark todo complete
# -------------------------------
@app.patch("/todos/{todo_id}/complete", response_model=TodoBase)
def mark_todo_complete(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.completed_at = date
    db.commit()
    db.refresh(db_todo)
    return db_todo