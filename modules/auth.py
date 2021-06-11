"""
AUTHOR: Keiber Urbila
CREATION DATE: 10/06/21
"""
from flask import request
import urllib.parse as urlparse


def is_safe_url(target):
    """
    A function that ensures that a redirect target will lead to the same server
    A common pattern with form processing is to automatically redirect back to
    the user. There are usually two ways this is done: by inspecting a next URL
    parameter or by looking at the HTTP referrer. Unfortunately you also have
    to make sure that users are not redirected to malicious attacker's pages
    and just to the same host. Source: http://flask.pocoo.org/snippets/62/
    """
    ref_url = urlparse.urlparse(request.host_url)
    test_url = urlparse.urlparse(urlparse.urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and \
        ref_url.netloc == test_url.netloc
