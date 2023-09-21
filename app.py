from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, make_response
from flask_login import current_user,logout_user, LoginManager, login_required, login_user, login_url
from forms import LoginForm, JobForm, UserForm, EducationForm, CommentForm, UserCreateForm, SkillForm, ProjectForm
from models import db, connect_db, User, Project, Comment, Job, Education, Skill
from sqlalchemy import exc


app = Flask(__name__)

app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://nwhaufdl:J4wxtg119DBhEt3BRMMwiWgH2b9duhwt@peanut.db.elephantsql.com/nwhaufdl"
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
    login_Form = LoginForm()
    register_Form = UserCreateForm()
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for("edit_profile", userid=current_user.id))
    return render_template("/update/home/home.html", login_Form=login_Form, register_Form=register_Form)

@app.route("/logout")
@login_required 
def logout():
    """Logs the current user out
    """
    logout_user()
    return redirect(url_for("home"))

#######################################################################
#Comment Routes

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

@app.route("/public/<int:userid>")
def view_profile(userid):
    """Renders public view of a user, This does not include editing capabilities
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    user_serial = User.serialize_user(user)
    
    jobs_serial = [Job.serialize_job(job) for job in user.jobs]
    jobs_serial.sort(key=lambda x: x["end_date"], reverse=True)
    
    education_serial = [Education.serialize_education(school) for school in user.education]
    education_serial.sort(key=lambda x: x["graduation_date"], reverse=True)
    
    serial_projects = [Project.serialize_project(project) for project in user.projects]
    serial_projects.sort(key=lambda x: x["title"])
    return render_template("/update/profile/public_profile.html", user = user_serial, jobs = jobs_serial, education=education_serial, projects = serial_projects)

@app.route("/private/<int:userid>")
@login_required
def edit_profile(userid):
    """Renders private view of a user, This includes editing capabilities
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    user_serial = User.serialize_user(user)
    
    jobs_serial = [Job.serialize_job(job) for job in user.jobs]
    jobs_serial.sort(key=lambda x: x["end_date"], reverse=True)
    
    education_serial = [Education.serialize_education(school) for school in user.education] 
    education_serial.sort(key=lambda x: x["graduation_date"], reverse=True)
    
    serial_projects = [Project.serialize_project(project) for project in user.projects]
    serial_projects.sort(key=lambda x: x["title"])
    
    return render_template("/update/profile/private_profile.html", user=user_serial, jobs=jobs_serial, education=education_serial, projects = serial_projects)

#######################################################################
#User Routes

@app.route("/users/<int:userid>/edit", methods=["GET", "POST"])
@login_required 
def edit_user_get(userid):
    """POST: Validates the form, edits the user based on form changes 
        GET: Renders UserForm with fields populated with current user data
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    form = UserForm(obj=user)
    return render_template("/edit/user_edit.html", form=form)

@app.route("/users/<int:userid>/edit", methods=["POST"])
@login_required 
def edit_user_post(userid):
    """POST: Validates the form, edits the user based on form changes 
        GET: Renders UserForm with fields populated with current user data
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    form = UserForm(obj=user)
    error = None
    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data 
        user.last_name = form.last_name.data 
        user.about_me = form.about_me.data
        user.github_url = form.github_url.data 
        user.linkedin_url = form.linkedin_url.data 
        user.website_url = form.website_url.data
        db.session.commit()
        return make_response(redirect(url_for("home")), 201)
    return make_response(render_template("/edit/user_edit.html", form=form), 400)

@app.route("/users/<int:userid>/delete", methods=["POST"])
@login_required 
def delete_user(userid):
    """POST: Deletes user
    Args:
        userid (int): id of user being queried
    """
    logout_user()
    user = User.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))

#######################################################################
#User Job Routes

@app.route("/users/<int:userid>/jobs/add", methods=["GET"])
@login_required
def add_user_job_get(userid):
    """GET: Renders JobForm
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    form = JobForm()
    return render_template("/add/add_job.html", form=form)

@app.route("/users/<int:userid>/jobs/add", methods=["POST"])
@login_required
def add_user_job_post(userid):
    """POST: Validates the form, adds job to current user
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data,
                  company=form.company.data,
                  start_date=form.start_date.data,
                  end_date=form.end_date.data,
                  current=form.current.data,
                  user=userid,
                  description = form.description.data)
        db.session.add(job)
        db.session.commit()
        return make_response(redirect(url_for("home")), 201)
    else:
        return make_response(render_template("/add/add_job.html", form=form), 400)

