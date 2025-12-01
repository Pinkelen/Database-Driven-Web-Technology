from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegistrationForm, LoginForm

from app import db, login_manager
from app.models import Movie, User

routes_bp = Blueprint('routes_bp', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            genre=request.form.get('genre', None)
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
        movie.genre = request.form.get('genre', movie.genre)
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

# --- Error Handler ---
@routes_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# --- Signup ---
@routes_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('routes_bp.login'))
    return render_template('register.html', form=form)

# --- Login ---
@routes_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('routes_bp.index'))
    return render_template('login.html', form=form)