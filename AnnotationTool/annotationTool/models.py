from datetime import datetime
from annotationTool import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    project = db.relationship('Project', backref='author', lazy=True)
    project_id = db.Column(db.Integer, nullable=True)
    is_passed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False) 
    projectType = db.Column(db.Text, nullable=False)
    projectID = db.Column(db.Text, nullable=False) 
    agreement = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    projectType = db.Column(db.Text, nullable=False) 
    labels = db.Column(db.Text, nullable=True)
    datasetLink = db.Column(db.String(20), nullable=False, default='default.csv')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.title}', '{self.date_posted}', '{self.user_id}')"
    
class DataRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    projectID = db.Column(db.Integer, nullable=False)
    projectName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f"DataRequest('{self.name}', '{self.projectID}', '{self.projectName}', '{self.email}')"
    