import asyncio
import logging
import os
from time import sleep

import asyncpraw

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
    asyncio.run(process_subreddit())
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

async def process_subreddit():
    rc = reddit_client()
    sr = await rc.subreddit("NewYorkNine", fetch=True)
    # async for submission in sr.top(time_filter="day"):
    count = 0;
    async for submission in sr.hot():
        # await submission.load()
        # print(f"\nsubmission....\n {vars(submission)}")
        # if submission._fetched is not True:
        #     print(f"the submission {submission.id} has not been fetched!Loading...")
        #     await submission.load()
        with scheduler.app.app_context():
            submission_lookup = RedditDataModel.query.filter_by(reddit_submission_id=submission.id)
            result = db.session.execute(submission_lookup).scalar()
            if result is None:
                try:
                    if 'gif' in submission.url or "gfycat" in submission.url:
                        if isinstance(submission.media, dict):
                            new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                              created_utc=submission.created_utc,
                                                              reddit_url=submission.preview['reddit_video_preview']['scrubber_media_url'],
                                                              content_type=submission.preview['reddit_video_preview']['is_gif'],
                                                              height=submission.preview['reddit_video_preview']['height'],
                                                              width=submission.preview['reddit_video_preview']['width'],
                                                              oembed_html=submission.media["oembed"]["html"],
                                                              score=submission.score
                                                              )
                            db.session.add(new_reddit_data)
                            db.session.commit()

                        elif "redd.it" in submission.url:
                            new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                              created_utc=submission.created_utc,
                                                              reddit_url=submission.url,
                                                              content_type="gif",
                                                              height=submission.preview['images'][0]['source']['height'],
                                                              width=submission.preview['images'][0]['source']['width'],
                                                              oembed_html=None,
                                                              score=submission.score
                                                              )
                            db.session.add(new_reddit_data)
                            db.session.commit()
                        elif ".gifv" in submission.url:
                            url_replace = submission.url.replace(".gifv", ".mp4")
                            new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                              created_utc=submission.created_utc,
                                                              reddit_url=url_replace,
                                                              content_type="gif/mp4",
                                                              height=submission.preview['reddit_video_preview']['height'],
                                                              width=submission.preview['reddit_video_preview']['width'],
                                                              oembed_html=None,
                                                              score=submission.score
                                                              )
                            db.session.add(new_reddit_data)
                            db.session.commit()

                    elif "preview" in vars(submission):
                        new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                          created_utc=submission.created_utc,
                                                          reddit_url=submission.url,
                                                          content_type="image",
                                                          height=submission.preview['images'][0]['source']['height'],
                                                          width=submission.preview['images'][0]['source']['width'],
                                                          oembed_html=None,
                                                          score=submission.score
                                                          )
                        db.session.add(new_reddit_data)
                        db.session.commit()
                    elif submission.is_gallery is True:
                        vals = submission.media_metadata
                        for d in vals:
                            media = vals[d]["s"]
                            new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                              created_utc=submission.created_utc,
                                                              reddit_url=media["u"],
                                                              content_type=vals[d]["m"],
                                                              height=media["y"],
                                                              width=media["x"],
                                                              oembed_html=None,
                                                              score=submission.score
                                                              )
                            db.session.add(new_reddit_data)
                            db.session.commit()
                    else:
                        raise RedditSubmissionProcessingError(submission.id, submission.url)

                except KeyError as e:
                    print(f"Key Error: {e}\nSubmission: {vars(submission)}")
                    pass
                except AttributeError as e:
                    print(f"Attribute Error: {e}\nSubmission: {vars(submission)}")
                    pass
                except RedditSubmissionProcessingError as e:
                    print(e)
                    pass
                finally:
                    count += 1
                    continue
            else:
                count += 1
                print(f"Submission {submission.id} exists in db.")
    await rc.close()
    print(f"\nJob Complete, count: {count}")




async def process_reddit_multi():
    rc = reddit_client()
    multi = await rc.multireddit(redditor="kjoneslol", name='sfwpornnetwork', fetch=True)
    async for submission in multi.top(time_filter="day", limit=100):
        # print(f"\nsubmission....\n {vars(submission)}")
        with scheduler.app.app_context():
            submission_lookup = RedditDataModel.query.filter_by(reddit_submission_id=submission.id)
            result = db.session.execute(submission_lookup).scalar()
            if result is None:
                if 'gif' in submission.url:
                    if submission.media == 'None':
                        new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                          created_utc=submission.created_utc,
                                                          reddit_url=submission.url,
                                                          content_type=submission.media.type,
                                                          height=submission.media.height,
                                                          width=submission.media.width,
                                                          oembed_html=submission.media.oembed.html,
                                                          score=submission.score
                                                          )
                        # with scheduler.app.app_context():
                        db.session.add(new_reddit_data)
                        db.session.commit()

                    else:
                        if "redd.it" in submission.url:
                            new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                              created_utc=submission.created_utc,
                                                              reddit_url=submission.url,
                                                              content_type="gif",
                                                              height=submission.preview['images'][0]['source']['height'],
                                                              width=submission.preview['images'][0]['source']['width'],
                                                              oembed_html=None,
                                                              score=submission.score
                                                              )
                            # with scheduler.app.app_context():
                            db.session.add(new_reddit_data)
                            db.session.commit()
                        else:
                            url_replace = submission.url.replace(".gifv", ".mp4")
                            new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                              created_utc=submission.created_utc,
                                                              reddit_url=url_replace,
                                                              content_type="gif/mp4",
                                                              height=submission.preview['reddit_video_preview']['height'],
                                                              width=submission.preview['reddit_video_preview']['width'],
                                                              oembed_html=None,
                                                              score=submission.score
                                                              )
                            # with scheduler.app.app_context():
                            db.session.add(new_reddit_data)
                            db.session.commit()
                else:
                    new_reddit_data = RedditDataModel(reddit_submission_id=submission.id,
                                                      created_utc=submission.created_utc,
                                                      reddit_url=submission.url,
                                                      content_type="image",
                                                      height=submission.preview['images'][0]['source']['height'],
                                                      width=submission.preview['images'][0]['source']['width'],
                                                      oembed_html=None,
                                                      score=submission.score
                                                      )
                    # with scheduler.app.app_context():
                    db.session.add(new_reddit_data)
                    db.session.commit()
            else:
                print(f"Submission {submission.id} exists in db.")
    await rc.close()



job = {
        "id": "reddit-rr",
        "func": "src:redditJob",
        "coalesce": True,
        "max_instances": 1,
        "trigger": "interval",
        "hours": 6
    }


