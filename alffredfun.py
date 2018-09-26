# coding=utf-8

# -*- coding: utf-8 -*-
import itertools
import os
import sys
import unicodedata
from xml.etree.ElementTree import Element, SubElement, tostring

"""
You should run your script via /bin/bash with all escape options ticked.
The command line should be

python yourscript.py "{query}" arg2 arg3 ...
"""
UNESCAPE_CHARACTERS = u""" ;()"""

_MAX_RESULTS_DEFAULT = 9

# preferences = plistlib.readPlist('info.plist')
bundleid = 'xingmo'


class Item(object):
    @classmethod
    def unicode(cls, value):
        try:
            items = iter(value.items())
        except AttributeError:
            return unicode(value)
        else:
            return dict(map(unicode, item) for item in items)

    def __init__(self, attributes, title, subtitle=None, icon=None):
        self.attributes = attributes
        self.title = title
        self.subtitle = subtitle
        self.icon = icon

    def __str__(self):
        return tostring(self.xml()).decode('utf-8')

    def xml(self):
        item = Element(u'item', self.unicode(self.attributes))
        for attribute in (u'title', u'subtitle', u'icon'):
            value = getattr(self, attribute)
            if value is None:
                continue
            if len(value) == 2 and isinstance(value[1], dict):
                (value, attributes) = value
            else:
                attributes = {}
            SubElement(item, attribute, self.unicode(attributes)).text = self.unicode(value)
        return item


def args(characters=None):
    return tuple(unescape(decode(arg), characters) for arg in sys.argv[1:])


def config():
    return _create('config')


def decode(s):
    return unicodedata.normalize('NFD', s.decode('utf-8'))


def env(key):
    return os.environ['alfred_%s' % key]


def uid(uid):
    return u'-'.join(map(str, (bundleid, uid)))


def unescape(query, characters=None):
    for character in (UNESCAPE_CHARACTERS if (characters is None) else characters):
        query = query.replace('\\%s' % character, character)
    return query


def work(volatile):
    path = {
        True: env('workflow_cache'),
        False: env('workflow_data')
    }[bool(volatile)]
    return _create(path)


def write(text):
    sys.stdout.write(text)


def xml(items, maxresults=_MAX_RESULTS_DEFAULT):
    root = Element('items')
    for item in itertools.islice(items, maxresults):
        root.append(item.xml())
    return tostring(root, encoding='utf-8')


def _create(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.access(path, os.W_OK):
        raise IOError('No write access: %s' % path)
    return path


def main():
    result = []
    result.append(Item({"uid": uid("fun")}, title=u'%s' % args("1")))
    write(xml(result))

'''
if __name__ == '__main__':
    main()
'''
# main()
print uid(100)