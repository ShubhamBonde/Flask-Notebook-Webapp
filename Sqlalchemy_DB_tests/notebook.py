from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notebook.db'
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post(id:{self.id}, title:{self.title}, content:{self.content})"