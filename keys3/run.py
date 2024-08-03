from app import app, db
from app.models import User, Post, Tag, Comment

if __name__ == '__main__':
    app.run(debug=True)