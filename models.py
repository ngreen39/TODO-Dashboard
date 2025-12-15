from sqlalchemy import *
from database import *
from datetime import *

class Todo(Base):
    __tablename__ = "personal_todo"

    id = Column(Integer, primary_key=True, index=True)
    task_body = Column(String(500), nullable=False)
    due_day = Column(Integer, nullable=False)
    due_month = Column(String(20), nullable=False)
    due_year = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    priority = Column(String(20), default="medium")
    category = Column(String(50), default="general")

