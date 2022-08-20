from enum import unique
from flask_sqlalchemy import SQLAlchemy
from app import db


class Links(db.models):
    id = db.Column(db.integer, primary_key=True)
    link_text = db.Column(db.String(80), unique=True,nullable=False)
    link = db.Column(db.String(120), unique=True,nullable=False)

    def __repr__(self):
        return '<Link %r>' % self.link_text