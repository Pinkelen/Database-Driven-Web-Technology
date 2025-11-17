from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Movie model representing the movies table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    oscars = db.Column(db.Integer, nullable=False)

# Create the database and the tables for the model
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    movies = Movie.query.all()  # Get all movies from the database
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == "POST":
        name = request.form['name']
        year = request.form['year']
        oscars = request.form['oscars']

        new_movie = Movie(name=name, year=year, oscars=oscars)
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_movie.html', movie=None)

@app.route('/delete_movie/<int:id>', methods=['POST'])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_movie/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    movie = Movie.query.get_or_404(id)

    if request.method == "POST":
        movie.name = request.form['name']
        movie.year = request.form['year']
        movie.oscars = request.form['oscars']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_movie.html', movie=movie)
    
if __name__ == '__main__':
    app.run(debug=True)
