from sqlalchemy.orm import Session
import models, schemas

# Get all companies
def get_companies(db: Session):
    return db.query(models.Company).all()

# Create a new company
def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name, location=company.location)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

# Delete a company by ID
def delete_company(db: Session, company_id: int) -> bool:
    db_company = db.query(models.Company).filter(models.Company.company_id == company_id).first()
    if db_company:
        db.delete(db_company)
        db.commit()
        return True
    return False

# Update company by ID
def update_company(db: Session, company_id: int, updated_data: schemas.CompanyCreate):
    db_company = db.query(models.Company).filter(models.Company.company_id == company_id).first()
    if db_company:
        db_company.name = updated_data.name
        db_company.location = updated_data.location
        db.commit()
        db.refresh(db_company)
        return db_company
    return None
