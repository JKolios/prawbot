import re

DEFAULT_URL_REGEX = re.compile("""http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+""")


def find_urls(text, regex=DEFAULT_URL_REGEX):
    urls = re.findall(regex, text)
    return urls
