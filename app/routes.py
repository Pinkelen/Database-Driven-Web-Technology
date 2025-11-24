from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.models import Movie, User

routes_bp = Blueprint('routes_bp', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Signup ---
@routes_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password'])
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('routes_bp.login'))
    return render_template('register.html')

# --- Login ---
@routes_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('routes_bp.index'))
    return render_template('login.html')

# --- Logout ---
@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes_bp.login'))

# --- Home ---
@routes_bp.route('/')
def index():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)

# --- Add Movie ---
@routes_bp.route('/add_movie', methods=['GET','POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        new_movie = Movie(
            name=request.form['name'],
            year=request.form['year'],
            oscars=request.form['oscars']
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('routes_bp.index'))
    return render_template('add_movie.html', movie=None)

# --- EDIT MOVIE ---
@routes_bp.route('/edit_movie/<int:id>', methods=['GET','POST'])
@login_required
def edit_movie(id):
    movie = Movie.query.get_or_404(id)

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.year = request.form['year']
        movie.oscars = request.form['oscars']
        db.session.commit()
        return redirect(url_for('routes_bp.index'))

    return render_template('add_movie.html', movie=movie)

# --- Delete Movie ---
@routes_bp.route('/delete_movie/<int:id>', methods=['POST'])
@login_required
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('routes_bp.index'))
