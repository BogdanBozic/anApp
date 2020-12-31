# from db import db
from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from db import Base, session

from db import Base


class ItemModel(Base):
    __tablename__ = 'items'

    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    price = Column(Float(2), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    weight = Column(Float(2), nullable=False)
    notes = Column(String, nullable=True)

    def __init__(self, name, price, vendor_id, weight, notes):
        # self.id = _id
        self.name = name
        self.price = price
        self.vendor_id = vendor_id
        self.weight = weight
        self.notes = notes

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "vendor_id": self.vendor_id,
            "weight": self.weight,
            "notes": self.notes
        }

    @classmethod
    def get_items(cls):
        return session.query(cls).all()

    @classmethod
    def get_item_by_id(cls, _id):
        # return cls.query.filter_by(id=_id).first()
        return session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def get_items_by_name(cls, name):
        return session.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_item_by_name_and_vendor_id(cls, name, vendor_id):
        return session.query(cls).filter(cls.name == name, cls.vendor_id == vendor_id).first()

    @classmethod
    def get_item_by_multiple_parameters(cls, **kwargs):
        return session.query(cls).filter(cls.name == ItemModel.name)

    def add_to_db(self):
        session.add(self)
        session.commit()

