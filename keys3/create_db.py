from app import app, db
from app.models import User, Post, Tag, Comment

def create_database():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if __name__ == "__main__":
    create_database()