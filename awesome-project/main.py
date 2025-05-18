from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data(file):
  with open(file, 'r') as f:
    data = json.load(f)

  return data

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/patients")
def read_patients():
  data = load_data('patients.json')
  return data

@app.get("/patients/{patient_id}")
def read_patient(patient_id: str = Path(..., description="Patient ID", example="P001")):
  data = load_data('patients.json')
  if patient_id not in data:
    raise HTTPException(status_code=404, detail="Patient not found")
  return data[patient_id]

@app.get("/patients/sort/")
def sort_patients(sort_by: str = Query(..., description="Sort by age, height, bmi", example="age"), sort_order: str = Query("asc", description="Sort order", example="asc")):
  if sort_order not in ["asc", "desc"]:
    raise HTTPException(status_code=400, detail="Sort order must be asc or desc")

  if sort_by not in ["age", "height", "bmi"]:
    raise HTTPException(status_code=400, detail="Sort by must be age, height or bmi")

  data = load_data('patients.json')

  sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order == "desc")

  return sorted_data
