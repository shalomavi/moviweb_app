from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    is_logged_in = db.Column(db.Boolean, default=False)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    movies = db.relationship("Movie", backref="users", lazy=True)

    def __repr__(self) -> str:
        return f"User(user_id={self.id}, name='{self.name}')"

    def __str__(self) -> str:
        return f"{self.name}, {self.username}"


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    poster = db.Column(db.String)
    address = db.Column(db.String)

    def __repr__(self) -> str:
        return f"Movie(movie_id={self.movie_id}, title='{self.title}')"

    def __str__(self) -> str:
        return f"{self.movie_id}, {self.title}"


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    review = db.Column(db.String)

    movie = db.relationship('Movie', backref='reviews', lazy=True)
    user = db.relationship('User', backref='reviews', lazy=True)

    def __repr__(self) -> str:
        return (f"Review(review_id={self.review_id}, user_id={self.user_id},"
                f" movie_id={self.movie_id}, review='{self.review}')")

    def __str__(self) -> str:
        return f"{self.review_id}, {self.review}"
