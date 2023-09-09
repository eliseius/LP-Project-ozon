from sqlalchemy import Column, Integer, String, Date, Float
from db import Base, engine

class Currency (Base):
    __tablename__ = "currency"

    id = Column(Integer(), primary_key=True)
    date = Column(Date)
    currency = Column(String)
    value = Column(Float)

    def __repr__(self):
        return f"Currency id: {self.id}, date: {self.date}, value: {self.value}"


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)