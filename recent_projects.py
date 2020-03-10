#!/usr/bin/env python

import json
import os
import sys
from xml.etree import ElementTree


class AlfredItem:
    def __init__(self, title, subtitle, arg, type="file"):
        self.title = title
        self.subtitle = subtitle
        self.arg = arg
        self.type = type


class AlfredOutput:
    def __init__(self, items):
        self.items = items


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AlfredItem) | isinstance(obj, AlfredOutput):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def create_json(targets):
    alfred = AlfredOutput(items=[AlfredItem(title=target.split('/')[-1], subtitle=target, arg=target) for target in targets])
    print CustomEncoder().encode(alfred)


def read_app_data(app):
    try:
        with open('products.json', 'r') as outfile:
            data = json.load(outfile)
            return data[app]
    except IOError:
        print "can't open file"
    except KeyError:
        print "App '{}' is not found in the products.json".format(app)
    exit(1)


def find_recent_files_xml(application):
    preferences_path = os.path.expanduser("~/Library/Preferences/")
    most_recent_preferences = max(
        [x for x in next(os.walk(preferences_path))[1] if application['folder-name'] in x])
    return '{}{}/options/{}.xml'.format(preferences_path, most_recent_preferences, application['xml-name'])


def main():
    try:
        application = read_app_data(sys.argv[1])
        most_recent_projects_file = find_recent_files_xml(application)

        projects = read_projects(most_recent_projects_file)
        projects = filter_projects(projects)

        create_json(projects)
    except IndexError:
        print "no app specified, exiting"
        exit(1)


def read_projects(most_recent_projects_file):
    tree = ElementTree.parse(most_recent_projects_file)
    xpath = ".//option[@name='recentPaths']/list/option"
    objects = tree.findall(xpath)
    targets = [o.attrib['value'].replace('$USER_HOME$', "~") for o in objects]
    return targets


def smart_filter(entry, query):
    previous_was_break = False
    abbreviation = entry[1][0]
    for char in entry[1][1: len(entry[1]): 1]:
        if char == "_" or char == "-":
            previous_was_break = True
        else:
            if previous_was_break:
                abbreviation += char
                previous_was_break = False
    return query in entry[0] or query in abbreviation


def filter_projects(targets):
    try:
        query = sys.argv[2].strip()
        if len(query) < 1:
            raise IndexError
        targets = map(lambda t: (t, t.split('/')[-1]), targets)
        results = filter(lambda t: smart_filter(t, query), targets)
        results.sort(key=lambda t: (query in t[1]), reverse=True)
        return map(lambda t: t[0], results)
    except IndexError:
        return targets


if __name__ == "__main__":
    main()
