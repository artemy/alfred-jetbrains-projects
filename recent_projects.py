#!/usr/bin/env python

import json
import os
import sys
from xml.etree import ElementTree

RECENT_PROJECT_DIRECTORIES_XML = 'recentProjectDirectories.xml'

RECENT_PROJECTS_FILENAME = {'Idea': 'recentProjects.xml'}


class AlfredItem:
    def __init__(self, title, arg, type="file"):
        self.title = title
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


def recent_projects_filename(app):
    return '/options/{0}'.format(RECENT_PROJECTS_FILENAME.get(app, RECENT_PROJECT_DIRECTORIES_XML))


def create_json(targets):
    alfred = AlfredOutput(items=[AlfredItem(arg=target, title=target) for target in targets])
    print CustomEncoder().encode(alfred)


def find_recent_files_xml():
    try:
        app = sys.argv[1]
        preferences_path = os.path.expanduser("~/Library/Preferences/")
        most_recent_preferences = max([x for x in next(os.walk(preferences_path))[1] if app in x])
        return preferences_path + most_recent_preferences + recent_projects_filename(app)
    except IndexError:
        print "no app specified, exiting"
        exit(1)


def main():
    most_recent_projects_file = find_recent_files_xml()

    projects = read_projects(most_recent_projects_file)

    projects = filter_projects(projects)

    return create_json(projects)


def read_projects(most_recent_projects_file):
    tree = ElementTree.parse(most_recent_projects_file)
    xpath = ".//option[@name='recentPaths']/list/option"
    objects = tree.findall(xpath)
    targets = [o.attrib['value'].replace('$USER_HOME$', "~") for o in objects]
    return targets


def filter_projects(targets):
    try:
        query = sys.argv[2]
        if len(query) < 1:
            raise IndexError
        return [t for t in targets if query in t]
    except IndexError:
        return targets


if __name__ == "__main__":
    main()
