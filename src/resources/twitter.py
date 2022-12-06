import base64
import hashlib
import json
import os
import re

import requests
from flask import session, redirect, current_app
from flask_smorest import Blueprint
from flask.views import MethodView
from requests_oauthlib import OAuth2Session

from src.schemas import TwitterAuthCallbackSchema

blp = Blueprint("Twitter", __name__, "Operations on twitter")
client_id = os.environ.get("TWITTER_CLIENT_ID")
client_secret = os.environ.get("TWITTER_CLIENT_SECRET")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
redirect_uri = os.environ.get("TWITTER_REDIRECT_URL")
scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

def make_token():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

def post_tweet(payload, token):
    print("Tweeting!")
    return requests.request(
        "POST",
        "https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        },
    )


@blp.route("/twitter/auth")
class TwitterAuthLanding(MethodView):
    def get(self):
        twitter = make_token()
        print(twitter, code_challenge)
        authorization_url, state = twitter.authorization_url(
            auth_url, code_challenge=code_challenge, code_challenge_method="S256"
        )
        session["oauth_state"] = state
        return redirect(authorization_url)


@blp.route("/oauth/callback")
class TwitterOAuth(MethodView):
    @blp.arguments(TwitterAuthCallbackSchema, location="query")
    @blp.response(201)
    def get(self, twitter_auth_callback):
        code = twitter_auth_callback["code"]
        twitter = make_token()
        token = twitter.fetch_token(
            token_url=token_url,
            client_secret=client_secret,
            code_verifier=code_verifier,
            code=code,
        )
        st_token = '"{}"'.format(token)
        j_token = json.loads(st_token)
        # r.set("token", j_token)
        print(j_token)
        current_app.config["TWITTER_TOKEN_RES"] = j_token
        current_app.config["TWITTER_TOKEN"] = token["access_token"]
        # payload = {"text": "hello"}
        # response = post_tweet(payload, token).json()
        return 201
