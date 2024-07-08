from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    item_name = StringField('Item Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    expire_date = DateField('Expiration Date',
                           validators=[DataRequired()])
    add_btn = SubmitField('Add')