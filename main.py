from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, unique=True, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


db.create_all()


class EditForm(FlaskForm):
    rating = FloatField(label="Your rating out of 10", validators=[DataRequired()])
    review = StringField(label="Your review", validators=[DataRequired()])
    submit = SubmitField(label="Update")


class AddForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    year = IntegerField(label="Year", validators=[DataRequired()])
    img_url = StringField(label="Image URL", validators=[DataRequired(), URL()])
    rating = FloatField(label="Your rating out of 10", validators=[DataRequired()])
    ranking = IntegerField(label="Movie rank out of 10", validators=[DataRequired()])
    review = StringField(label="Your review", validators=[DataRequired()])
    description = StringField(label="Description", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.ranking).all()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        new_movie = Movie(
            title=add_form.title.data,
            year=add_form.year.data,
            rating=add_form.rating.data,
            ranking=add_form.ranking.data,
            review=add_form.review.data,
            description=add_form.description.data,
            img_url=add_form.img_url.data
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=add_form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    edit_form = EditForm()
    movie_id = request.args.get("id")
    movie_selected = Movie.query.get(movie_id)
    if edit_form.validate_on_submit():
        movie_selected.rating = edit_form.rating.data
        movie_selected.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", movie=movie_selected, form=edit_form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()
