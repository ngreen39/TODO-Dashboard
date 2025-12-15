import random
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Make sure tables exist
models.Base.metadata.create_all(bind=engine)

# Sample data to choose from
tasks = [
    "Finish report", "Call client", "Prepare presentation", 
    "Clean inbox", "Update project plan", "Review code", 
    "Plan team meeting", "Organize files", "Backup database",
    "Write documentation"
]
months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]
priorities = ["low", "medium", "high"]
categories = ["work", "personal", "school", "misc"]

# Number of todos to create
NUM_TODOS = 100

def random_date(years=[2025, 2026]):
    day = random.randint(1, 28)  # keep it safe for all months
    month = random.randint(1, 12)
    year = random.choice(years)
    return datetime(year, month, day).date()  # returns date without time

def generate_todos():
    db: Session = SessionLocal()
    try:
        for _ in range(NUM_TODOS):
            due_year = random.choice([0, 2025, 2026])
            if due_year == 0:
                due_year = 2025  # default year if 0

            todo = models.Todo(
                task_body=random.choice(tasks),
                due_day=random.randint(1, 28),
                due_month=random.choice(months),
                due_year=due_year,
                priority=random.choice(priorities),
                category=random.choice(categories),
                completed_at=random_date() if random.random() < 0.5 else None
            )
            db.add(todo)
        db.commit()
        print(f"Inserted {NUM_TODOS} todos successfully.")
    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    generate_todos()