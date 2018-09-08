from flask import Flask
import os
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/sample'
app.config['SECRET_KEY'] = "mysecret123456"
db = SQLAlchemy(app)

class Movie(db.Model):
    title = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def home():
    movies = None
    if request.form:
        try:
            movie = Movie(title=request.form.get("title"), location=request.form.get("location"), time=request.form.get("time"))
            db.session.add(movie)
            db.session.commit()
        except Exception as e:
            print("Failed to add movie")
            print(e)
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)

@app.route("/update", methods=["POST"])
def update():
    try:
        oldtitle = request.form.get("oldtitle")
        newtitle = request.form.get("newtitle")
        location = request.form.get("location")
        time = request.form.get("time")
        movie = Movie.query.filter_by(title=oldtitle).first()
        movie.title = newtitle
        movie.location = location
        movie.time = time
        db.session.commit()
    except Exception as e:
        print("Couldn't update movie title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    movie = Movie.query.filter_by(title=title).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect("/")
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)