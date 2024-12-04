import json
import os
import plistlib
import re
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    keyword: str
    uid: str
    folder_name: str
    bundle_id: str
    display_name: Optional[str] = None
    preferences_path: Optional[str] = None

    def name(self) -> str:
        return self.display_name if self.display_name else self.folder_name


def create_connection(destination_uid: str) -> list[dict]:
    return [{'destinationuid': destination_uid,
             'modifiers': 0,
             'modifiersubtext': '',
             'vitoclose': False}]


def create_script_filter(product: Product) -> dict:
    return {
        'config': {'alfredfiltersresults': False,
                   'alfredfiltersresultsmatchmode': 0,
                   'argumenttreatemptyqueryasnil': False,
                   'argumenttrimmode': 0,
                   'argumenttype': 1,
                   'escaping': 102,
                   'keyword': f'{{var:{product.keyword}}}',
                   'queuedelaycustom': 3,
                   'queuedelayimmediatelyinitially': True,
                   'queuedelaymode': 0,
                   'queuemode': 1,
                   'runningsubtext': '',
                   'script': f'/usr/bin/python3 recent_projects.py {product.keyword} "{{query}}"',
                   'scriptargtype': 0,
                   'scriptfile': '',
                   'subtext': '',
                   'skipuniversalaction': True,
                   'title': f'Search through your recent {product.name()} projects',
                   'type': 0,
                   'withspace': True},
        'type': 'alfred.workflow.input.scriptfilter',
        'uid': product.uid,
        'version': 3}


def create_userconfigurationconfig(product: Product) -> dict:
    return {'config': {'default': '',
                       'placeholder': product.keyword,
                       'required': False,
                       'trim': True},
            'description': f'Assign a keyword to enable {product.name()}',
            'label': f'{product.name()} keyword',
            'type': 'textfield',
            'variable': product.keyword}


def create_coordinates(xpos: int, ypos: int) -> dict[str, int]:
    return {'xpos': xpos, 'ypos': ypos}


def get_run_script_uid(plist) -> str:
    for obj in plist["objects"]:
        if obj["config"]["script"] == 'open -nb $bundle_id --args $@' and obj["uid"] is not None:
            return obj["uid"]
    raise ValueError(
        f"Could not find the script object with 'open -nb $bundle_id --args $@' as the script in the template")


def create_coordinate_ruler(size: int) -> list[int]:
    start = 40
    step = 120
    return list(range(start, start + (step * size), step))


def build():
    # Collect info
    products = get_products()

    with open('alfred/template.plist', 'rb') as fp:
        plist = plistlib.load(fp)

    version = sys.argv[1] if len(sys.argv) > 1 else "unknown"

    # Modify plist
    # Get the UID of the runscript action in the template
    run_script_uid = get_run_script_uid(plist)
    run_script_connection = create_connection(run_script_uid)

    plist["connections"].update({product.uid: run_script_connection for product in products})

    y_coordinate_ruler = create_coordinate_ruler(len(products))
    plist["uidata"].update(
        {product.uid: create_coordinates(30, coord) for product, coord in zip(products, y_coordinate_ruler)})

    plist["uidata"][run_script_uid]["ypos"] = sum(y_coordinate_ruler) / len(y_coordinate_ruler)

    plist["objects"].extend([create_script_filter(product) for product in products])

    plist["userconfigurationconfig"].extend([create_userconfigurationconfig(product) for product in products])

    plist["version"] = version

    with open(".readme/embedded-readme.md", 'r', encoding='utf-8') as file:
        plist["readme"] = file.read()

    # Output
    print(f"Building {[product.name() for product in products]}")
    os.system(f'mkdir -p out')

    with open('out/info.plist', 'wb') as fp:
        plistlib.dump(plist, fp)

    for product in products:
        os.system(f'cp icons/{product.keyword}.png ./out/{product.uid}.png')

    os.system(
        f'zip -j -r alfred-jetbrains-projects.alfredworkflow out/* recent_projects.py products.json icon.png')


def get_products() -> list[Product]:
    with open('products.json', 'r') as outfile:
        js = json.load(outfile)
        products = [Product(k, **v) for k, v in js.items()]
    return products


def clean():
    os.system("rm out/*")
    os.system("rm *.alfredworkflow")


def main():
    clean()
    build()


if __name__ == '__main__':
    main()
