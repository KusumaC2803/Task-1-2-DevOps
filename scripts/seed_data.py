from app.database import Base, engine, SessionLocal
from app.models import Company, Job, Candidate
from app.search import index_job

Base.metadata.create_all(bind=engine)
db = SessionLocal()

company = db.query(Company).filter_by(email="hr@placemux-demo.example").first()
if not company:
    company = Company(name="PlaceMux Demo Company", email="hr@placemux-demo.example")
    db.add(company)
    db.commit()
    db.refresh(company)

jobs = [
    ("Python Backend Developer", "Build APIs with Python FastAPI and PostgreSQL", ["python", "fastapi", "postgresql"]),
    ("Data Analyst", "Work with SQL, Excel and dashboards", ["sql", "excel", "powerbi"]),
    ("Frontend Developer", "Build React applications and reusable UI", ["react", "javascript", "html"]),
]

for title, description, skills in jobs:
    existing = db.query(Job).filter_by(title=title, company_id=company.id).first()
    if not existing:
        job = Job(company_id=company.id, title=title, description=description, skills=skills)
        db.add(job)
        db.commit()
        db.refresh(job)
        index_job(job)

candidate = db.query(Candidate).filter_by(email="candidate@demo.example").first()
if not candidate:
    db.add(Candidate(
        name="Demo Candidate",
        email="candidate@demo.example",
        skills=["python", "sql", "fastapi"]
    ))
    db.commit()

db.close()
print("Demo data is ready.")
