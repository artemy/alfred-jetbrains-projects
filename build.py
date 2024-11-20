import json
import os
import plistlib
import re
import sys
import uuid


def create_connection(destination_uid):
    return [{'destinationuid': destination_uid, 'modifiers': 0, 'modifiersubtext': '',
             'vitoclose': False}]


def create_object(keyword, app_name, uid):
    return {
        'config': {'alfredfiltersresults': False, 'alfredfiltersresultsmatchmode': 0,
                   'argumenttreatemptyqueryasnil': False,
                   'argumenttrimmode': 0, 'argumenttype': 1, 'escaping': 102, 'keyword': f'{{var:{keyword}}}',
                   'queuedelaycustom': 3, 'queuedelayimmediatelyinitially': True, 'queuedelaymode': 0, 'queuemode': 1,
                   'runningsubtext': '', 'script': f'python3 recent_projects.py {keyword} "{{query}}"',
                   'scriptargtype': 0,
                   'scriptfile': '', 'subtext': '', 'title': f'Search through your recent {app_name} projects',
                   'type': 0,
                   'withspace': True}, 'type': 'alfred.workflow.input.scriptfilter',
        'uid': uid, 'version': 3}


def create_userconfigurationconfig(keyword, app_name):
    return {'config': {'default': '', 'placeholder': keyword, 'required': False, 'trim': True},
            'description': 'Leave this blank to disable this IDE',
            'label': f'{app_name} Keyword', 'type': 'textfield',
            'variable': keyword}


def create_uidata(xpos, ypos):
    return {'xpos': xpos, 'ypos': ypos}


def build():
    # Collect info
    with open('products.json', 'r') as outfile:
        APPS = json.load(outfile)

    with open('alfred/template.plist', 'rb') as fp:
        plist = plistlib.load(fp)

    keywords = APPS.keys()
    app_names = [item.get('display-name', item['folder-name']) for item in APPS.values()]
    uids = [str(uuid.uuid4()).upper() for _ in range(len(keywords))]

    start = 30
    number = len(keywords)
    step = 120

    y_coordinates = list(range(start, start + (step * number), step))

    version = sys.argv[1] if len(sys.argv) > 1 else "unknown"

    # Modify plist
    if not (len(keywords) == len(app_names) == len(uids) == len(y_coordinates)):
        raise ValueError("All of the lists must be equal length.")

    # Get the UID of the runscript action in the template
    script_uid = None
    for object in plist["objects"]:
        if object["config"]["script"] == 'open -nb $bundle_id --args $@':
            script_uid = object["uid"]
            break
    if script_uid is None:
        raise ValueError(f"Could not find the script object with 'open -nb $bundle_id --args $@' as the script in the template")


    plist["connections"].update({uid: create_connection(script_uid) for uid in uids})

    plist["uidata"].update({uid: create_uidata(30, coord) for uid, coord in zip(uids, y_coordinates)})

    plist["uidata"][script_uid]["ypos"] = min(y_coordinates) + (max(y_coordinates) - min(y_coordinates)) / 2

    plist["objects"].extend(
        [create_object(keyword, app_name, uid) for keyword, app_name, uid in zip(keywords, app_names, uids)])

    plist["userconfigurationconfig"].extend(
        [create_userconfigurationconfig(keyword, app_name) for keyword, app_name in zip(keywords, app_names)])

    plist["version"] = version

    with open("README.md", 'r', encoding='utf-8') as file:
        content = file.read()
        # Replace nested .readme paths with flattened paths
        content = re.sub(r'\.readme/(?:[^/\s]+/)*([^/\s]+)', r'\1', content)

        plist["readme"] = content

    # Output
    print(f"Building {app_names}")
    os.system(f'mkdir -p out')

    with open('out/info.plist', 'wb') as fp:
        plistlib.dump(plist, fp)

    for i, keyword in enumerate(keywords):
        os.system(f'cp icons/{keyword}.png ./out/{uids[i]}.png')

    os.system(
        f'zip -j -r alfred-jetbrains-projects.alfredworkflow out/* recent_projects.py products.json icon.png .readme/*')


def clean():
    os.system("rm *.alfredworkflow")


def main():
    clean()
    build()


if __name__ == '__main__':
    main()
