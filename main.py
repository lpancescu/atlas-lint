#!/usr/bin/env python2.7
from __future__ import unicode_literals, print_function

import argparse
import logging
import sys
import httplib
import urllib2
from atlas.box import Box


def check_url(url):
    request = urllib2.Request(url)
    if request.get_type() == 'https':
        conn = httplib.HTTPSConnection(request.get_host())
    elif request.get_type() == 'http':
        conn = httplib.HTTPConnection(request.get_host())
    conn.request('HEAD', request.get_selector())
    response = conn.getresponse()
    if response.status == httplib.OK:
        logging.info('{}: OK'.format(url))
        return True
    elif response.status == httplib.FOUND:
        redirect_url = response.getheader('Location')
        logging.debug('{}: FOUND'.format(url))
        logging.debug('==> {}'.format(redirect_url))
        return check_url(redirect_url)
    else:
        logging.error('{}: {} {}'.format(url, response.status, response.reason))
        return False


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.NOTSET)
    result = True
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true',
                        help='check all box versions')
    parser.add_argument('boxes', nargs='+', metavar='box',
                        help='name of a box to check, e.g. centos/7')
    args = parser.parse_args()

    for box_name in args.boxes:
        box = Box(*box_name.split('/', 1))
        versions = list(box.versions())
        if not args.all:
            versions = versions[:1] # only test the latest version
        for version in versions:
            for provider in box.providers(version):
                url = box.url(version, provider)
                if not check_url(url):
                    result = False
    if not result:
        sys.exit(1)
