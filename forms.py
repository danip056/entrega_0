from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    SelectField,
    DateTimeField,
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional
# import email_validator
from flask_login import current_user
from wtforms import ValidationError,validators
from models import User, EventCategoryEnum

class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])

class register_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(6, 25)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(6, 25),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )

class EventForm(FlaskForm):

    name = StringField(validators=[InputRequired(), Length(1, 64)])
    category = SelectField(choices=[
        (EventCategoryEnum.conferencia.value, EventCategoryEnum.conferencia.value),
        (EventCategoryEnum.seminario.value, EventCategoryEnum.seminario.value),
        (EventCategoryEnum.congreso.value, EventCategoryEnum.congreso.value),
        (EventCategoryEnum.curso.value, EventCategoryEnum.curso.value),
        ])
    place = StringField(validators=[InputRequired(), Length(1, 64)])
    address = StringField(validators=[InputRequired(), Length(1, 64)])
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()
    is_virtual = BooleanField()