@app.route("/users/<int:userid>/jobs/<int:jobid>/edit", methods=["GET"])
@login_required 
def edit_user_job_get(userid, jobid):
    """GET: Renders JobForm with fields populated with current job data
    Args:
        userid (int): id of user being queried
        jobid (int): id of job being queried
    """
    job = Job.query.get(jobid)
    form = JobForm(obj=job)
    return render_template("/edit/job_edit.html", job=job, form=form)

@app.route("/users/<int:userid>/jobs/<int:jobid>/edit", methods=["POST"])
@login_required 
def edit_user_job_post(userid, jobid):
    """POST: Validates the form, edits the job based on form changes
    Args:
        userid (int): id of user being queried
        jobid (int): id of job being queried
    """
    job = Job.query.get(jobid)
    form = JobForm(obj=job)
    print(form.title.data)
    if form.validate_on_submit():
        job.title = form.title.data 
        job.company = form.company.data
        job.start_date = form.start_date.data 
        job.end_date = form.end_date.data 
        job.current = form.current.data 
        job.description = form.description.data 
        db.session.commit()
        return redirect(url_for("home"))
    return make_response(render_template("/edit/job_edit.html", job=job, form=form), 400)

@app.route("/users/<int:userid>/jobs/<int:jobid>", methods=["POST"])
@login_required 
def delete_job(userid, jobid):
    """DELETE: Deletes Job
    Args:
        jobid (int): id of job being queried
        userid (int): id of user being queried
    """
    job = Job.query.get(jobid)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for("home"))


#######################################################################
#User Education Routes

@app.route("/users/<int:userid>/education/add", methods=["GET"])
@login_required
def add_user_education_get(userid):
    """POST: Validates the form, adds education to current user
        GET: Renders EducationForm
    Args:
        userid (int): id of user being queried
    """
    form = EducationForm()
    return render_template("/add/add_education.html", form=form)

@app.route("/users/<int:userid>/education/add", methods=["POST"])
@login_required
def add_user_education_post(userid):
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
        return make_response(redirect(url_for("home")), 201)
    return make_response(render_template("/add/add_education.html", form=form), 400)

@app.route("/users/<int:userid>/education/<int:eduid>/edit", methods=["GET"])
@login_required
def edit_user_education_get(userid, eduid):
    """POST: Validates the form, edits the education based on form changes
        GET: Renders EducationForm with fields populated with current education data
    Args:
        userid (int): id of user being queried
        eduid (int): id of education being queried
    """
    school = Education.query.get(eduid)
    form = EducationForm(obj=school)
    return render_template("/edit/education_edit.html", form=form, school=school)

@app.route("/users/<int:userid>/education/<int:eduid>/edit", methods=["POST"])
@login_required
def edit_user_education_post(userid, eduid):
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
        return make_response(redirect(url_for("home")), 201)
    return make_response(render_template("/edit/education_edit.html", form=form, school=school), 400)

@app.route("/users/<int:userid>/education/<int:eduid>/delete", methods=["POST"])
@login_required 
def delete_education(userid, eduid):
    """POST: Deletes Education
    Args:
        eduid (int): id of education being queried
        userid (int): id of user being queried
    """
    edu = Education.query.get(eduid)
    db.session.delete(edu)
    db.session.commit()
    return redirect(url_for("home"))

#######################################################################
#Project Routes

@app.route("/users/<int:userid>/projects/add", methods=["GET"])
@login_required
def add_user_project_get(userid):
    """POST: Validates the form, adds project to current user
        GET: Renders ProjectForm
    Args:
        userid (int): id of user being queried
    """
    form = ProjectForm()
    return render_template("/add/add_project.html", form=form)

