import os
import re
import sys

APPS = [
    ['Android Studio', 'androidstudio', 'com.google.android.studio'],
    ['AppCode', 'appcode', 'com.jetbrains.appcode'],
    ['CLion', 'clion', 'com.jetbrains.clion'],
    ['DataGrip', 'datagrip', 'com.jetbrains.datagrip'],
    ['GoLand', 'goland', 'com.jetbrains.goland'],
    ['IntelliJ IDEA', 'idea', 'com.jetbrains.intellij'],
    ['PhpStorm', 'phpstorm', 'com.jetbrains.phpstorm'],
    ['PyCharm', 'pycharm', 'com.jetbrains.pycharm'],
    ['RustRover', 'rustrover', 'com.jetbrains.rustrover'],
    ['WebStorm', 'webstorm', 'com.jetbrains.webstorm'],
]


def prepare_workflow(app):
    app_name, keyword, bundle = app
    version = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    version = re.sub(r'v(.*)', r'\1', version)
    print(f"Building {app_name} v{version}")
    os.system(f'mkdir -p out/{keyword}')
    os.system(f'cp icons/{keyword}.png ./out/{keyword}/icon.png')
    os.system(f'cp icons/{keyword}.png ./out/{keyword}/36E4312B-0CAB-4AE7-A8B6-E30EAF07B766.png')
    os.system('sed '
              f'-e "s/%APPNAME%/{app_name}/g" '
              f'-e "s/%KEYWORD%/{keyword}/g" '
              f'-e "s/%BUNDLE%/{bundle}/g" '
              f'-e "s/%VERSION%/{version}/g" '
              f' alfred/info.plist > out/{keyword}/info.plist')
    os.system(f'zip -j -r {keyword}.alfredworkflow out/{keyword}/* recent_projects.py products.json')


def build():
    for app in APPS:
        prepare_workflow(app)


def clean():
    os.system("rm *.alfredworkflow")


def main():
    clean()
    build()


if __name__ == '__main__':
    main()
