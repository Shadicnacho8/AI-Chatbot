from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app import db
from app.models import User
import sqlalchemy as sa


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Enter your email..."})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter your password..."})


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your name..."})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email..."})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password..."})
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your password..."})

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
