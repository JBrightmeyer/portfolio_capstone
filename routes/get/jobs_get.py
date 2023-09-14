from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, make_response
from flask_login import current_user,logout_user, LoginManager, login_required, login_user, login_url
from forms import LoginForm, JobForm, UserForm, EducationForm, CommentForm, UserCreateForm, SkillForm, ProjectForm
from models import db, connect_db, User, Project, Comment, Job, Education, Skill
from sqlalchemy import exc
from app import app

@app.route("/users/<int:userId>/jobs", methods=["POST"])
@login_required
def add_user_job(userId):
    user = User.query.get(userid)
    form = JobForm()
    return render_template("/add/add_job.html", form=form)