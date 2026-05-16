from datetime import datetime, timezone
from typing import Generator, Optional

from fastapi import Depends, FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./applications.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Applications API", version="1.0.0")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False)
    whatsapp_number = Column(String, nullable=False)
    university = Column(String, nullable=False)
    course = Column(String, nullable=False)
    level = Column(String, nullable=False)
    track = Column(String, nullable=False)
    motivation = Column(String, nullable=False)
    portfolio_link = Column(String, nullable=False)
    resume_link = Column(String, nullable=False)
    join_innovation_club = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="pending")
    submitted_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class ApplicationBase(BaseModel):
    fullName: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    whatsappNumber: str = Field(..., min_length=1)
    university: str = Field(..., min_length=1)
    course: str = Field(..., min_length=1)
    level: str = Field(..., min_length=1)
    track: str = Field(..., min_length=1)
    motivation: str = Field(..., min_length=1)
    portfolioLink: str = Field(..., min_length=1)
    resumeLink: str = Field(..., min_length=1)
    joinInnovationClub: bool
    status: str = "pending"


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsappNumber: Optional[str] = None
    university: Optional[str] = None
    course: Optional[str] = None
    level: Optional[str] = None
    track: Optional[str] = None
    motivation: Optional[str] = None
    portfolioLink: Optional[str] = None
    resumeLink: Optional[str] = None
    joinInnovationClub: Optional[bool] = None
    status: Optional[str] = None


class ApplicationRead(ApplicationBase):
    id: int
    submittedAt: datetime


seed_applications = [
    {
        "id": 2,
        "fullName": "Ama Serwaa Owusu",
        "email": "amaserwaa@gmail.com",
        "phone": "0245567812",
        "whatsappNumber": "0245567812",
        "university": "University of Ghana",
        "course": "Computer Engineering",
        "level": "2nd Year",
        "track": "Embedded Systems",
        "motivation": "I want to gain hands-on experience in embedded systems and IoT development.",
        "portfolioLink": "https://github.com/amase",
        "resumeLink": "https://linkedin.com/in/amase",
        "joinInnovationClub": True,
        "status": "accepted",
        "submittedAt": "2026-05-04T10:12:45Z",
    },
    {
        "id": 3,
        "fullName": "Yaw Mensah",
        "email": "yawmensah@gmail.com",
        "phone": "0558876123",
        "whatsappNumber": "0558876123",
        "university": "KNUST",
        "course": "Electrical Engineering",
        "level": "4th Year",
        "track": "Radar & RF Systems",
        "motivation": "To improve my knowledge in RF systems, radar engineering, and wireless communications.",
        "portfolioLink": "https://github.com/yawmensah",
        "resumeLink": "https://linkedin.com/in/yawmensah",
        "joinInnovationClub": True,
        "status": "pending",
        "submittedAt": "2026-05-05T08:45:30Z",
    },
    {
        "id": 4,
        "fullName": "Priscilla Adjei",
        "email": "priscilla.adjei@gmail.com",
        "phone": "0203344556",
        "whatsappNumber": "0203344556",
        "university": "Ashesi University",
        "course": "Software Engineering",
        "level": "3rd Year",
        "track": "Backend Engineering",
        "motivation": "I want to strengthen my backend engineering skills using FastAPI and modern software architecture.",
        "portfolioLink": "https://github.com/priscillaadjei",
        "resumeLink": "https://linkedin.com/in/priscillaadjei",
        "joinInnovationClub": True,
        "status": "accepted",
        "submittedAt": "2026-05-06T14:18:22Z",
    },
    {
        "id": 5,
        "fullName": "Daniel Kofi Asante",
        "email": "danielasante@gmail.com",
        "phone": "0277788990",
        "whatsappNumber": "0277788990",
        "university": "UENR",
        "course": "Biomedical Engineering",
        "level": "2nd Year",
        "track": "Biomedical Systems",
        "motivation": "To explore biomedical monitoring systems and healthcare technology innovations.",
        "portfolioLink": "https://github.com/danielasante",
        "resumeLink": "https://linkedin.com/in/danielasante",
        "joinInnovationClub": False,
        "status": "rejected",
        "submittedAt": "2026-05-07T11:05:10Z",
    },
]


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def application_to_read(application: Application) -> ApplicationRead:
    return ApplicationRead(
        id=application.id,
        fullName=application.full_name,
        email=application.email,
        phone=application.phone,
        whatsappNumber=application.whatsapp_number,
        university=application.university,
        course=application.course,
        level=application.level,
        track=application.track,
        motivation=application.motivation,
        portfolioLink=application.portfolio_link,
        resumeLink=application.resume_link,
        joinInnovationClub=application.join_innovation_club,
        status=application.status,
        submittedAt=application.submitted_at,
    )


