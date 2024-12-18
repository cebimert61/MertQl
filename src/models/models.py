from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Models will be defined based on your MSSQL database schema
# Example:
# class YourModel(Base):
#     __tablename__ = 'your_table'
#     # Define your columns here
