from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, make_response
from flask_login import current_user,logout_user, LoginManager, login_required, login_user, login_url
from forms import LoginForm, JobForm, UserForm, EducationForm, CommentForm, UserCreateForm, SkillForm, ProjectForm
from models import db, connect_db, User, Project, Comment, Job, Education, Skill
from sqlalchemy import exc

@app.route("/users/<int:userId>/jobs", methods=["POST"])
@login_required
def add_user_job(userId):
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
        return make_response(jsonify({"created":job}), 201)
    else:
        return make_response(render_template("/add/add_job.html", form=form), 400)