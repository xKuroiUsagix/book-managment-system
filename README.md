# Come Back Agency Test Task
## Task Description

Develop a feature-rich book management system using FastAPI for the backend and a PostgreSQL database for storage. The system should go beyond basic CRUD operations and include additional features to demonstrate expertise in software architecture, optimization, and testing.

## Local Setup

1. Create virtual environment with `python -m venv venv`. Python version used is `13.3.0`
2. Run command `pip install -r requirements.txt`
3. Create `.env` file in project directory with `DATABASE_URL=postgresql://user:password@localhost/database`
4. Run `create_tables.py` once to create tables in your DB
5. Run server using command `uvicorn app.main:app --reload`

After these steps, the server should be running successfully.

## API Docs

When server is runing you can check API documentation by going to http://127.0.0.1:8000/docs#/
