import os
import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session



engine = create_engine(os.environ['DB_POSTGRESQL']) # create_engine(settings.ADDRES_POSTGRESQL)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()