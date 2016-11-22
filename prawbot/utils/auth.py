import shelve
import functools

import flask

auth_app = flask.Flask(__name__)


def retrieve_oauth_credentials():

    with shelve.open('api_creds') as key_store:
        try:
            credentials = {
                'access_token': key_store['access_token'],
                'refresh_token': key_store['refresh_token'],
                'scope': key_store['scope']
            }
        except KeyError:
            credentials = None

    return credentials


def store_oauth_credentials(api_client, code):
    info = api_client.get_access_information(code)
    with shelve.open('api_creds') as key_store:
        key_store['access_token'] = info['access_token']
        key_store['refresh_token'] = info['refresh_token']
        key_store['scope'] = info['scope']


def start_server(api_client, host, port):
    auth_app.config['credentials_set_func'] = functools.partial(store_oauth_credentials, api_client)
    auth_app.run(host=host,
                 port=port)


def stop_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@auth_app.route('/authorize_callback')
def authorize_callback():
    code = flask.request.args.get('code', '')
    auth_app.config['credentials_set_func'](code)
    stop_server()
    return 'Done!'
