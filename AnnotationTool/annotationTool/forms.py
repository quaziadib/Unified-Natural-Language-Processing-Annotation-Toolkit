from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField, 
    SelectField, 
    PasswordField, 
    SubmitField, 
    BooleanField, 
    TextAreaField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from annotationTool.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    requirements = TextAreaField('Job Requirements', validators=[DataRequired()])
    agreement = TextAreaField('Agreement', validators=[DataRequired()])
    projectType = SelectField(
        'Select Your Project Type', 
        choices=[
            ('Token', 'Token Classification'), 
            ('Text', 'Text Classification'), 
            ('Entailment', 'Text Entailment Annotation'),
            ('Generation', 'Text Generation Annotation'),
            ('Coreference Resolution', 'Coreference Resolution Annotation'),
            ('Q/A Annotation', 'Q/A Annotation')], 
        validators=[DataRequired()]
        )
    submit = SubmitField('Post')
    

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Project Description', validators=[DataRequired()])
    projectType = SelectField(
        'Select Your Project Type', 
        choices=[
            ('Token', 'Token Classification'), 
            ('Text', 'Text Classification'), 
            ('Entailment', 'Text Entailment Annotation'),
            ('Generation', 'Text Generation Annotation'),
            ('Coreference Resolution', 'Coreference Resolution Annotation'),
            ('Q/A Annotation', 'Q/A Annotation')], 
        validators=[DataRequired()]
        )
    labels = TextAreaField('Labels', validators=[DataRequired()]) 
    datasetlink = FileField('Upload Dataset (CSV)', validators=[FileAllowed(['csv'])])
    submit = SubmitField('Post')

class ProjectDashboardDropdown(FlaskForm):

    projectType = SelectField(
            'Select Your Project Type', 
            validators=[DataRequired()]
            )

class TextClassificationDropdown(FlaskForm):

    label_type = SelectField(
            'Label', 
            validators=[DataRequired()]
            )
    submit = SubmitField('Next')
    
class TextEntailmentForm(FlaskForm):
    hypothesis = TextAreaField('Hypothesis', validators=[DataRequired()]) 
    label_type = SelectField(
            'Label', 
            validators=[DataRequired()]
            )
    submit = SubmitField('Next')
    
class TextGenerationForm(FlaskForm):
    response = TextAreaField('Your Response', validators=[DataRequired()])
    submit = SubmitField('Next')
    
class Q_A_Form(FlaskForm):
    answer = TextAreaField('Your Answer', validators=[DataRequired()])
    explaination = TextAreaField('Your Explaination', validators=[DataRequired()])
    submit = SubmitField('Next')
    
class Q_A_MuliModal_Dropdown(FlaskForm):
    answer = TextAreaField('Your Answer', validators=[DataRequired()])
    submit = SubmitField('Next')
    

class DataRequestForms(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    projectName = StringField('Project Name', validators=[DataRequired()])
    projectID = StringField('Project ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
class ExamForm(FlaskForm):
    q1 = SelectField(
        'Classify Sentiment', 
        choices=[
            ('Positive', 'Positive'), 
            ('Negative', 'Negative')], 
        validators=[DataRequired()]
        ) 
    q2 = SelectField(
        'Classify Sentiment', 
        choices=[
            ('Positive', 'Positive'), 
            ('Negative', 'Negative')], 
        validators=[DataRequired()]
        )
    q3 = SelectField(
        'Classify Sentiment', 
        choices=[
            ('Positive', 'Positive'), 
            ('Negative', 'Negative')], 
        validators=[DataRequired()]
        )
    
    q4 = SelectField(
        'Classify Sentiment', 
        choices=[
            ('Positive', 'Positive'), 
            ('Negative', 'Negative')], 
        validators=[DataRequired()]
        )
    
    q5 = SelectField(
        'Classify Sentiment', 
        choices=[
            ('Positive', 'Positive'), 
            ('Negative', 'Negative')], 
        validators=[DataRequired()]
        )
    
    submit = SubmitField('Submit')
    