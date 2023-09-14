from flask_wtf import FlaskForm 
from wtforms import validators, IntegerField,FieldList, StringField, PasswordField, SelectField, BooleanField, SelectMultipleField, DateField, TextAreaField
from wtforms.validators import URL, Optional, InputRequired, DataRequired 

class LoginForm(FlaskForm):
    
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
class JobForm(FlaskForm):
    def validate_date_range(form, field):
        start_date = form.start_date.data
        end_date = field.data

        if end_date < start_date:
            raise validators.ValidationError("End date must be greater than or equal to start date.")

    title = StringField("Title", validators=[InputRequired()])
    company = StringField("Company", validators=[InputRequired()])
    start_date = DateField("Start Date", validators=[InputRequired()])
    end_date = DateField("End Date", validators=[InputRequired(), validate_date_range])
    current = BooleanField("Current")
    description = TextAreaField("Description")
    
  
    
class UserForm(FlaskForm):
    
    username = StringField("Username", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    github_url = StringField("Github URL (optional)", validators=[URL(), Optional()])
    linkedin_url = StringField("LinkedIn URL (optional)", validators=[URL(), Optional()])
    website_url = StringField("Website URL (optional)", validators=[URL(), Optional()])
    about_me = TextAreaField("About Me", validators=[Optional()])
    
class UserCreateForm(FlaskForm):
    
    username = StringField("Username", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    github_url = StringField("Github URL (optional)", validators=[URL(), Optional()])
    linkedin_url = StringField("LinkedIn URL (optional)", validators=[URL(), Optional()])
    website_url = StringField("Website URL (optional)", validators=[URL(), Optional()])
    about_me = TextAreaField("About Me", validators=[Optional()])

class EducationForm(FlaskForm):
    
    institution = StringField("Institution", validators=[InputRequired()])
    degree = StringField("Degree", validators=[InputRequired()])
    graduation_date = DateField("Graduated", validators=[InputRequired()])
    start_date = DateField("Start", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    graduated = BooleanField("Graduated")
    
class CommentForm(FlaskForm):
    
    name = StringField("Name/Institution", validators=[InputRequired()])
    comment = StringField("Comment", validators=[InputRequired()])
    
class SkillForm(FlaskForm):
    
    description = StringField("Skill", validators=[InputRequired()])
    
class ProjectForm(FlaskForm):
    
    title = StringField("Title", validators=[InputRequired()])
    repository = StringField("Github Repository Name", validators=[InputRequired()])
    project_name = StringField("Github Project Name", validators=[InputRequired()])
    owner_name = StringField("Github Repository Owner Name", validators=[InputRequired()])
    display_picture_url = StringField("Display Picture URL (Optional)", validators=[URL(), Optional()])
    github_url = StringField("Github URL (Optional)", validators=[URL(), Optional()])
    website_url = StringField("Deployed URL (Optional)", validators=[URL(), Optional()])
    description = TextAreaField("Description", validators=[InputRequired()])