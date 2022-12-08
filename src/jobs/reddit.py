import asyncio
import logging
import os
from time import sleep

import asyncpraw
from flask import current_app, session, url_for
from werkzeug.utils import secure_filename

from src.extensions.scheduler import scheduler
# from src.extensions.scheduler import scheduler
from src.models import RedditDataModel
from src.extensions.db import db

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


async def get_subreddit_data():
    rc = reddit_client()
    print(f"read only reddit client: {rc.read_only}")
    await rc.close()


def redditJob():
    print(f"running function redditJob")
    asyncio.run(psubreddit("NewYorkNine", "day"))
    # asyncio.run(process_reddit_multi())
    # sleep(10)


def callback(future):
    print(f"callback {future.title}")


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


def download_media(media, folder):
    media = requests.get('https://i.redd.it/9yzxvmmccnv81.jpg')
    b = BytesIO(media.content)
    target = os.path.join(current_app.config['UPLOAD_FOLDER'], f'reddit/{folder}')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = media
    if file.filename == '':
        return
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    session['uploadFilePath'] = destination
    item_image_url = url_for('download_item_image_file', name=filename)
    return destination


async def psubreddit(subreddit_name, time_filter):
    rc = reddit_client()
    sr = await rc.subreddit(subreddit_name, fetch=True)
    count = 0
    # async for submission in sr.top(time_filter=time_filter, limit=100):
    async for submission in sr.hot():
        with scheduler.app.app_context():
            submission_lookup = RedditDataModel.query.filter_by(reddit_submission_id=submission.id)
            result = db.session.execute(submission_lookup).scalar()
            if result is None:
                try:
                    # download_media(submission.url, subreddit_name)
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
                            new_reddit_data.content_type = 'image/png'
                        elif 'jpg' in submission.url or 'jpeg' in submission.url:
                            new_reddit_data.content_type = 'image/jpg'
                        db.session.add(new_reddit_data)
                        db.session.commit()

                    elif 'gallery' in submission.url:
                        if hasattr(submission, 'crosspost_parent_list'):
                            vals = submission.crosspost_parent_list[0]['media_metadata']
                        else:
                            vals = submission.media_metadata
                        for d in vals:
                            reddit_gallery_data = RedditDataModel(
                                reddit_submission_id=submission.id,
                                created_utc=submission.created_utc,
                                score=submission.score,
                                subreddit_name_prefixed=submission.subreddit_name_prefixed,
                                is_gallery=True
                            )
                            media = vals[d]["s"]
                            reddit_gallery_data.reddit_url = media["u"]
                            reddit_gallery_data.content_type = "gallery/"+vals[d]["m"]
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

                # except TypeError as e:
                #     print(f"Type Error... {submission.url}\n{vars(submission)}\n")
                finally:
                    count += 1

            else:
                print(f"Submission {submission.id} exists in db.")
                count += 1
                continue
    print(f"Process count: {count}")
    await rc.close()





job = {
        "id": "reddit-rr",
        "func": "src:redditJob",
        "coalesce": True,
        "max_instances": 1,
        "trigger": "interval",
        "hours": 6
    }


