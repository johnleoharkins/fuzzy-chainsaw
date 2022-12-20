from src.extensions.db import db
from sqlalchemy.dialects.postgresql import TIMESTAMP
class RedditDataModel(db.Model):
    __tablename__ = "reddit.data"

    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(20))
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    reddit_url = db.Column(db.String(200))
    reddit_submission_id = db.Column(db.String(20))
    created_utc = db.Column(db.Float)
    score = db.Column(db.Integer)
    tweet_id = db.Column(db.String(24), nullable=True)
    subreddit_name_prefixed = db.Column(db.String(25))
    is_gallery = db.Column(db.Boolean)
    local_filename = db.Column(db.String(35))
