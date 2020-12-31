# from flask_sqlalchemy import SQLAlchemy
# # from app import app
#
# db = SQLAlchemy()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db?'
                       'check_same_thread=false', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
