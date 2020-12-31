from db import Base, session
from sqlalchemy import Column, Integer, String


class CustomerModel(Base):
    __tablename__ = 'customers'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, unique=True, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    phone_number = Column(Integer, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    def __init__(self, first_name, last_name, phone_number, email, address, notes):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.notes = notes

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            "notes": self.notes
        }

    @classmethod
    def get_customers(cls):
        return session.query(cls).all()

    @classmethod
    def get_customer_by_id(cls, _id):
        return session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def get_customers_by_first_name(cls, first_name):
        return session.query(cls).filter(cls.first_name == first_name).all()

    @classmethod
    def get_customers_by_last_name(cls, last_name):
        return  session.query(cls).filter(cls.last_name == last_name).all()

    @classmethod
    def get_customer_by_phone_number(cls, phone_number):
        return session.query(cls).query.filter(cls.phone_number == phone_number).first()

    @classmethod
    def get_customer_by_email(cls, email):
        return session.query(cls).filter(cls.email == email).first()

    def add_to_db(self):
        session.add(self)
        session.commit()

