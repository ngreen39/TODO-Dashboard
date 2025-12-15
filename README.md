# Todo List Manager & Business Intelligence Prototype
A full-stack, data-driven application demonstrating proficiency across API design, database persistence, and data visualization.

### Tech Stack
+Backend API: FastAPI (RESTful CRUD)
+Database: SQLAlchemy / MySQL (Persistent Storage)
+Analytics: Pandas / Seaborn (Data Transformation & Visualization)

### Quick Setup

git clone [YOUR_REPO_URL]
cd [repo-name]
Install & Configure:

### Install dependencies
pip install -r requirements.txt

## Configure your DB credentials in a local .env file
Run Pipeline: Execute these three commands in order

### 1. Initialize DB tables and add 100 sample tasks
python seed.py

### 2. Start the API server (API docs @ http://127.0.0.1:8000/docs)
uvicorn main:app --reload 

### 3. Run the analytics script to generate charts/KPIs
python analytics.py
