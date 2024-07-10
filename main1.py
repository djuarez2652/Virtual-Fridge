from flask import Flask, render_template, url_for, redirect, request
from forms import RegistrationForm, LoginForm, addStockForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import subprocess
import signal
from datetime import datetime
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '83d6f0aedb63b08422f3b396f423f79c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'  # database filename
db = SQLAlchemy(app)
proxied = FlaskBehindProxy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):  # Represents table for a single user, can change if using different thing
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.username}')"


class Stock(db.Model):  # Represents a food table storing all the food and expiration dates, each associated with a user id
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    food_name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)


    def __repr__(self):
        return f"Food('{self.food_name}', '{self.expiration_date}')"

with app.app_context():
  db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")      
@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('stock'))
        else:
            logout_user()
            return render_template('login.html', form=login_form, incorrect=True)

    return render_template('login.html', subtitle='Login Page', form=login_form, incorrect=False)


@app.route("/register", methods=['GET', 'POST'])
def register():  # change if using different register thing
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User(username=reg_form.username.data, password=reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('stock'))
    
    return render_template('register.html', title='Register', form=reg_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/stock", methods=['GET', 'POST'])
@login_required
def stock():
    add_stock_form = addStockForm()
    if add_stock_form.validate_on_submit():
        food_name = add_stock_form.item_name.data
        expiration_date = add_stock_form.expire_date.data
        user_id = current_user.id
        insert_food(user_id, food_name, expiration_date)
        print(has_food(user_id))
        return redirect(url_for("stock"))
    return render_template('stock.html', form=add_stock_form, stock_query=query_stock(current_user.id))

# special URL for removal of stock item
@app.route("/remove_stock", methods=['GET'])
def remove_stock():
  item_name = request.args['item_name']
  remove_food(current_user.id, item_name)

  return redirect(url_for('stock'))

@app.route("/recipes")
@login_required
def recipes():

  # get ingredients, if any
  ingredients = request.args.getlist('ingredient')

  '''if ingredients:
    BASE_URL = 'https://api.edamam.com/api/recipes/v2'
    APP_ID = 'd3661e3f'
    APP_KEY = '1c75873f67d56f2a5c48a2b82f53cc56'
    
    params = {
        'type' : 'public',
        'q' : ingredients,
        'app_id' : APP_ID,
        'app_key' : APP_KEY,
    }

    response = requests.get(BASE_URL, params=params)
    recipe_dict = response.json()

    # check if recipe actually found:

    print(dict_format['hits'][0]['recipe']['ingredientLines'])  # list of ingredients
    print(dict_format['hits'][0]['recipe']['label']) # recipe name
    print(dict_format['hits'][0]['recipe']['shareAs']) # edamam recipe url
    print(dict_format['hits'][0]['recipe']['url']) # original recipe url'''

  return render_template('recipes.html', stock_query=query_stock(current_user.id), ingredients_list=ingredients)


'''@app.route("/generate_recipe", methods=['POST'])
@login_required
def generate_recipe():

    
'''

# add a food item to database
def insert_food(user_id, food_name, expiration_date):
    new_item = Stock(user_id=user_id, food_name=food_name, expiration_date=expiration_date)
    db.session.add(new_item)
    db.session.commit()

# check if a user has a food item
def has_food(user_id):
    food_item = Stock.query.filter_by(user_id=user_id).all()
    if food_item:
        return food_item
    return None  # user has no food itmes

# pulls up all of the stock corresponding to a user
def query_stock(user_id):
    result = db.session.execute(db.select(Stock.food_name, Stock.expiration_date).where(Stock.user_id == user_id)).all()
    return result

# removes a food item with a user's id from the stock table
def remove_food(user_id, food_name):
  to_remove = Stock.query.filter_by(user_id=user_id, food_name=food_name).first()
  if to_remove:
      msg_text = 'Food item %s successfully removed' % str(to_remove)
      db.session.delete(to_remove)
      db.session.commit()
      print(msg_text)

def cleanup(signum, frame):
    # pass
    # uncomment for styling cleanup

    print('Cleaning up tailwind')
    process.terminate()
    process.wait()
    print('Cleaned up')
    exit(0)


signal.signal(signal.SIGINT, cleanup)


if __name__ == '__main__':
    # uncomment if working on styling
    process = subprocess.Popen(['npx', 'tailwindcss', '-i', './static/styles/input.css', '-o', './static/styles/output.css', '--watch'])
    try:
        app.run(debug=True, host="0.0.0.0")
    finally:
        # pass
        # uncomment if working on styling
        cleanup(None, None)
