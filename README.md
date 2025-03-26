# Recent JetBrains Projects for Alfred

![test & release](https://github.com/artemy/alfred-jetbrains-projects/workflows/test%20&%20release/badge.svg)
![MIT License](https://img.shields.io/github/license/artemy/alfred-jetbrains-projects)

An Alfred workflow for opening your JetBrains IDEs projects

![image](.readme/images/screenshot.png)

## Getting started

### Prerequisites

Project requires Python 3.9+ to run, which is not included by default with macOS. You can install Python 3 using
this [guide](https://docs.python-guide.org/starting/install3/osx/).

### Installing

Download the `alfred-jetbrains-projects.alfredworkflow` file from the latest release
at [Releases](https://github.com/artemy/alfred-jetbrains-projects/releases) page and open it with Alfred.

### ⚠️ Assign a keyword for every IDE you use ⚠️

By default, all IDEs are disabled. Assigning keywords activates specific IDEs:
<img src="https://github.com/artemy/alfred-jetbrains-projects/raw/master/.readme/images/configuration.png" width="50%" height="50%">

Keyword settings are persisted across workflow upgrades.

## How to Use

Open Alfred and type the keyword for your IDE (see Supported IDEs below).
The workflow will display a list of recent
projects (sorted by time last opened descending).

You can further filter a project list by typing additional characters.
Fuzzy first-letter search is supported (i.e.,
typing `map` will find `my-awesome-project`):

![animation](.readme/images/animation.gif)

### Supported IDEs

| IDE Name                  | Version | Keyword       |
|---------------------------|---------|---------------|
| Android Studio            | 4.1+    | androidstudio |
| AppCode                   | 2020.3+ | appcode       |
| CLion                     | 2020.3+ | clion         |
| DataGrip                  | 2020.3+ | datagrip      |
| GoLand                    | 2020.3+ | goland        |
| IntelliJ IDEA             | 2020.3+ | idea          |
| PhpStorm                  | 2024.3+ | phpstorm      |
| PyCharm Professional      | 2020.3+ | pycharm       |
| PyCharm Community Edition | 2024.3+ | pycharmce     |
| Rider                     | 2024.3+ | rider         |
| RubyMine                  | 2024.3+ | rubymine      |
| RustRover                 | 2024.1+ | rustrover     |
| WebStorm                  | 2020.3+ | webstorm      |

Support for older IDE versions is not guaranteed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Running the tests

Make sure to first install test dependencies:

```shell
pip3 install -r requirements.txt
```

To run tests, execute

```shell
python3 -m recent_projects_test
```

If you want to get coverage figures through `coverage` tool:

```shell
coverage run -m unittest recent_projects_test # gather test data
coverage report -m # display coverage figures
```

## Built With

* [Python 3.9](https://docs.python.org/3.9/)
* [coverage.py](https://coverage.readthedocs.io/) - Code coverage measurement

## License

This project is licensed under the MIT License — see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

See [CONTRIBUTORS.md](CONTRIBUTORS.md)
and [contributors](https://github.com/artemy/alfred-jetbrains-projects/contributors) for the list of contributors.

## Legal

This workflow is not associated with JetBrains in any way.

Copyright © 2024 JetBrains s.r.o. JetBrains and the JetBrains logo are trademarks of JetBrains s.r.o.
