from db import Base, session
from sqlalchemy import Integer, String, Date, ForeignKey, Column
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import relationship, backref


class VendorModel(Base):
    __tablename__ = 'vendors'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    phone_number = Column(Integer, nullable=False, unique=True)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, unique=True, nullable=False)
    notes = Column(String, nullable=True)

    # items = relationship('Item', backref=backref('vendors'))

    def __init__(self, name, phone_number, email, address, notes):
        # self.id = _id
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.notes = notes

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            "notes": self.notes
        }

    @classmethod
    def query_vendor_by_id(cls, id):
        # return cls.query.filter_by(id=_id).first()
        return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def query_vendor_by_kwargs(cls, **kwargs):
        try:
            list_of_vendors = session.query(cls).filter_by(**kwargs).all()
        except InvalidRequestError as e:
            error = e._message()
            return error[-6:]
        return cls.jsonify_list_of_vendors(list_of_vendors)

    @classmethod
    def jsonify_vendor(cls, vendor):
        return {
            "name": cls.name,
            "phone_number": cls.phone_number,
            "email": cls.email,
            "address": cls.address,
            "notes": cls.notes
        }

    @classmethod
    def jsonify_list_of_vendors(cls, list_of_vendors):
        dict_of_vendors = {'vendors': []}
        for element in list_of_vendors:
            dict_of_vendors['vendors'].append(element.json())
        return dict_of_vendors

    @classmethod
    def query_vendors(cls):
        list_of_vendors = session.query(cls).all()
        return cls.jsonify_list_of_vendors(list_of_vendors)

    @classmethod
    def check_if_vendor_exists(cls, name, phone_number, email, address):
        if session.query(cls).filter(cls.name == name).first():
            return False, "name"
        elif session.query(cls).filter(cls.phone_number == phone_number).first():
            return False, "phone_number"
        elif session.query(cls).filter(cls.email == email).first():
            return False, "email"
        elif session.query(cls).filter(cls.address == address).first():
            return False, "address"
        else:
            return True, ''

    def add_to_db(self):
        session.add(self)
        session.commit()

    def put_to_db(self):

