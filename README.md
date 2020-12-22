# JetBrains projects for Alfred

![Test & release artifacts](https://github.com/artemy/alfred-jetbrains-projects/workflows/Test%20&%20release%20artifacts/badge.svg?branch=master)
![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)

Alfred workflow for opening your JetBrains IDEs projects

![image](.readme/images/screenshot.png)

## Supported IDEs

| IDE Name | Version | Keyword |
| --- | --- | --- |
| Android Studio | 4.1+ | androidstudio |
| AppCode | 2020.3+ | appcode |
| CLion | 2020.3+ | clion |
| GoLand | 2020.3+ | goland |
| IntelliJ IDEA | 2020.3+ | idea |
| PyCharm | 2020.3+ | pycharm |
| WebStorm | 2020.3+ | webstorm |

Support for older IDE versions is not guaranteed.

## Getting started

### Prerequisites

Project uses standard Python 2.7 shipped with all modern OSX distributions. No dependencies are required for running the
workflow.

### Installing

Download `*.workflow` file for your IDE from the latest release
at [Releases](https://github.com/artemy/alfred-jetbrains-projects/releases) page and open it with Alfred.

### How to Use

Open Alfred and type keyword for your IDE (see Supported IDEs above). Workflow will display list of recent projects (
sorted by time last opened descending).

You can further filter project list by typing additional words. Fuzzy first-letter search is supported (i.e.
typing `map` will find `my-awesome-project`):

![animation](.readme/images/animation.gif)

## Running the tests

Make sure to first install test dependencies:

```shell
pip install -r requirements.txt
```

To run tests, execute

```shell
python -m recent_projects_test
```

If you want to get coverage figures through `coverage` tool:

```shell
coverage run -m unittest recent_projects_test # gather test data
coverage report -m # display coverage figures
```

## Built With

* [Python 2.7](https://docs.python.org/2.7/)
* [GNU Make](https://www.gnu.org/software/make/manual/make.html) - Build scripting
* [mock](http://mock.readthedocs.org/) - Testing library
* [coverage.py](https://coverage.readthedocs.io/) - Code coverage measurement

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

See [CONTRIBUTORS.md](CONTRIBUTORS.md) and [contributors](https://github.com/your/project/contributors) for the list of
contributors.
