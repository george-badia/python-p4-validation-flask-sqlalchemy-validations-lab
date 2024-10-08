from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

 
    @validates("name")
    def validate_name(self, key, name):
      if not name:
        raise ValueError("name must be of type string and more than 1 characters")
      
      author = db.session.query(Author.id).filter_by(name = name).first()
      if author is not None:
         raise ValueError('name must be unique.')
      return name

    @validates('phone_number')
    def validate_phone(self, key, phone_value):
        if not re.match(r'^\d{10}$', phone_value):
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validates_title(self, key, title_value):
        if not title_value or title_value.strip() == '':
            raise ValueError("Title must be a non-empty string")
        clickbait_phrases = ["Won't Believe", "Secret", "Top ", "Guess"]
        if not any(phrase in title_value for phrase in clickbait_phrases):
            raise ValueError("Title needs to be more clickbaity!")
        return title_value

    @validates('content')
    def validates_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return content

    @validates('summary')
    def validates_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must not exceed 250 characters")
        return summary

    @validates('category')
    def validates_category(self, key, category):
        valid_categories = ["Fiction", "Non-Fiction"]
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'