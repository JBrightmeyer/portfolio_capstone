from flask import Flask, render_template, session, request 
from flask_login import LoginManager 

app = Flask(__name__)

app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///portfolio"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="admin"

login_manager = LoginManager()
login_manager.init_app(app)

connect_db(app)


db.create_all()