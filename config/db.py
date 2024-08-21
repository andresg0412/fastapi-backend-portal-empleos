from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:1234@localhost:3306/gestion_vacantes")
meta = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

conn = engine.connect()