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
    created_at = db.Column(db.DateTime)
    
    jobs = db.Relationship("Job")
    projects = db.Relationship("Project")
    education = db.Relationship("Education")
    

    @classmethod 
    def serialize_user(cls,user):
        return {"first_name":user.first_name,
                "last_name":user.last_name}


    @classmethod
    def register(cls, name, username, password):
        hash = bcrypt.generate_password_hash(password).decode("utf8")
        user = User(
            username = username,
            password = hash,
            name = name
        )
        db.session.add(user)
        db.session.commit()
        return cls(username=username, password=hash, name=name)
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user 
        else:
            return False
    
    
class Project(db.Model):
    
    __tablename__ = "projects"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    owner = db.Column(db.ForeignKey("users.id"))
    github_url = db.Column(db.String)
    last_modified = db.Column(db.DateTime)
    
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
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime,
                         nullable=False)
    current = db.Column(db.Boolean)
    user = db.Column(db.ForeignKey("users.id"))
    
    responsibilities = db.Relationship("Responsibility", secondary="jobs_responsibilities", backref="jobs")
    
    
    @classmethod 
    def serialize_job(cls, job):
        resps = job.responsibilities 
        resp_serial = []
        for resp in resps:
            resp_serial.append(Responsibility.serialize_responsibility(resp))
        return {"title":job.title,
                "company": job.company,
                "start_date": job.start_date,
                "end_date":job.end_date,
                "current":job.current,
                "responsibilities":resp_serial}
        
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
    
    @classmethod 
    def serialize_responsibility(cls, responsibility):
        return {"id":responsibility.id, "description":responsibility.description}
    
class Job_Responsibility(db.Model):
    
    __tablename__ = "jobs_responsibilities"
    
    responsibility = db.Column(db.ForeignKey("responsibilities.id"),
                               primary_key=True)
    job = db.Column(db.ForeignKey("jobs.id"),
                    primary_key=True)
    
class Skill(db.Model):
    
    __tablename__ "skills"
    
    