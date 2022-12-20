import asyncio
import io
import logging
import os
import time
import uuid

import asyncpraw
import requests

from flask import current_app, session, url_for
from werkzeug.utils import secure_filename

from src.extensions.scheduler import scheduler

from src.models import RedditDataModel
from src.extensions.db import db

# figure out if I should refactor everything to class based.

def reddit_client():
    reddit_secret = os.getenv('REDDIT_SECRET')
    reddit_id = os.getenv('REDDIT_WEB_APP_ID')
    reddit = asyncpraw.Reddit(
        client_id=reddit_id,
        client_secret=reddit_secret,
        user_agent="asunalab",
    )
    logging.info("created reddit client")
    return reddit



class RedditSubmissionProcessingError(Exception):
    # Constructor or Initializer
    def __init__(self, submissionId, submissionUrl):
        self.id = submissionId
        self.url = submissionUrl

    # __str__ is to print() the value
    def __str__(self):
        msg = (f"[jobs/reddit] Exception: RedditSubmissionProcessing Error! "
               f"submission id: {self.id} | "
               f"submission url: {self.url}")
        return msg

# cannot download from redgif until i get keys .... assuming similar for gyphycat gyphy etc so fuck it
def download_media(content_url, subreddit: str, submission_id, ext):
    subreddit = subreddit.removeprefix('r/')

    # local path to dest. make folders if they dont exist
    target = os.path.join(current_app.config['UPLOAD_FOLDER'], f'reddit/{subreddit}')
    if not os.path.isdir(target):
        os.mkdir(target)
    # generate unique filename
    ct = time.gmtime()
    filename_str = f"{ct.tm_year}{ct.tm_mon}{ct.tm_mday}T{ct.tm_hour}{ct.tm_min}{ct.tm_sec}_{submission_id}{subreddit}.{ext}"
    sec_fn = secure_filename(filename_str)
    destination = os.path.join(target, sec_fn)

    res = requests.get(content_url)
    if res.status_code != requests.codes.ok:
        # TODO: convert to logger; enclose in try catch, throw diff errors. refactor loggers else where
        print(f"Cannot download media. Error retrieving content.\nStatus code: {res.status_code}. Content URL: {content_url}")
        return

    contentb = res.content
    bio = io.BytesIO(contentb)
    with open(destination, 'wb') as fd:
        fd.write(bio.read())
        fd.close()
    bio.close()

    return sec_fn


async def process_subreddit(subreddit_name, sort, time_filter):
    rc = reddit_client()
    sr = await rc.subreddit(subreddit_name, fetch=True)
    match sort:
        case "top":
            async for submission in sr.top(time_filter=time_filter, limit=30):
                process_submission(submission)
        case "hot":
            async for submission in sr.hot(limit=10):
                process_submission(submission)
        case "new":
            async for submission in sr.new(limit=10):
                process_submission(submission)
    await rc.close()


async def process_multireddit(multireddit_name, redditor, sort, time_filter):
    rc = reddit_client()
    mr = await rc.multireddit(redditor=redditor, name=multireddit_name, fetch=True)
    match sort:
        case "top":
            async for submission in mr.top(time_filter=time_filter, limit=30):
                process_submission(submission)
        case "hot":
            async for submission in mr.hot(limit=10):
                process_submission(submission)
        case "new":
            async for submission in mr.new(limit=10):
                process_submission(submission)
    await rc.close()


