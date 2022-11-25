from marshmallow import Schema, fields


class RedditDataSchema(Schema):
    id = fields.Int()
    content_type = fields.Str()
    height = fields.Int()
    width = fields.Int()
    reddit_url = fields.Str()
    reddit_submission_id = fields.Str()
    # created_utc = db.Column(db.TIMESTAMP(timezone=True))
    created_utc = fields.Float()
    oembed_html = fields.Str()
    score = fields.Int()
