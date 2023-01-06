from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, length


class LoginForm(FlaskForm):
    id = StringField("User id", validators=[DataRequired(), length(max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")



class RegisterForm(FlaskForm):
    id = IntegerField("id")
    first_name = StringField("First name", validators=[DataRequired(), length(max=50)])
    last_name = StringField("Last name", validators=[DataRequired(), length(max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    age = IntegerField("Age")
    biography = TextAreaField("Biography")
    city = StringField("City", validators=[length(max=50)]) 
    submit = SubmitField("Submit")
