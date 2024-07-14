from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    TextAreaField
)
from wtforms.validators import DataRequired, ValidationError, EqualTo

from app.models import User, Role, Group, Status


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")


class TicketForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[(status, status.value) for status in Status],
        validators=[DataRequired()]
    )
    group = SelectField(
        "Group",
        choices=[(group, group.value) for group in Group],
        validators=[DataRequired()]
    )
    note = TextAreaField("Note", validators=[DataRequired()])
    submit = SubmitField("Submit")
