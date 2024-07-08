from flask import Flask, render_template, url_for, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '83d6f0aedb63b08422f3b396f423f79c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'  # database filename
db = SQLAlchemy(app)


class User(db.Model):  # Represents table for a single user, can change if using different thing
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"


class Stock(db.Model):  # Represents a food table storing all the food and expiration dates, each associated with a user id
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # figure out how to ge this
    food_name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Food('{self.food_name}', '{self.expiration_date}')"

with app.app_context():
  db.create_all()


@app.route("/")      
@app.route("/login")
def login():
    login_message = "Login"
    return render_template('login.html', subtitle='Login Page', text=login_message)


@app.route("/register", methods=['GET', 'POST'])
def register():  # change if using different register thing
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('register.html', title='Register', form=form)   


@app.route("/stock")
def stock():
  return render_template('stock.html', subtitle='Stock page', text='Current Stock')


@app.route("/recipes")
def recipes():
  return render_template('recipes.html', subtitle='Recipe page', text='Generate Recipes')


# add a food item to database
def insert_food(user_id, food_name, expiration_date):
    new_item = Stock(user_id=user_id, food_name=food_name, expiration_date=expiration_date)
    db.session.add(new_item)
    db.session.commit()


# check if a user has a food item
def has_food(user_id, food_name):
    food_item = Stock.query.filter_by(user_id=user_id, food_name=food_name)
    if food_item:
        return food_item
    return None


if __name__ == '__main__':         \
    app.run(debug=True, host="0.0.0.0")