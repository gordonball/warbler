from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired, Optional, URL


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """ Form for users to edit their profiles. """
    username = StringField(
        "Username",
        validators=[
            Length(max=20),
            InputRequired()
        ]
    )

    email = StringField(
        "Email",
        validators=[
            Length(max=50),
            InputRequired(),
            Email()
        ]
    )

    image_url = StringField(
        "User Profile Picture",
        validators=[
            Optional(),
            URL()
        ]
    )

    header_image_url = StringField(
        "Profile Banner Image",
        validators=[
            Optional(),
            URL()
        ]
    )

    bio = StringField(
        "User Bio",
        validators=[
            Optional()
        ]
    )

    password = PasswordField(
        "password",
        validators=[
            InputRequired()
        ]
    )

class CSRFProtectForm(FlaskForm):
    """For protection against cross-site request forgery"""

