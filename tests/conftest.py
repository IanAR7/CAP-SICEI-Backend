import pytest  
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker  
from infrastructure.db.models import Base  
  
  
@pytest.fixture(scope="function")  
def db_session():  
    engine = create_engine("sqlite:///:memory:")  
    Base.metadata.create_all(engine)  
    SessionLocal = sessionmaker(bind=engine)  
    session = SessionLocal()  
      
    yield session  
      
    session.close()  
    Base.metadata.drop_all(engine)  
  
  
@pytest.fixture  
def sample_grade_data():  
    return {  
        "student_id": "S001",  
        "subject_id": "SUB001",  
        "value": 85.5  
    }