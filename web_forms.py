from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import re


class LoginForm(FlaskForm):
    ohr = StringField('OHR', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log in')


class NewUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ohr = StringField('OHR', validators=[DataRequired()])
    proc = SelectField('Process', choices=['ABC', 'DEF', 'GHI'], validators=[DataRequired()])
    band = SelectField('Band', choices=['Band 5', 'Band 4'], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('Create Account')

    def validate_password(self, password):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,30}$"
        match_reg = re.compile(reg)
        reg_search = re.search(match_reg, password.data)
        if not reg_search:
            raise ValidationError("Password should contain 1 lower case character, 1 upper case character, 1 number and 1 special  character.")


class ManagerChangeForm(FlaskForm):
    manager_details = SelectField('Choose New Manager', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')


class OOOForm1(FlaskForm):
    q1 = TextAreaField('How is the environment in the office?', validators=[DataRequired(), Length(min=20, max=500)])
    q2 = TextAreaField('How is your interaction with your manager?', validators=[DataRequired(), Length(min=20, max=500)])
    q3 = TextAreaField('How are your trainers supporting you?', validators=[DataRequired(), Length(min=20, max=500)])
    q4 = TextAreaField('How is your interaction with your colleagues?', validators=[DataRequired(), Length(min=20, max=500)])
    q5 = TextAreaField('Are you able to move toward?', validators=[DataRequired(), Length(min=20, max=240)])
    q6 = TextAreaField('Are you facing any challenges or problems?', validators=[DataRequired(), Length(min=20, max=500)])
    q7 = TextAreaField('How do you feel working in the current position?', validators=[DataRequired(), Length(min=20, max=500)])
    submit = SubmitField('Submit')


class OOOForm2(FlaskForm):
    m1 = TextAreaField('Manager Comments', validators=[DataRequired(), Length(min=20, max=500)])
    m2 = TextAreaField('Manager Comments', validators=[DataRequired(), Length(min=20, max=500)])
    m3 = TextAreaField('Manager Comments', validators=[DataRequired(), Length(min=20, max=500)])
    m4 = TextAreaField('Manager Comments', validators=[DataRequired(), Length(min=20, max=500)])
    m5 = TextAreaField('Manager Comments', validators=[DataRequired(), Length(min=20, max=500)])
    m6 = TextAreaField('Manager Comments', validators=[DataRequired(), Length(min=20, max=500)])
    m7 = TextAreaField('Manager Comments', validators=[DataRequired(), Length(min=20, max=500)])
    submit = SubmitField('Submit')


class OOOForm3(FlaskForm):
    submit = SubmitField('Submit')
