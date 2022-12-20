import random
import sys

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
            payload = {"text": f"{result.reddit_url}"}
            res = requests.request(
                "POST",
                "https://api.twitter.com/2/tweets",
                json=payload,
                headers={
                    "Authorization": "Bearer {}".format(j_token),
                    "Content-Type": "application/json",
                },
            )

            res = res.json()
            print("response: ", res)
            result.tweet_id = res['data']['id']
            db.session.add(result)
            db.session.commit()
            return res


def upload_media_twitter(file_path):
    media = {'media': open(file_path, 'rb')}
    res = requests.request('POST', 'https://upload.twitter.com/1.1/media/upload.json')
    rjson = res.json()
    print(f"twitter media upload res: {rjson}")


tweet_job = {
        "id": "new-tweet",
        "func": "src:post_tweet",
        "trigger": "interval",
        "hours": 20
    }


class ImageTweet(object):
    def __init__(self, file):
        self.file = file
        self.total_bytes = os.path.getsize(self.file)
        self.media_id = None
        self.processing_info = None

# doesn't work in a scratch python script. invalid token/or expired. tokens dont expire. idk. figure it out later. fuck it
# source: https://github.com/twitterdev/large-video-upload-python/blob/master/async-upload.py
MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'
class VideoTweet(object):
    def __init__(self, file):
        self.file = file
        self.total_bytes = os.path.getsize(self.file)
        self.media_id = None
        self.processing_info = None

    def upload_init(self):
        request_data = {
            'command': 'INIT',
            'media_type': 'video/mp4',
            'total_bytes': self.total_bytes,
            'media_category': 'tweet_image'
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
        media_id = req.json()['media_id']

        self.media_id = media_id

        print('Media ID: %s' % str(media_id))

    def upload_append(self):
        segment_id = 0
        bytes_sent = 0
        file = open(self.file, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4*1024*1024)
            print('APPEND')
            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media': chunk
            }

            req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

            if req.status_code < 200 or req.status_code > 299:
                print(req.status_code)
                print(req.text)
                return

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))

        print('Upload chunks complete.')

    def upload_finalize(self):
        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
        print(req.json())

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def check_status(self):
        if self.processing_info is None:
            return

        state = self.processing_info['state']

        print('Media processing status is %s' % state)

        if state == u'succeeded':
            return

        if state == u'failed':
            return

        check_after_secs = self.processing_info['check_after_secs']

        print('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def tweet(self):

        request_data = {
            'status': 'I just uploaded',
            'media_ids': self.media_id
        }

        req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)
        print(req.json())