def seed_database() -> None:
    with SessionLocal() as db:
        existing_count = db.query(Application).count()
        if existing_count:
            return

        for item in seed_applications:
            submitted_at = datetime.fromisoformat(item["submittedAt"].replace("Z", "+00:00"))
            application = Application(
                id=item["id"],
                full_name=item["fullName"],
                email=item["email"],
                phone=item["phone"],
                whatsapp_number=item["whatsappNumber"],
                university=item["university"],
                course=item["course"],
                level=item["level"],
                track=item["track"],
                motivation=item["motivation"],
                portfolio_link=item["portfolioLink"],
                resume_link=item["resumeLink"],
                join_innovation_club=item["joinInnovationClub"],
                status=item["status"],
                submitted_at=submitted_at,
            )
            db.add(application)

        db.commit()


Base.metadata.create_all(bind=engine)
seed_database()


@app.get("/")
def root():
    return {"message": "Applications API is running"}


@app.get("/applications", response_model=list[ApplicationRead])
def list_applications(db: Session = Depends(get_db)):
    applications = db.query(Application).order_by(Application.id).all()
    return [application_to_read(application) for application in applications]


@app.get("/applications/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: int = Path(..., description="The ID of the application to retrieve", gt=0),
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application_to_read(application)


@app.post("/applications", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    db_application = Application(
        full_name=application.fullName,
        email=application.email,
        phone=application.phone,
        whatsapp_number=application.whatsappNumber,
        university=application.university,
        course=application.course,
        level=application.level,
        track=application.track,
        motivation=application.motivation,
        portfolio_link=application.portfolioLink,
        resume_link=application.resumeLink,
        join_innovation_club=application.joinInnovationClub,
        status=application.status,
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return application_to_read(db_application)


@app.put("/applications/{application_id}", response_model=ApplicationRead)
def replace_application(
    application_id: int,
    application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    db_application = db.get(Application, application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db_application.full_name = application.fullName
    db_application.email = application.email
    db_application.phone = application.phone
    db_application.whatsapp_number = application.whatsappNumber
    db_application.university = application.university
    db_application.course = application.course
    db_application.level = application.level
    db_application.track = application.track
    db_application.motivation = application.motivation
    db_application.portfolio_link = application.portfolioLink
    db_application.resume_link = application.resumeLink
    db_application.join_innovation_club = application.joinInnovationClub
    db_application.status = application.status

    db.commit()
    db.refresh(db_application)
    return application_to_read(db_application)


@app.patch("/applications/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    db_application = db.get(Application, application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    updates = application.model_dump(exclude_unset=True) if hasattr(application, "model_dump") else application.dict(exclude_unset=True)
    field_map = {
        "fullName": "full_name",
        "email": "email",
        "phone": "phone",
        "whatsappNumber": "whatsapp_number",
        "university": "university",
        "course": "course",
        "level": "level",
        "track": "track",
        "motivation": "motivation",
        "portfolioLink": "portfolio_link",
        "resumeLink": "resume_link",
        "joinInnovationClub": "join_innovation_club",
        "status": "status",
    }

    for key, value in updates.items():
        setattr(db_application, field_map[key], value)

    db.commit()
    db.refresh(db_application)
    return application_to_read(db_application)


@app.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = db.get(Application, application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(db_application)
    db.commit()
    return None