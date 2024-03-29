from ..sharedDB.sharedDB import db
from sqlalchemy.dialects.postgresql import JSON as SQL_JSON
from flask_login import UserMixin


class TVResult(db.Model):
    __tablename__ = 'TVResults'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(500))
    year = db.Column(db.String(10))
    score = db.Column(db.Float)
    score_count = db.Column(db.Integer)
    poster = db.Column(db.String(500))
    backdrop = db.Column(db.String(500))
    providers = db.Column(SQL_JSON)
    reviews = db.Column(SQL_JSON)
    media_type = "tv"
    last_updated = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<TVResult: {self.title} ({self.id})>'


class MovieResult(db.Model):
    __tablename__ = 'MovieResults'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(500))
    year = db.Column(db.String(10))
    score = db.Column(db.Float)
    score_count = db.Column(db.Integer)
    poster = db.Column(db.String(500))
    backdrop = db.Column(db.String(500))
    providers = db.Column(SQL_JSON)
    reviews = db.Column(SQL_JSON)
    media_type = "movie"
    last_updated = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<MovieResult: {self.title} ({self.id})>'


class Query(db.Model):
    __tablename__ = 'Queries'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    q = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Query: {self.q}>'


class QueryResultMapping(db.Model):
    __tablename__ = 'QueryResultMappings'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    q = db.Column(db.Integer, db.ForeignKey('Queries.id'), nullable=False)
    tv_result = db.Column(db.Integer, db.ForeignKey(
        'TVResults.id'))
    movie_result = db.Column(db.Integer, db.ForeignKey(
        'MovieResults.id'))

    def __repr__(self):
        return f'<QueryResultMapping: {self.q}, {self.tv_result}, {self.movie_result}>'


class UserAccount(UserMixin, db.Model):
    __tablename__ = 'UserAccounts'
    username = db.Column(db.String(25), primary_key=True, nullable=False)
    password = db.Column(db.String(25))

    def __repr__(self):
        return f'<UserAccount: {self.username}>'

    def get_id(self):
        return (self.username)


class Watchlist(db.Model):
    __tablename__ = 'Watchlist'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(25), db.ForeignKey('UserAccounts.username'), nullable=False)
    tv_id = db.Column(db.Integer, db.ForeignKey('TVResults.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('MovieResults.id'))

    def __repr__(self):
        return f'<Watchlist id:{self.id} tv_id:{self.tv_id} movie_id:{self.movie_id} user_id:{self.user_id}>'
