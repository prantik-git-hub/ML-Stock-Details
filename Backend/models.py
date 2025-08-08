# app/models.py

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///results.db', connect_args={'check_same_thread': False})
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(10))
    latest_date = Column(Date)
    latest_close = Column(Float)
    previous_close = Column(Float)
    change = Column(Float)
    percent_change = Column(Float)
    pros = Column(String)
    cons = Column(String)
    sales_growth = Column(Float)
    profit_growth = Column(Float)
    roe = Column(Float)

    def __repr__(self):
        return f'<Result {self.ticker}>'

def init_db():
    Base.metadata.create_all(bind=engine)
