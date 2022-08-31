# Page-loader
Page-loader is a Python library that downloads html page and resources from the links, which this page contains.

____

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Dddarknight/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/Dddarknight/python-project-lvl3/actions)

[![Python CI](https://github.com/Dddarknight/python-project-lvl3/actions/workflows/pyci.yml/badge.svg)](https://github.com/Dddarknight/python-project-lvl3/actions)

### CodeClimate:
<a href="https://codeclimate.com/github/Dddarknight/python-project-lvl3/maintainability"><img src="https://api.codeclimate.com/v1/badges/7ba6dc8f87fb8431d54f/maintainability" /></a>

<a href="https://codeclimate.com/github/Dddarknight/python-project-lvl3/test_coverage"><img src="https://api.codeclimate.com/v1/badges/7ba6dc8f87fb8431d54f/test_coverage" /></a>

## Links
This project was built using these tools:
| Tool | Description |
|----------|---------|
| [poetry](https://python-poetry.org/) |  "Python dependency management and packaging made easy" |
| [Py.Test](https://pytest.org) | "A mature full-featured Python testing tool" |

## Description
Page_loader is a CLI utility.
The html page is downloaded to the html file, path to which has to be provided by the user. Otherwise the file is created in the current directory.
Resources from this page, which are availible via links (tags 'img', 'script', 'link'), are downloaded in a separate directory. The path of this directory is similar to the html file path.

## Installation for contributors
```
$ git clone git@github.com:Dddarknight/python-project-lvl3.git
$ cd python-project-lvl3
$ pip install poetry
$ make install
$ make build
```

## Usage
```
$ page_loader -o `output_path` `url_to_download`
$ page_loader `url_to_download`

```

### Asciinema record:
[![asciinema](https://asciinema.org/a/gvquNzFgv3CcixRW6xCm7FlXz.svg)](https://asciinema.org/a/gvquNzFgv3CcixRW6xCm7FlXz)

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
