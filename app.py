from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import current_user,logout_user, LoginManager, login_required, login_user, login_url
from forms import LoginForm, JobForm, UserForm, EducationForm, CommentForm, UserCreateForm
from models import db, connect_db, User, Project, Comment, Job, Responsibility, Education

app = Flask(__name__)

app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///portfolio"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="admin"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
connect_db(app)

db.create_all()



@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    """If user is logged in, renders their homepage.  
    If not then redirects them to login page
    """
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for("edit_profile", userid=current_user.id))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """POST: Determines if login information is valid, if so logs the user in
        GET: Renders login form
    """
    form = LoginForm()
    if form.validate_on_submit:
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash("Logged in successfully")
            return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required 
def logout():
    """Logs the current user out
    """
    logout_user()
    return redirect(url_for("login"))

@app.route("/comments/add", methods=["GET", "POST"])
def add_comment():
    """POST: Validates the CommentForm and adds it to the database
        GET: Renders CommentForm
    """
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(name = form.name.data,
                           content = form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("/add/add_comment.html", form=form)

#######################################################################
#Profile Routes

@app.route("/profiles/<int:userid>/view")
def view_profile(userid):
    """Renders public view of a user, This does not include editing capabilities
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    user_serial = User.serialize_user(user)
    jobs = user.jobs
    jobs_serial = []
    for job in jobs:
        jobs_serial.append(Job.serialize_job(job))
    education = user.education
    education_serial = [] 
    for school in education:
        education_serial.append(Education.serialize_education(school))
    return render_template("user_public_profile.html", user = user_serial, jobs = jobs_serial, education=education_serial)

@app.route("/profiles/<int:userid>/edit")
@login_required
def edit_profile(userid):
    """Renders private view of a user, This includes editing capabilities
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    user_serial = User.serialize_user(user)
    jobs = user.jobs
    jobs_serial = []
    for job in jobs:
        jobs_serial.append(Job.serialize_job(job))
    education = user.education
    education_serial = [] 
    for school in education:
        education_serial.append(Education.serialize_education(school))
    return render_template("user_private_profile.html", user=user_serial, jobs=jobs_serial, education=education_serial)

#######################################################################
#User Routes

@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    """POST: Validates the form, registers the user and logs them in
        GET: Renders UserCreateForm
    """
    form = UserCreateForm()
    if form.validate_on_submit():
        user = User.register(form.first_name.data,
                             form.last_name.data,
                             form.username.data,
                             form.password.data)
        login_user(user)
        return redirect(url_for("edit_profile", userid = user.id))
    return render_template("/add/add_user.html", form=form)

@app.route("/users/<int:userid>/edit", methods=["GET", "POST"])
@login_required 
def edit_user(userid):
    """POST: Validates the form, edits the user based on form changes 
        GET: Renders UserForm with fields populated with current user data
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data 
        user.last_name = form.last_name.data 
        db.session.commit()
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/edit/user_edit.html", form=form)

@app.route("/users/<int:userid>/jobs/add", methods=["GET", "POST"])
@login_required
def add_user_job(userid):
    """POST: Validates the form, adds job to current user
        GET: Renders JobForm
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, company=form.company.data, start_date=form.start_date.data, end_date=form.end_date.data, current=form.current.data, user=userid, description = form.description.data)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/add/add_job.html", form=form)

@app.route("/users/<int:userid>/jobs/<int:jobid>/edit", methods=["GET", "POST"])
@login_required 
def edit_user_job(userid, jobid):
    """POST: Validates the form, edits the job based on form changes
        GET: Renders JobForm with fields populated with current job data
    Args:
        userid (int): id of user being queried
        jobid (int): id of job being queried
    """
    job = Job.query.get(jobid)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        job.title = form.title.data 
        job.company = form.company.data
        job.start_date = form.start_date.data 
        job.end_date = form.end_date.data 
        job.current = form.current.data 
        job.description = form.description.data 
        db.session.commit()
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/edit/job_edit.html", job=job, form=form)

@app.route("/users/<int:userid>/education/add", methods=["GET", "POST"])
@login_required
def add_user_education(userid):
    """POST: Validates the form, adds education to current user
        GET: Renders EducationForm
    Args:
        userid (int): id of user being queried
    """
    form = EducationForm()
    if form.validate_on_submit():
        education = Education(institution = form.institution.data,
                              degree = form.degree.data,
                              graduation_date = form.graduation_date.data,
                              start_date = form.start_date.data,
                              graduated = form.graduated.data,
                              user = userid)
        db.session.add(education)
        db.session.commit()
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/add/add_education.html", form=form)

@app.route("/users/<int:userid>/education/<int:eduid>/edit", methods=["GET", "POST"])
@login_required
def edit_user_education(userid, eduid):
    """POST: Validates the form, edits the education based on form changes
        GET: Renders EducationForm with fields populated with current education data
    Args:
        userid (int): id of user being queried
        eduid (int): id of education being queried
    """
    school = Education.query.get(eduid)
    form = EducationForm(obj=school)
    if form.validate_on_submit():
        school.institution = form.institution.data
        school.degree = form.degree.data 
        school.graduation_date = form.graduation_date.data 
        school.start_date = form.start_date.data 
        school.graduated = form.graduated.data 
        db.session.commit() 
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/edit/education_edit.html", form=form, school=school)

###############################################################################
#API


#For future use
@app.route("/api/profiles/<int:userid>/jobs", methods = ["POST"])
def edit_user_profile(userid):
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data,
                  company = form.company.data,
                  start_date = form.start_date.data,
                  end_date = form.end_date.data,
                  current = form.end_date.data,
                  user = userid)
        db.session.add(job)
        db.session.commit()
        return Job.serialize_job(job)