@app.route("/users/<int:userid>/projects/add", methods=["POST"])
@login_required
def add_user_project_post(userid):
    """POST: Validates the form, adds project to current user
        GET: Renders ProjectForm
    Args:
        userid (int): id of user being queried
    """
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(title = form.title.data,
                            repository = form.repository.data,
                            project_name = form.project_name.data,
                            owner_name = form.owner_name.data,
                            display_picture_url = form.display_picture_url.data,
                            github_url = form.github_url.data,
                            website_url = form.website_url.data,
                            description = form.description.data,
                            user_id = userid)
        db.session.add(project)
        db.session.commit()
        return make_response(redirect(url_for("home")), 201)
    return render_template("/add/add_project.html", form=form)

@app.route("/users/<int:userid>/projects/<int:projectid>/edit", methods=["GET"])
@login_required
def edit_user_project_get(userid, projectid):
    """POST: Validates the form, edits the project based on form changes
        GET: Renders ProjectForm with fields populated with current project data
    Args:
        userid (int): id of user being queried
        projectid (int): id of project being queried
    """
    project = Project.query.get(projectid)
    form = ProjectForm(obj=project)
    return render_template("/edit/project_edit.html", form=form, project=project)

@app.route("/users/<int:userid>/projects/<int:projectid>/edit", methods=["POST"])
@login_required
def edit_user_project_post(userid, projectid):
    """POST: Validates the form, edits the project based on form changes
        GET: Renders ProjectForm with fields populated with current project data
    Args:
        userid (int): id of user being queried
        projectid (int): id of project being queried
    """
    project = Project.query.get(projectid)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = form.title.data
        project.repository = form.repository.data
        project.project_name = form.project_name.data
        project.owner_name = form.owner_name.data
        project.display_picture_url = form.display_picture_url.data
        project.github_url = form.github_url.data
        project.website_url = form.website_url.data
        project.description = form.description.data
        db.session.commit()
        return make_response(redirect(url_for("home")), 201)
    return make_response(render_template("/edit/project_edit.html", form=form, project=project), 400)

@app.route("/users/<int:userid>/projects/<int:projectid>/delete", methods=["POST"])
@login_required 
def delete_project(userid, projectid):
    """POST: Deletes Project
    Args:
        projectid (int): id of project being queried
        userid (int): id of user being queried
    """
    project = Project.query.get(projectid)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("home"))

###############################################################################
#API
    
@app.route("/api/projects/<int:userid>")
def get_projects(userid):
    """returns the serialized list of projects associated with a user

    Args:
        userid (int): user being queried

    Returns:
        list: list of dictionaries representing serialized projects associated with a user
    """
    projects = Project.query.filter_by(user_id=userid)
    serial_projects = [Project.serialize_project(project) for project in projects]
    return jsonify(serial_projects)

@app.route("/api/login", methods=["POST"])
def api_login():
    """POST: Determines if login information is valid, if so logs the user in
        GET: Renders login form
    """
    error = None
    login_Form = LoginForm()
    register_Form = UserCreateForm()
    if login_Form.validate_on_submit and request.method == "POST":
        user = User.authenticate(login_Form.username.data, login_Form.password.data)
        if user:
            login_user(user)
            return make_response(jsonify({"message":"logged in successfully", "user":user.id}), 200)
        else: 
            error="Invalid Credentials"
            return make_response(jsonify({"message":"invalid credentials"}), 400)
    return render_template("/update/home/home.html", login_Form=login_Form, register_Form=register_Form)

@app.route("/api/register", methods=["POST"])
def api_register():
    """POST: Validates the form, registers the user and logs them in
        GET: Renders UserCreateForm
    """
    login_Form = LoginForm()
    register_Form = UserCreateForm()
    error=None
    if register_Form.validate_on_submit():
        try:
            user = User.register(register_Form.first_name.data,
                                register_Form.last_name.data,
                                register_Form.username.data,
                                register_Form.password.data,
                                register_Form.about_me.data,
                                register_Form.github_url.data,
                                register_Form.linkedin_url.data,
                                register_Form.website_url.data)
            login_user(user)
            return make_response(jsonify({"message":"registered", "user":user.id}), 200)
        except exc.IntegrityError as e:
            db.session.rollback()
            print(e)
            error = "That username already exists"
            return make_response(jsonify({"message":"error"}), 401)
    return render_template("/update/home/home.html", login_Form=login_Form, register_Form=register_Form)