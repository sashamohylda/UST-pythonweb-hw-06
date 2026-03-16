# HW06 — University Database

## Stack
- Python 3.10+
- PostgreSQL (via Docker)
- SQLAlchemy 2.x ORM
- Alembic (migrations)
- Faker (seed data)
- argparse (CLI)

## Setup

### 1. Start PostgreSQL via Docker
```bash
docker run --name university-db -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply migrations
```bash
alembic upgrade head
```

### 4. Seed the database
```bash
python seed.py
```

### 5. Run queries
```bash
python my_select.py
```

## CLI Usage
```bash
python main.py -a create -m Teacher -n 'Boris Johnson'
python main.py -a list -m Teacher
python main.py -a update -m Teacher --id 3 -n 'Andry Bezos'
python main.py -a remove -m Teacher --id 3
python main.py -a create -m Group -n 'AD-101'
python main.py -a create -m Student -n 'John Doe' --group_id 1
python main.py -a create -m Subject -n 'Physics' --teacher_id 2
```

## Database Schema
- **groups** — student groups
- **teachers** — teachers
- **students** — students (belong to a group)
- **subjects** — subjects (each has a teacher)
- **grades** — grades (student + subject + date + score)
