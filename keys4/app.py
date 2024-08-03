from flask import Flask
from flask_login import LoginManager
from models import db, User, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    # Add test data
    from datetime import datetime
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin', is_admin=True)
        user = User(username='user', password='user')
        db.session.add_all([admin, user])
        
    if not Book.query.first():
        books = [
            Book(title='The Great Gatsby', author='F. Scott Fitzgerald', year=1925, category='Classic', purchase_price=15.99, rent_price=5.99, available_quantity=10),
            Book(title='To Kill a Mockingbird', author='Harper Lee', year=1960, category='Classic', purchase_price=14.99, rent_price=4.99, available_quantity=8),
            Book(title='1984', author='George Orwell', year=1949, category='Dystopian', purchase_price=12.99, rent_price=3.99, available_quantity=15),
            Book(title='The Hobbit', author='J.R.R. Tolkien', year=1937, category='Fantasy', purchase_price=16.99, rent_price=6.99, available_quantity=12),
            Book(title='Pride and Prejudice', author='Jane Austen', year=1813, category='Romance', purchase_price=11.99, rent_price=3.99, available_quantity=7)
        ]
        db.session.add_all(books)
    
    db.session.commit()

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
