from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mssql+pyodbc://@\\SQLEXPRESS/EmployeeDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

# Session
SessionLocal = sessionmaker(bind=engine)

# Metadata
metadata = MetaData()

# Table
employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("department", String(100)),
    Column("salary", Integer),
)

# Create Table
metadata.create_all(engine)