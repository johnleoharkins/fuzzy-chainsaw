from marshmallow import Schema, fields


class RedditDataSchema(Schema):
    id = fields.Int()
    content_type = fields.Str()
    height = fields.Int()
    width = fields.Int()
    reddit_url = fields.Str()
    reddit_submission_id = fields.Str()
    created_utc = fields.Float()
    score = fields.Int()
    subreddit_name_prefixed = fields.Str()
    is_gallery = fields.Bool()
    local_filename = fields.Str()
