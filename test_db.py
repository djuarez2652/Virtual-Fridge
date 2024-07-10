from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import requests
import pprint

'''engine = create_engine('sqlite:///stock_test.db')  # db for just testing basic adding and querying
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
    expiration_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"Stock('{self.food_name}', '{self.expiration_date}')"

Base.metadata.create_all(engine)


def insert_food(user_id, food_name, expiration_date):
    expiration_date = datetime.strptime(expiration_date, '%m-%d-%Y')
    new_item = Stock(user_id=user_id, food_name=food_name, expiration_date=expiration_date)
    session.add(new_item)
    session.commit()


def has_food(user_id):
    food_item = session.query(Stock).filter_by(user_id=user_id).all()
    return food_item

if __name__ == '__main__':
    insert_food(1, "fish", '12-30-2004')
    insert_food(1, "acorn", '12-30-2004')
    insert_food(1, "leaf", '12-30-2004')
    insert_food(1, "tree", '12-30-2004')
    # get a list of all the food someone has
    print(has_food(1))
'''

BASE_URL = 'https://api.edamam.com/api/recipes/v2'
APP_ID = 'd3661e3f'
APP_KEY = '1c75873f67d56f2a5c48a2b82f53cc56'

# ingredients_list = 

params = {
    'type' : 'public',
    'q' : ['fish', 'fruit'],
    'app_id' : APP_ID,
    'app_key' : APP_KEY,
}

response = requests.get(BASE_URL, params=params)
dict_format = response.json()

print(dict_format['hits'][0]['recipe']['ingredientLines'])  # list of ingredients
print(dict_format['hits'][0]['recipe']['label']) # recipe name
print(dict_format['hits'][0]['recipe']['shareAs']) # edamam recipe url
print(dict_format['hits'][0]['recipe']['url']) # original recipe url

#totaltime and totalweight are the last things for each recipe

#for ... in ingredients:
