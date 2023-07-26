from datetime import datetime
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy() 

def connect_db(app):
    db.app = app
    db.init_app(app) 
    
class User(UserMixin, db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    type = db.Column(db.String,
                     default="basic")
    created_at = db.Column(db.DateTime,
                           default=datetime.today())
    
    projects = db.Relationship("Project", backref="users")
    jobs = db.Relationship("Job")
    education = db.Relationship("Education", cascade="all, delete")
    

    @classmethod 
    def serialize_user(cls,user):
        return {"first_name":user.first_name,
                "last_name":user.last_name}


    @classmethod
    def register(cls, first_name, last_name, username, password):
        hash = bcrypt.generate_password_hash(password).decode("utf8")
        user = User(
            username = username,
            password = hash,
            first_name = first_name,
            last_name = last_name
        )
        db.session.add(user)
        db.session.commit()
        return (user)
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user 
        else:
            return False
    
class Comment(db.Model):
    
    __tablename__ = "comments"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String)
    content = db.Column(db.String)
    date_submitted = db.Column(db.DateTime)
    
class Job(db.Model):
    
    __tablename__ = "jobs"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text)
    company = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date,
                         nullable=False)
    current = db.Column(db.Boolean)
    user = db.Column(db.ForeignKey("users.id"))
    description = db.Column(db.Text)
    
    
    @classmethod 
    def serialize_job(cls, job):
        return {"id":job.id,
                "title":job.title,
                "company": job.company,
                "start_date": job.start_date,
                "end_date":job.end_date,
                "current":job.current,
                "description":job.description}
        
class Education(db.Model):
    
    __tablename__ = "education"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    institution = db.Column(db.String)
    degree = db.Column(db.String)
    graduation_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    graduated = db.Column(db.Boolean)
    user = db.Column(db.ForeignKey("users.id"))
    
    @classmethod 
    def serialize_education(cls, education):
        return {"id":education.id,
                "institution":education.institution,
                "degree":education.degree,
                "graduation_date":education.graduation_date,
                "start_date":education.start_date,
                "graduated":education.graduated}
    
    
class Responsibility(db.Model):
    
    __tablename__ = "responsibilities"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    description = db.Column(db.String)
    job = db.Column(db.ForeignKey("jobs.id"))
    
    @classmethod 
    def serialize_responsibility(cls, responsibility):
        return {"id":responsibility.id, "description":responsibility.description}
    

class Project(db.Model):
    
    __tablename__ = "projects"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String)
    repository = db.Column(db.String)
    project_name = db.Column(db.String)
    owner_name = db.Column(db.String)
    display_picture_url = db.Column(db.String)
    github_url = db.Column(db.String)
    website_url = db.Column(db.String,
                            nullable=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey("users.id"))
    
    @classmethod
    def serialize_project(cls, project):
        return {"id": project.id,
                "repository":project.repository,
                "project_name":project.project_name,
                "owner_name":project.owner_name,
                "display_picture_url":project.display_picture_url,
                "github_url":project.github_url,
                "website_url":project.website_url,
                "title":project.title,
                "description":project.description,
                "user_id":project.user_id}