def process_submission(submission):
    with scheduler.app.app_context():
        submission_lookup = RedditDataModel.query.filter_by(reddit_submission_id=submission.id)
        result = db.session.execute(submission_lookup).scalar()
        if result is None:
            try:
                new_reddit_data = RedditDataModel(
                    reddit_submission_id=submission.id,
                    created_utc=submission.created_utc,
                    score=submission.score,
                    subreddit_name_prefixed=submission.subreddit_name_prefixed,
                    is_gallery=False
                )
                if 'redgif' in submission.url:
                    redgif_url = submission.url.replace("watch", "ifr")

                    new_reddit_data.content_type = "redgif/gif"
                    new_reddit_data.reddit_url = redgif_url
                    new_reddit_data.height = submission.preview['reddit_video_preview']['height']
                    new_reddit_data.width = submission.preview['reddit_video_preview']['width']
                    db.session.add(new_reddit_data)
                    db.session.commit()

                elif 'gfycat' in submission.url:
                    new_reddit_data.content_type = "gfycat/gif"
                    preview_url = submission.preview['reddit_video_preview']['fallback_url']
                    if '.mp4' in preview_url:
                        new_reddit_data.content_type = "gfycat/gif/mp4"
                    new_reddit_data.reddit_url = preview_url
                    new_reddit_data.height = submission.preview['reddit_video_preview']['height']
                    new_reddit_data.width = submission.preview['reddit_video_preview']['width']
                    db.session.add(new_reddit_data)
                    db.session.commit()

                elif 'giphy' in submission.url:
                    new_reddit_data.content_type = "giphy/gif"
                    new_reddit_data.reddit_url = submission.preview['reddit_video_preview']['fallback_url']
                    new_reddit_data.height = submission.preview['reddit_video_preview']['height']
                    new_reddit_data.width = submission.preview['reddit_video_preview']['width']
                    db.session.add(new_reddit_data)
                    db.session.commit()

                elif '.gifv' in submission.url:
                    url_replace = submission.url.replace(".gifv", ".mp4")
                    new_reddit_data.content_type = "gif/mp4"
                    new_reddit_data.reddit_url = url_replace
                    new_reddit_data.height = submission.preview['reddit_video_preview']['height']
                    new_reddit_data.width = submission.preview['reddit_video_preview']['width']
                    db.session.add(new_reddit_data)
                    db.session.commit()

                elif 'redd.it' in submission.url or 'imgur' in submission.url:
                    new_reddit_data.reddit_url = submission.url
                    new_reddit_data.height = submission.preview['images'][0]['source']['height']
                    new_reddit_data.width = submission.preview['images'][0]['source']['width']
                    if 'gif' in submission.url:
                        new_reddit_data.content_type = 'gif'
                    elif 'png' in submission.url:
                        fn = download_media(submission.url, submission.subreddit_name_prefixed, submission.id, 'png')
                        new_reddit_data.content_type = 'image/png'
                        new_reddit_data.local_filename = fn
                    elif 'jpg' in submission.url or 'jpeg' in submission.url:
                        fn = download_media(submission.url, submission.subreddit_name_prefixed, submission.id, 'jpg')
                        new_reddit_data.content_type = 'image/jpg'
                        new_reddit_data.local_filename = fn
                    db.session.add(new_reddit_data)
                    db.session.commit()

                elif 'gallery' in submission.url:
                    if hasattr(submission, 'crosspost_parent_list'):
                        vals = submission.crosspost_parent_list[0]['media_metadata']
                    else:
                        vals = submission.media_metadata
                    for d in vals:
                        fn = download_media(media["u"], submission.subreddit_name_prefixed, submission.id, 'jpg')
                        reddit_gallery_data = RedditDataModel(
                            reddit_submission_id=submission.id,
                            created_utc=submission.created_utc,
                            score=submission.score,
                            subreddit_name_prefixed=submission.subreddit_name_prefixed,
                            is_gallery=True,
                            local_filename=fn
                        )
                        media = vals[d]["s"]
                        reddit_gallery_data.reddit_url = media["u"]
                        reddit_gallery_data.content_type = "gallery/" + vals[d]["m"]
                        reddit_gallery_data.height = media["y"]
                        reddit_gallery_data.width = media["x"]
                        db.session.add(reddit_gallery_data)
                        db.session.commit()

                else:
                    raise RedditSubmissionProcessingError(submission.id, submission.url)
            except KeyError as e:
                print(f"Key Error: {e}\nSubmission: {vars(submission)}")

            except AttributeError as e:
                print(f"Attribute Error: {e}\nSubmission: {vars(submission)}")

            except RedditSubmissionProcessingError as e:
                print(e)

            finally:
                pass

        else:
            print(f"Submission {submission.id} exists in db.")



def subreddit_job(subreddit_name, sort, time_filter):
    asyncio.run(process_subreddit(subreddit_name, sort, time_filter))


def multireddit_job(multireddit_name, sort, time_filter):
    asyncio.run(process_multireddit(multireddit_name, sort, time_filter))

# for testing...
job = {
        "id": "sr-1",
        "func": "src.jobs:subreddit_job",
        "coalesce": True,
        "args": ("NewYorkNine", "top", "day"),
        "max_instances": 1,
        "trigger": "interval",
        "seconds": 6
}





