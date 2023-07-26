from models import db, connect_db, User, Project, Comment, Job, Responsibility, Education
from app import app 

db.session.commit()
db.drop_all()
db.create_all()

user = User.register("Test","Test", "test", "test")

for i in range(3):
    job = Job(title=f"Job Title {i}",
              company = "test company",
              start_date = "7/5/2020",
              end_date="7/5/2023",
              current=False,
              user=user.id,
              description="This is a test description for a job")
    db.session.add(job)
    db.session.commit()
    for j in range(3):
        resp = Responsibility(description=f"Hello I am a test description {j}", job=job.id)
        db.session.add(resp)
        db.session.commit()
        

for i in range(2):
    degree = Education(institution=f"Test School {i}",
                       degree=f"Test Degree {i}",
                       graduation_date = "7/5/2023",
                       start_date = "7/5/2020",
                       graduated = False,
                       user = user.id)
    db.session.add(degree)
    db.session.commit()
    
project = Project(repository="portfolio_capstone",
                  project_name="portfolio_capstone",
                  owner_name="JBrightmeyer",
                  display_picture_url="data:image/jpeg;base64,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",
                  title="Portfolio Capstone Website",
                  github_url = "https://github.com/JBrightmeyer/portfolio_capstone",
                  description = "This is a portfolio website built with HTML/CSS/JavaScript and uses Python/Flask as the backend.  It gives users the ability to construct a digital resume and showcase their portfolio projects with a responsive UI.  Editing routes are gated using the Flask-Login library while public routes which let you view the profile of the user are not gated. ",
                  user_id=1)
db.session.add(project)
db.session.commit()