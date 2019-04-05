# StingConf

This is a configuration library through envrionment variables, command line arguments,
configuration file and default value.

## Installation

```
pip install git+https://github.com/rsp9u/stingconf.git
```

## Getting started

* example.py

```python
import stingconf

parser = stingconf.Parser()
parser.env_prefix('SC')
parser.conf_file('config.yml')
parser.add('conf-a', short='a', type=int, default=0)
parser.add('conf-b', short='b', type=float, default=0.0)
parser.add('conf-c', short='c', type=str, default='conf-c')
parser.add('conf-d', short='d', default='conf-d', help='4th config')
parser.parse()

print('CONF_A:', parser.CONF_A)
print('CONF_B:', parser.CONF_B)
print('CONF_C:', parser.CONF_C)
print('CONF_D:', parser.CONF_D)
```

* config.yml

```yaml
conf_a: 100
conf_b: 1.0
conf_c: file-conf-c
```

* run example

```
$ export SC_CONF_A=300
$ python example.py --conf-a 200 -b 20.0
CONF_A: 300
CONF_B: 20.0
CONF_C: file-conf-c
CONF_D: conf-d
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

Currently, the supported formats are json and yaml, and the file contains content
must be non-nested dictionary.
