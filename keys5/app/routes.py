from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Trip

def init_routes(app):
    @app.route('/')
    def home():
        trips = Trip.query.all()
        return render_template('home.html', trips=trips)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user = User(username=request.form['username'])
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username']).first()
            if user and user.check_password(request.form['password']):
                login_user(user)
                return redirect(url_for('home'))
            flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/create_trip', methods=['GET', 'POST'])
    @login_required
    def create_trip():
        if request.method == 'POST':
            trip = Trip(
                user_id=current_user.id,
                description=request.form['description'],
                latitude=float(request.form['latitude']),
                longitude=float(request.form['longitude']),
                places_to_visit=request.form['places_to_visit'],
                overall_rating=int(request.form['overall_rating']),
                transportation_rating=int(request.form['transportation_rating']),
                safety_rating=int(request.form['safety_rating']),
                population_rating=int(request.form['population_rating']),
                vegetation_rating=int(request.form['vegetation_rating'])
            )
            db.session.add(trip)
            db.session.commit()
            flash('Trip created successfully!')
            return redirect(url_for('home'))
        return render_template('create_trip.html')

    @app.route('/trip/<int:trip_id>')
    def view_trip(trip_id):
        trip = Trip.query.get_or_404(trip_id)
        return render_template('view_trip.html', trip=trip)
