from models import Base
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with React URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/companies/", response_model=list[schemas.Company])
def read_companies(db: Session = Depends(get_db)):
    return crud.get_companies(db)

@app.post("/companies/", response_model=schemas.Company)
def add_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db, company)

@app.put("/companies/{company_id}", response_model=schemas.Company)
def update_company(company_id: int, company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = crud.update_company(db, company_id, company)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    success = crud.delete_company(db, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Deleted successfully"}
