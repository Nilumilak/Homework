from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import configparser
import json

config = configparser.ConfigParser()
config.read('settings.ini')

user = config['DB']['user']
password = config['DB']['password']
db_name = config['DB']['db_name']

Base = declarative_base()

engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{db_name}', echo=True)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=100), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)

    publisher = relationship(Publisher, backref='book')


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(String(10), nullable=False)
    date_sale = Column(DateTime, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    count = Column(Integer, nullable=False)

    stock = relationship(Stock, backref='sale')


def create_tables(engine):
    Base.metadata.create_all(engine)


create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publishers = []
books = []
shops = []
stocks = []
sales = []

with open('data.json') as file:
    data = json.load(file)

for row in data:
    if row['model'] == 'publisher':
        publishers.append(Publisher(name=row['fields']['name']))
    elif row['model'] == 'book':
        books.append(Book(title=row['fields']['title'], id_publisher=row['fields']['id_publisher']))
    elif row['model'] == 'shop':
        shops.append(Shop(name=row['fields']['name']))
    elif row['model'] == 'stock':
        stocks.append(Stock(id_book=row['fields']['id_book'], id_shop=row['fields']['id_shop'],
                            count=row['fields']['count']))
    elif row['model'] == 'sale':
        sales.append(Sale(price=row['fields']['price'], date_sale=row['fields']['date_sale'],
                          id_stock=row['fields']['id_stock'], count=row['fields']['count']))

session.add_all(publishers)
session.add_all(books)
session.add_all(shops)
session.add_all(stocks)
session.add_all(sales)
session.commit()


def select_publisher():
    pb = input('Input id or name of a publisher: ')
    for row in (session.query(Publisher, Book, Stock, Shop)
            .filter(Book.id_publisher == Publisher.id)
            .filter(Stock.id_book == Book.id)
            .filter(Shop.id == Stock.id_shop)
            .filter(Publisher.id == int(pb) if pb.isdigit() else Publisher.name == id).distinct(Shop.name)):
        print(row.Publisher.id, row.Publisher.name, '-', row.Shop.name)


select_publisher()
