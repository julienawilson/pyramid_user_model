from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'usermodels'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    password = Column(Unicode)
    firstname = Column(Unicode)
    lastname = Column(Unicode)
    food = Column(Unicode)
    email = Column(Unicode)





# Index('my_index', MyModel.name, MyModel.password, unique=True, mysql_length=255)
