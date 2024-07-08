from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///stock_test.db')  # db for just testing basic adding and querying
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    user_id = Column(Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    food_name = Column(String(100), nullable=False)
    expiration_date = Column(String(100), nullable=False)

    def __repr__(self):
        return f"Stock('{self.food_name}', '{self.expiration_date}')"

Base.metadata.create_all(engine)


def insert_food(user_id, food_name, expiration_date):
    new_item = Stock(user_id=user_id, food_name=food_name, expiration_date=expiration_date)
    session.add(new_item)
    session.commit()


def has_food(user_id, food_name):
    food_item = session.query(Stock).filter_by(user_id=user_id, food_name=food_name).first()
    return food_item

if __name__ == '__main__':
    insert_food(1, "fish", "march")
    print(has_food(1, "fish"))  # should return 'fish'
    print(has_food(1, "chicken"))  # should return none


