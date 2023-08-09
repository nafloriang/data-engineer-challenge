from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Definición de modelos
class HiredEmployee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    datetime = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String)

# Establecer conexión con la base de datos
DATABASE_URL = "sqlite:///mydatabase.db"
engine = create_engine(DATABASE_URL)

# Crear las tablas
Base.metadata.create_all(engine)

print("Tablas creadas exitosamente!")
