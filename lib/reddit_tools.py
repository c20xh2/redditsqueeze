import praw
from os import getenv


class squeeze_reddit():
    def __init__(self):
        self.client = None
        self.post_limit = 15
        self.get_client()

    def get_client(self):
        client_id = getenv('REDDIT_CLIENT_ID')
        client_secret = getenv('REDDIT_CLIENT_SECRET')

        self.client = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Comment Extraction (by u/thao)",
        )