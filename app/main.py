from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import Base, engine, SessionLocal
from .models import Company, Job, Candidate
from .schemas import (
    CompanyCreate, CompanyOut, JobCreate, JobOut,
    CandidateCreate, CandidateOut
)
from .search import index_job, search_jobs, client

app = FastAPI(title="PlaceMux Marketplace API", version="1.0")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    db_ok = False
    search_ok = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        pass
    try:
        search_ok = bool(client().ping())
    except Exception:
        pass
    return {
        "status": "ok" if db_ok and search_ok else "degraded",
        "database": db_ok,
        "search": search_ok,
    }

@app.post("/companies", response_model=CompanyOut)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(name=payload.name, email=payload.email)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@app.get("/companies", response_model=list[CompanyOut])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).order_by(Company.id).all()

@app.post("/jobs", response_model=JobOut)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    company = db.get(Company, payload.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    job = Job(
        company_id=payload.company_id,
        title=payload.title,
        description=payload.description,
        skills=payload.skills,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    index_job(job)
    return job

@app.get("/jobs", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).order_by(Job.id).all()

@app.get("/jobs/search")
def search(q: str):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query is required")
    return search_jobs(q)

@app.post("/candidates", response_model=CandidateOut)
def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    candidate = Candidate(
        name=payload.name,
        email=payload.email,
        skills=payload.skills,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

@app.get("/candidates", response_model=list[CandidateOut])
def list_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).order_by(Candidate.id).all()
