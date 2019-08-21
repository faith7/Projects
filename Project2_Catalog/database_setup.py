import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False)
    profile_pic = Column(String)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    genre = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# return JSON object
@property
def serialize(self):
    return {
        'id': self.id,
        'genre': self.name
    }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    show = Column(String)
    title = Column(String, nullable=False)
    description = Column(String)
    release = Column(String)
    img = Column(String)

    category = relationship(
        Category, backref=backref("item", lazy=True))
    category_id = Column(Integer, ForeignKey('category.id'))

    user = relationship(User, backref=backref("user", lazy=True))
    user_id = Column(Integer, ForeignKey('user.id'))


# return JSON object
@property
def serialize(self):
    return{
        'id': self.id,
        'show': self.show,
        'title': self.title,
        'description': self.description,
        'release': self.release,
        'img': self.img
    }


engine = create_engine('sqlite:///itemcatalog.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
