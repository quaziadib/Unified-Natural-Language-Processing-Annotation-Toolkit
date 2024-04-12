from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import EqualTo, DataRequired, Email, Length



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    

## TODO: TextClassification Annotation Input Form
class TextClassificationInputForm(FlaskForm):
    labels = RadioField('Label', validators=[DataRequired()], choices=[('value','description'),('value_two','whatever')])
    submit = SubmitField('Submit')


## TODO: TextEntailment Annotation Input Form
class TextEntailmentInputForm(FlaskForm):
    labels = RadioField('Label', choices=[('value','description'),('value_two','whatever')])
    submit = SubmitField('Submit')

## TODO: TextGeneration Annotation Input Form
class TextGenerationInputForm(FlaskForm):
    text = TextAreaField('Your Response', validators=[DataRequired()])
    submit = SubmitField('Submit')

## TODO: Q/A Annotation Input Form
class QAInputForm(FlaskForm):
    answer = TextAreaField('Your Answer', validators=[DataRequired()])
    explaination = TextAreaField('Your Explaination', validators=[DataRequired()])
    submit = SubmitField('Submit')

## TODO: Token Classification Annotation Input Form

## TODO: Coreference Resolution Annotation









    

