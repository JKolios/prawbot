import sched
from datetime import datetime
import sys
from praw.helpers import comment_stream

from utils.url_finder import find_urls
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class Bot(object):
    def __init__(self, api_client):
        self.client = api_client

    def configure(self, *args, **kwargs):
        pass

    def func(self, *args, **kwargs):
        log.info('Override this!')
        raise NotImplementedError

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class ExampleBot(Bot):
    def func(self, *args, **kwargs):
        subreddits = ['funny', 'videos']
        results = []

        for subreddit in subreddits:
            api_sub = self.client.get_subreddit(subreddit)
            submissions = [submission.title for submission in api_sub.get_hot()]
            results.append(submissions)
        current_time = datetime.now().isoformat()
        log.info(current_time, results)


class PeriodicBot(Bot):
    def __init__(self, api_client):
        self.period = None
        self.scheduler = sched.scheduler()
        super().__init__(api_client)

    def run(self, *args, **kwargs):
        if not self.period:
            raise ValueError('Self.period must be set by configure()')

        while True:
            self.scheduler.enter(self.period, 1, self.func, args, kwargs)
            self.scheduler.run()


class CommentStreamBot(Bot):
    def __init__(self, api_client):
        self.subreddit = None
        super().__init__(api_client)

    def run(self, *args, **kwargs):

        if not self.subreddit:
            raise ValueError('Self.subreddit must be set by configure()')

        try:
            for comment in comment_stream(self.client, self.subreddit, verbosity=0):
                self.func(comment, *args, **kwargs)
        except KeyboardInterrupt:
            log.info('Got a KeyboardInterrupt, running exit handler')
            self.exit_handler()
            sys.exit()

    def exit_handler(self):
        pass


class ExampleCommentStreamBot(CommentStreamBot):
    def func(self, comment, *args, **kwargs):
        current_time = datetime.utcnow().isoformat()
        comment_time = datetime.utcfromtimestamp(comment.created).isoformat()
        urls = find_urls(comment.body)
        log.info('Current time: {0} Comment time:{1}  Comment body: {2} URLs: {3}'.format(
            current_time, comment_time, comment.body, urls))
