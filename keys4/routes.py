from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc  # Добавьте эту строку
from app import app, db
from models import Book, User, Rental
from datetime import datetime, timedelta

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('user_books' if not user.is_admin else 'admin_books'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('user_books' if not current_user.is_admin else 'admin_books'))

@app.route('/user/books')
@login_required
def user_books():
    sort = request.args.get('sort')
    query = Book.query

    if sort == 'category':
        query = query.order_by(Book.category)
    elif sort == 'author':
        query = query.order_by(Book.author)
    elif sort == 'year':
        query = query.order_by(desc(Book.year))  # сортировка по убыванию года
    
    books = query.all()
    return render_template('user/books.html', books=books, current_sort=sort)

@app.route('/user/rent/<int:book_id>', methods=['GET', 'POST'])
@login_required
def rent_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        duration = int(request.form['duration'])
        if book.available_quantity > 0 and current_user.balance >= book.rent_price:
            end_date = datetime.utcnow() + timedelta(days=duration*30)
            rental = Rental(user_id=current_user.id, book_id=book.id, end_date=end_date)
            current_user.balance -= book.rent_price
            book.available_quantity -= 1
            db.session.add(rental)
            db.session.commit()
            flash(f'You have successfully rented "{book.title}" for {duration} month(s)')
            return redirect(url_for('user_books'))
        else:
            flash('Not enough balance or book not available')
    return render_template('user/rent.html', book=book)

@app.route('/user/buy/<int:book_id>')
@login_required
def buy_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_quantity > 0 and current_user.balance >= book.purchase_price:
        current_user.balance -= book.purchase_price
        book.available_quantity -= 1
        db.session.commit()
        flash(f'You have successfully purchased "{book.title}"')
    else:
        flash('Not enough balance or book not available')
    return redirect(url_for('user_books'))

@app.route('/admin/books')
@login_required
def admin_books():
    if not current_user.is_admin:
        return redirect(url_for('user_books'))
    books = Book.query.all()
    return render_template('admin/books.html', books=books)

@app.route('/admin/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        return redirect(url_for('user_books'))
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = int(request.form['year'])
        book.category = request.form['category']
        book.purchase_price = float(request.form['purchase_price'])
        book.rent_price = float(request.form['rent_price'])
        book.available_quantity = int(request.form['available_quantity'])
        db.session.commit()
        flash('Book updated successfully')
        return redirect(url_for('admin_books'))
    return render_template('admin/edit_book.html', book=book)

@app.route('/check_rentals')
@login_required
def check_rentals():
    rentals = Rental.query.filter_by(user_id=current_user.id, returned=False).all()
    for rental in rentals:
        if rental.end_date <= datetime.utcnow():
            flash(f'Your rental for "{rental.book.title}" has expired. Please return the book.')
    return redirect(url_for('user_books'))
