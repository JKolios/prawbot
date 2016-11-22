import logging
import urllib.parse

import praw

import utils.auth

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


def create_bot(user_agent, client_id, client_secret, redirect_uri, required_scopes, bot_class, *args, **kwargs):
    api_client = praw.Reddit(user_agent)
    api_client.set_oauth_app_info(client_id=client_id,
                                  client_secret=client_secret,
                                  redirect_uri=redirect_uri)

    oauth_credentials = utils.auth.retrieve_oauth_credentials()
    if not oauth_credentials:
        auth_url = api_client.get_authorize_url(state=bot_class.__name__,
                                                scope=required_scopes,
                                                refreshable=True)
        log.info('Please visit: {0} to start the OAuth process.'.format(auth_url))
        redirect_uri_elements = urllib.parse.urlparse(redirect_uri)
        redirect_uri_host = redirect_uri_elements.netloc
        utils.auth.start_server(api_client,
                                host=redirect_uri_host[:redirect_uri_host.find(':')],
                                port=redirect_uri_elements.port)
        oauth_credentials = utils.auth.retrieve_oauth_credentials()

    api_client.set_access_credentials(**oauth_credentials)
    bot = bot_class(api_client)
    bot.configure(*args, **kwargs)
    return bot
