from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from myapp.models import User, Book

class SignUpForm(FlaskForm):
    username = StringField('Username',
                            validators =[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):   #this function is checking to make sure that the same username that a user wants to create an account with doesnt already exist
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one ')

    def validate_email(self, email):   #this function is checking to make sure that the same username that a user wants to create an account with doesnt already exist
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one ')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Title',
                            validators =[DataRequired(), Length(min=2, max=100)])
    author = StringField('Author', validators = [DataRequired(), Length(min=3, max=75)])
    genre = SelectField('Genre', choices=['Fiction', 'Non-fiction', 'Fantasy', 'Sci-fi', 'Mystery', 'Thriller', 'Romance', 'Dystopian', 'Drama', 'Poetry', 'Historical', 'Classic', 'Action', 'other' ], validators=[DataRequired()])
    picture = FileField('Picture', validators = [DataRequired(), FileAllowed(['jpeg', 'png'])])
    submit = SubmitField('Add book')


class BooksForSaleForm(FlaskForm):
    price = IntegerField('Price', validators=[DataRequired()])
    style = SelectField('Hardback or paperback?', choices=['Hardback', 'Paperback'], validators=[DataRequired()])
    condition = SelectField('Book condition', choices=['Brand new', 'Used-perfect', 'Used - good', 'Used - fine', 'Used - poor'])
    submit = SubmitField('Add book')

class CheckByTitleForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Search')

class BuyBookForm(FlaskForm):
    submit = SubmitField('Confirm Purchase')
