import random

import requests
from flask import current_app
from requests_oauthlib import OAuth1Session
import os
import json
import asyncio

from src.extensions.db import db
from src.extensions.scheduler import scheduler
from src.models import RedditDataModel


def post_tweet():
    with scheduler.app.app_context():
        result = RedditDataModel.query.filter_by(tweet_id=None).first()
        # result = db.session.execute(data_lookup)
        print(result.reddit_url)
        if result is not None:
            rd = result
            j_token = current_app.config["TWITTER_TOKEN"]
            # j_token = json.load(j_token)
            print("result", rd)
            if j_token is None:
                print(f"Twitter token not set... {j_token}")
                return
            rand = random.randint(a=1, b=20)
            payload = {"text": "hello{}".format(rand)}
            res = requests.request(
                "POST",
                "https://api.twitter.com/2/tweets",
                json=payload,
                headers={
                    "Authorization": "Bearer {}".format(j_token),
                    "Content-Type": "application/json",
                },
            )
            print("response: ", res)
            return res


tweet_job = {
        "id": "new-tweet",
        "func": "src:post_tweet",
        "trigger": "interval",
        "hours": 20
    }
