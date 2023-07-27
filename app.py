from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_login import current_user,logout_user, LoginManager, login_required, login_user, login_url
from forms import LoginForm, JobForm, UserForm, EducationForm, CommentForm, UserCreateForm, SkillForm, ProjectForm
from models import db, connect_db, User, Project, Comment, Job, Education, Skill
from sqlalchemy import exc

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
    error = None
    form = LoginForm()
    if form.validate_on_submit and request.method == "POST":
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash("Logged in successfully")
            return redirect(url_for("home"))
        else: 
            error="Invalid Credentials"
            return render_template("login.html", form=form, error=error)
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required 
def logout():
    """Logs the current user out
    """
    logout_user()
    return redirect(url_for("login"))

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

@app.route("/profiles/<int:userid>/view")
def view_profile(userid):
    """Renders public view of a user, This does not include editing capabilities
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    user_serial = User.serialize_user(user)
    jobs_serial = []
    for job in user.jobs:
        jobs_serial.append(Job.serialize_job(job))
    education_serial = [] 
    for school in user.education:
        education_serial.append(Education.serialize_education(school))
    skills_serial = []
    for skill in user.skills:
        skills_serial.append(Skill.serialize_skill(skill))
    skills_serial.sort(key=lambda x: x["description"])
    return render_template("/public/user_public_profile.html", user = user_serial, jobs = jobs_serial, education=education_serial, skills=skills_serial)

@app.route("/profiles/<int:userid>/edit")
@login_required
def edit_profile(userid):
    """Renders private view of a user, This includes editing capabilities
    Args:
        userid (int): id of user being queried
    """
    user = User.query.get(userid)
    user_serial = User.serialize_user(user)
    jobs_serial = []
    for job in user.jobs:
        jobs_serial.append(Job.serialize_job(job))
    jobs_serial.sort(key=lambda x: x["end_date"], reverse=True)
    education_serial = [] 
    for school in user.education:
        education_serial.append(Education.serialize_education(school))
    skills_serial = []
    for skill in user.skills:
        skills_serial.append(Skill.serialize_skill(skill))
    skills_serial.sort(key=lambda x: x["description"])
    education_serial.sort(key=lambda x: x["graduation_date"], reverse=True)
    return render_template("/private/user_private_profile.html", user=user_serial, jobs=jobs_serial, education=education_serial, skills=skills_serial)

#######################################################################
#User Routes

@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    """POST: Validates the form, registers the user and logs them in
        GET: Renders UserCreateForm
    """
    form = UserCreateForm()
    error=None
    if form.validate_on_submit():
        try:
            user = User.register(form.first_name.data,
                                form.last_name.data,
                                form.username.data,
                                form.password.data,
                                form.about_me.data,
                                form.github_url.data,
                                form.linkedin_url.data,
                                form.website_url.data)
            login_user(user)
        except exc.IntegrityError as e:
            db.session.rollback()
            print(e)
            error = "That username already exists"
            return render_template("/add/add_user.html", form=form, error=error)
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
    error = None
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.first_name = form.first_name.data 
            user.last_name = form.last_name.data 
            user.about_me = form.about_me.data
            user.github_url = form.github_url.data 
            user.linkedin_url = form.linkedin_url.data 
            user.website_url = form.website_url.data
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            error = "That username already exists"
            return render_template("/edit/user_edit.html", form=form, error=error)
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/edit/user_edit.html", form=form)

@app.route("/users/<int:userid>/delete", methods=["POST"])
@login_required 
def delete_user(userid):
    logout_user()
    user = User.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    flash("User has been deleted")
    return redirect(url_for("home"))

#######################################################################
#User Job Routes

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
        job = Job(title=form.title.data,
                  company=form.company.data,
                  start_date=form.start_date.data,
                  end_date=form.end_date.data,
                  current=form.current.data,
                  user=userid,
                  description = form.description.data)
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

@app.route("/users/<int:userid>/jobs/<int:jobid>/delete", methods=["POST"])
@login_required 
def delete_job(userid, jobid):
    job = Job.query.get(jobid)
    db.session.delete(job)
    db.session.commit()
    flash("Job has been deleted")
    return redirect(url_for("home"))


#######################################################################
#User Education Routes

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

@app.route("/users/<int:userid>/education/<int:eduid>/delete", methods=["POST"])
@login_required 
def delete_education(userid, eduid):
    edu = Education.query.get(eduid)
    db.session.delete(edu)
    db.session.commit()
    flash("Education has been deleted")
    return redirect(url_for("home"))

#######################################################################
#Project Routes

@app.route("/users/<int:userid>/projects/add", methods=["GET", "POST"])
@login_required
def add_user_project(userid):
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
        return redirect(url_for("edit_portfolio", userid=userid))
    return render_template("/add/add_project.html", form=form)

@app.route("/users/<int:userid>/projects/<int:projectid>/edit", methods=["GET", "POST"])
@login_required
def edit_user_project(userid, projectid):
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
        return redirect(url_for("edit_portfolio", userid=userid))
    return render_template("/edit/project_edit.html", form=form, project=project)

@app.route("/users/<int:userid>/projects/<int:projectid>/delete", methods=["POST"])
@login_required 
def delete_project(userid, projectid):
    project = Project.query.get(projectid)
    db.session.delete(project)
    db.session.commit()
    flash("Project has been deleted")
    return redirect(url_for("home"))



#######################################################################
#User Skill Routes

@app.route("/users/<int:userid>/skills/add", methods=["GET", "POST"])
@login_required 
def add_user_skill(userid):
    form = SkillForm()
    if form.validate_on_submit():
        skill = Skill(description=form.description.data, user=userid)
        db.session.add(skill)
        db.session.commit()
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/add/add_skill.html", form=form)

@app.route("/users/<int:userid>/skills/<int:skillid>/edit", methods=["GET", "POST"])
@login_required 
def edit_user_skill(userid, skillid):
    skill = Skill.query.get(skillid) 
    form = SkillForm(obj=skill)
    if form.validate_on_submit():
        skill.description = form.description.data 
        db.session.commit()
        return redirect(url_for("edit_profile", userid=userid))
    return render_template("/edit/edit_skill.html", form=form, skill=skill, user=userid)

@app.route("/users/<int:userid>/skills/<int:skillid>/delete", methods=["POST"])
@login_required 
def delete_skill(userid, skillid):
    skill = Skill.query.get(skillid)
    db.session.delete(skill)
    db.session.commit()
    flash("Skill has been deleted")
    return redirect(url_for("home"))

###############################################################################
#Portfolio Routes

@app.route("/portfolios/<int:userid>/view")
def get_portfolio(userid):
    user = User.query.get(userid)
    projects = user.projects
    serial_projects = []
    for project in projects:
        serial_projects.append(Project.serialize_project(project))
    serial_projects.sort(key=lambda x: x["title"])
    return render_template("/public/user_public_portfolio.html", user=user, projects = serial_projects)

@app.route("/portfolios/<int:userid>/edit")
@login_required
def edit_portfolio(userid):
    user = User.query.get(userid)
    projects = user.projects
    serial_projects = []
    for project in projects:
        serial_projects.append(Project.serialize_project(project))
    serial_projects.sort(key=lambda x: x["title"])
    return render_template("/private/user_private_portfolio.html", user=user, projects = serial_projects)


###############################################################################
#API
    
@app.route("/api/projects/<int:userid>")
def get_projects(userid):
    projects = Project.query.filter_by(user_id=userid)
    serial_projects = []
    for project in projects:
        serial_projects.append(Project.serialize_project(project))
    return jsonify(serial_projects)

