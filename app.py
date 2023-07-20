from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, login_url
from forms import LoginForm
from models import db, connect_db, User, Project, Comment, Job, Responsibility, Job_Responsibility, Education

app = Flask(__name__)

app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///portfolio"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="admin"

login_manager = LoginManager()
login_manager.init_app(app)
connect_db(app)

db.create_all()



@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit:
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            
            login_user(user)
        
            flash("Logged in successfully")
        
            return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/profiles/<int:userid>/view")
def view_profile(userid):
    user = User.query.get(userid)
    jobs = user.jobs
    jobs_serial = []
    for job in jobs:
        jobs_serial.append(Job.serialize_job(job))
    education = user.education
    education_serial = [] 
    for school in education:
        education_serial.append(Education.serialize_education(school))
    return render_template("user_public_profiel")