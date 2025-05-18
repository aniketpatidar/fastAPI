# FastAPI Project

This is a FastAPI-based web application that includes basic endpoints for managing patients data.

## Project Structure

```

fastAPI-project/
├── main.py
├── patients.json
├── requirements.txt
└── README.md

```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/aniketpatidar/fastAPI-project.git
```
2. Navigate to the project directory:

```bash
cd fastAPI-project
```
3. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

2. **Run the application**

```bash
uvicorn main:app --reload
```

## API Endpoints

* `GET /` — Health check
* `GET /patients` — Retrieve all patients
* `GET /patients/{patient_id}` — Retrieve a patient by ID
* `GET /patients/sort/` — Sort patients by `age`, `height`, or `bmi`

## Example Query

```bash
curl "http://127.0.0.1:8000/patients/sort/?sort_by=age&sort_order=desc"
```
