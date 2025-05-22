from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
  id: Annotated[str, Field(..., description="Patient ID", example="P001")]
  name: Annotated[str, Field(..., description="Patient Name", example="Ananya Sharma")]
  city: Annotated[str, Field(..., description="Patient City", example="Guwahati")]
  age: Annotated[int, Field(..., gt=0, lt=120, description="Patient Age", example=28)]
  gender: Annotated[Literal["male", "female", "other"], Field(..., description="Patient Gender", example="female")]
  height: Annotated[float, Field(..., gt=0, description="Patient Height (in meters)", example=1.65)]
  weight: Annotated[float, Field(..., gt=0, description="Patient Weight (in kilograms)", example=90.0)]

  @computed_field
  @property
  def bmi(self) -> float:
    return round(self.weight / (self.height ** 2), 2)

  @computed_field
  @property
  def verdict(self) -> Literal["Underweight", "Normal", "Overweight", "Obese"]:
    if self.bmi < 18.5:
      return "Underweight"
    elif self.bmi < 25:
      return "Normal"
    elif self.bmi < 30:
      return "Overweight"
    else:
      return "Obese"

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

@app.post("/patients")
def create_patient(patient: Patient):
  data = load_data('patients.json')
  if patient.id in data:
    raise HTTPException(status_code=400, detail="Patient already exists")

  data[patient.id] = patient.model_dump(exclude={"id"})

  with open('patients.json', 'w') as f:
    json.dump(data, f)

  return JSONResponse(content={"message": "Patient created successfully", "patient": patient.model_dump()}, status_code=201)
