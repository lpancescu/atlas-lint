from __future__ import unicode_literals, print_function

import json
import urllib2


class Box(object):
    def __init__(self, publisher, name):
        json_url = "https://atlas.hashicorp.com/{0}/boxes/{1}/"\
                    .format(publisher, name)
        request = urllib2.Request(json_url, None,
                    {'Accept': 'application/json'})
        json_file = urllib2.urlopen(request)
        self._data = json.loads(json_file.read())

    def versions(self):
        return tuple(v['version'] for v in self._data['versions']
                                    if v['status'] == 'active')

    def providers(self, version):
        _ver = ([v for v in self._data['versions']
                    if v['version'] == version])[0]
        return [p['name'] for p in _ver['providers']]

    def url(self, version, provider):
        _ver = ([v for v in self._data['versions']
                    if v['version'] == version])[0]
        return ([p for p in _ver['providers']
                    if p['name'] == provider])[0]['url']