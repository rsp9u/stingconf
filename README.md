# StingConf

[![Build Status](https://travis-ci.org/rsp9u/stingconf.svg?branch=master)](https://travis-ci.org/rsp9u/stingconf)
[![codecov](https://codecov.io/gh/rsp9u/stingconf/branch/master/graph/badge.svg)](https://codecov.io/gh/rsp9u/stingconf)

This is a configuration library through envrionment variables, command line arguments,
configuration file and default value.

## Installation

```
pip install stingconf
```

## Examples

### define args with functions

* example.py

```python
import stingconf

parser = stingconf.Parser('Example module')
parser.env_prefix('SC')
parser.conf_file('config.yml')
parser.add('conf-a', short='a', type=int, default=0)
parser.add('conf-b', short='b', type=float, default=0.0)
parser.add('conf-c', short='c', type=str, default='conf-c')
parser.add('conf-d', short='d', default='conf-d', help='4th config')
config = parser.parse()

print('CONF_A:', config.CONF_A)
print('CONF_B:', config.CONF_B)
print('CONF_C:', config.CONF_C)
print('CONF_D:', config.CONF_D)
```

* config.yml

```yaml
conf_a: 100
conf_b: 1.0
conf_c: file-conf-c
```

* run example

```bash
$ export SC_CONF_A=300
$ python example.py --conf-a 200 -b 20.0
CONF_A: 300
CONF_B: 20.0
CONF_C: file-conf-c
CONF_D: conf-d
```

### define args with object

* example.py

```python
import stingconf

definitions = {
    'env_prefix': 'SC',
    'conf_file': 'config.yml',
    'items': {
        'conf-a': {
            'arg': {'short': 'a'},
            'type': 'int',
            'default': 0,
        },
        'conf-b': {
            'arg': {'short': 'b'},
            'type': 'float',
            'default': 0.0,
        },
        'conf-c': {
            'arg': {'short': 'c'},
            'type': 'str',
            'default': 'conf-c',
        },
        'conf-d': {
            'arg': {'short': 'd'},
            'default': 'conf-d',
            'help': '4th config',
        },
    },
}
parser = stingconf.Parser('Example module', definitions)
config = parser.parse()
```

### define args with file

* definitions.yml

```yaml
env_prefix: SC
conf_file: config.yml
order:
  - env
  - arg
  - file
  - default
items:
  user:
    help: 'login user'
    arg:
      short: u
  password:
    help: 'login passowrd'
    arg:
      short: p
  enable:
    type: bool
    default: false
    help: 'enable something'
    arg:
      long_prefix: '-'
  http-proxy:
    env:
      no_prefix: true
      ignorecase: true
  https-proxy:
    env:
      no_prefix: true
      ignorecase: true
```

* example.py

```python
import yaml
import stingconf

with open('definitions.yml') as f:
	definitions = yaml.safe_load(f)
parser = stingconf.Parser('Example module', definitions)
config = parser.parse()
```

## Naming convention

### Environment

Environment variables' name should be set `LIKE_THIS`.

If desired, you can set the prefix of name by `Parser.env_prefix()`.

### Argument

Arguments' name should be set `like-this`.

If desired, you can use short version argument by passing `short` to `Parser.add()`

### File

Variables' name in the configuration file should be set `like_this`

Currently, the supported formats are json and yaml, and the content must be
non-nested dictionary.
