import csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department = Column(String)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job = Column(String)

class HiredEmployee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

DATABASE_URL = "sqlite:///mydatabase.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def load_csv_to_db(session, model, csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar el encabezado
        for row in reader:
            instance = model(**{
                column.name: value for column, value in zip(model.__table__.columns, row)
            })
            session.add(instance)

def main():
    # Crear una nueva sesión
    session = SessionLocal()

    # Cargar datos desde los CSVs
    load_csv_to_db(session, Department, 'departments.csv')
    load_csv_to_db(session, Job, 'jobs.csv')
    load_csv_to_db(session, HiredEmployee, 'hired_employees.csv')

    # Confirmar cambios
    session.commit()

    # Cerrar la sesión
    session.close()

if __name__ == '__main__':
    main()
