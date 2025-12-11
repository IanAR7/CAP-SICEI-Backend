import sys
import os
import random
from faker import Faker
from sqlalchemy import Column, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

try:
    from infrastructure.db.database import DATABASE_URL
except ImportError:
    print("No se pudo importar DATABASE_URL. Asegúrate de configurar tus variables de entorno.")
    sys.exit(1)
NUM_RECORDS = 50
Base = declarative_base()

class StudentRiskTestDataset(Base):
    __tablename__ = 'Student_Risk_Test_Dataset'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
   
    internet_home = Column(Integer, nullable=False)        
    has_laptop = Column(Integer, nullable=False)           
    is_female = Column(Integer, nullable=False)            
    age = Column(Integer, nullable=False)
    works = Column(Integer, nullable=False)                
    num_people_home = Column(Integer, nullable=False)
    prev_school_public = Column(Integer, nullable=False)   
    finished_prev_school = Column(Integer, nullable=False) 
    repeated_subjects = Column(Integer, nullable=False)    
    work_hours = Column(Float, nullable=False)
           
def run():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    fake = Faker()
    session = SessionLocal()
    
    try:
        new_records = []
        for _ in range(NUM_RECORDS):
            works_val = random.choices([0, 1], weights=[0.6, 0.4])[0]
            work_hours_val = 0.0
            if works_val == 1:
                work_hours_val = round(random.uniform(5.0, 40.0), 1)

            record = StudentRiskTestDataset(
                internet_home=random.choices([0, 1], weights=[0.3, 0.7])[0],
                has_laptop=random.choices([0, 1], weights=[0.4, 0.6])[0],
                is_female=random.choices([0, 1], weights=[0.5, 0.5])[0],
                age=fake.random_int(min=17, max=25),
                works=works_val,
                num_people_home=fake.random_int(min=1, max=8),
                prev_school_public=random.choice([0, 1]),
                finished_prev_school=random.choices([0, 1], weights=[0.1, 0.9])[0],
                repeated_subjects=random.choices([0, 1], weights=[0.8, 0.2])[0],
                work_hours=work_hours_val
            )
            new_records.append(record)
        
        session.add_all(new_records)
        session.commit()
        print(f"Éxito: Se han insertado {len(new_records)} registros en '{StudentRiskTestDataset.__tablename__}'.")
        
    except Exception as e:
        session.rollback()
        print(f"Error durante la inserción: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run()
