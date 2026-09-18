# AI Book Reader Backend

A modern, fast, and robust backend built with **FastAPI** and **SQLAlchemy** for an interactive, audio-synced book reader application.

The core feature of this application is rendering PDF books with an interactive frontend text layer that synchronizes with MP3 audiobooks, allowing users to click a word in the PDF and jump directly to its spoken timestamp in the audio file.

---

## 🚀 Key Features

* **PDF Upload & Page Counting**: Save uploaded PDF files to the local disk and automatically extract their page count using `PyPDF2` at the moment of upload.
* **Safe Duplicate Handling**: Automatically rename duplicate uploads (e.g., `book.pdf` becomes `book_1.pdf`) while safely keeping the `.pdf` extension intact.
* **Robust CRUD Operations**:
  * Retrieve a user's entire library or query metadata for a single PDF.
  * Safely delete books from the PostgreSQL database and clean up the associated physical files on disk without risking orphaned database records.
* **Automatic Database Initialization**: Checks and initializes the database tables automatically when the server starts.
* **Dockerized Database**: Easy setup of the PostgreSQL database using Docker Compose.

---

## 🛠️ Tech Stack

* **Language**: Python 3
* **Framework**: FastAPI (Asynchronous Web API)
* **ORM**: SQLAlchemy (Declarative mapping)
* **Database**: PostgreSQL (via Docker)
* **PDF Processing**: PyPDF2 / pypdf

---

## 📂 Directory Structure

* [main.py](file:///c:/Users/tymek/PycharmProjects/PythonProject6/main.py) — The FastAPI entry point containing routes, endpoints, and request lifecycles.
* [database.py](file:///c:/Users/tymek/PycharmProjects/PythonProject6/database.py) — Database connections, session generators, and the `PDF` SQLAlchemy model.
* [config.py](file:///c:/Users/tymek/PycharmProjects/PythonProject6/config.py) — Application configuration management using Pydantic Settings.
* [pdfPageCounter.py](file:///c:/Users/tymek/PycharmProjects/PythonProject6/pdfPageCounter.py) — Helper utility to read and extract page counts from PDF files.
* [docker-compose.yml](file:///c:/Users/tymek/PycharmProjects/PythonProject6/docker-compose.yml) — PostgreSQL service container definition.
* `.env` — Environment configurations (DB user, passwords, ports, etc.).

---

## 🚦 How to Run the App

### 1. Spin up the Database
Make sure Docker is running on your machine, then run:
```bash
docker-compose up -d
```

### 2. Set Up the Virtual Environment
Activate your virtual environment:
```powershell
# On Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Install any required dependencies:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic-settings python-multipart PyPDF2
```

### 3. Run the FastAPI Server
Start Uvicorn in reload/development mode:
```bash
uvicorn main:app --reload
```

### 4. Open Interactive API Documentation
Once the server is running, navigate to:
* **Swagger UI Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Redoc Docs:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---
