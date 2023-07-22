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