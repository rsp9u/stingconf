import os
import sys
import argparse
import json
import yaml
from copy import deepcopy
from .utils import str_to_type, to_upper_snake
from .config import Config


class Parser():
    def __init__(self, description='', definitions=None):
        self._argparser = argparse.ArgumentParser(description=description)
        self._args = None
        self._conf_file = None
        self._env_prefix = None
        self._order = ['env', 'arg', 'file', 'default']
        self._items = []

        if definitions is not None:
            self.conf_file(definitions.get('conf_file', None))
            self.env_prefix(definitions.get('env_prefix', None))
            self.order(*definitions.get('order', ['env', 'arg', 'file', 'default']))
            self._items = []
            for name, value in definitions.get('items', {}).items():
                v = deepcopy(value)
                v['type'] = str_to_type(v.get('type', 'str'))
                v.update(value.get('arg', {}))
                v.update(value.get('env', {}))
                self.add(name, **v)

    def add(self, name, short=None, type=str, default=None,
            no_prefix=False, long_prefix='--', short_prefix='-',
            repeatable=False, delimiter=',',
            help=None, **kwargs):
        item = {
            'name': name,
            'short': short,
            'type': self._type_func(type),
            'default': default,
            'no_prefix': no_prefix,
            'repeatable': repeatable,
            'delimiter': delimiter,
        }
        item.update(kwargs)
        self._items.append(item)

        arg_names = []
        arg_names.append(long_prefix + name)
        if short is not None:
            arg_names.append(short_prefix + short)
        if repeatable:
            nargs = '+'
        else:
            nargs = None
        self._argparser.add_argument(*arg_names, dest=to_upper_snake(name),
                                     type=self._type_func(type), nargs=nargs, help=help)

    def env_prefix(self, prefix):
        self._env_prefix = prefix

    def conf_file(self, path, type='yaml'):
        if path is None:
            return

        with open(path) as f:
            if type == 'yaml':
                self._conf_file = yaml.safe_load(f)
            elif type == 'json':
                self._conf_file = json.load(f)

    def order(self, *orders):
        for o in reversed(orders):
            self._order.remove(o)
            self._order.insert(0, o)

    def parse(self, argv=None):
        config = Config()

        if argv is None:
            self._args = self._argparser.parse_args(sys.argv[1:])
        else:
            self._args = self._argparser.parse_args(argv)

        for item in self._items:
            for o in self._order:
                f = getattr(self, '_get_from_' + o)
                value = f(item)
                if value is None:
                    continue
                try:
                    value = self._cast_value(value, item['type'])
                except ValueError:
                    # TODO: Add warning log
                    continue
                config.add(to_upper_snake(item['name']), value, item)
                break

        return config

    def _type_func(self, type_func):
        def _to_bool(s):
            if isinstance(s, str):
                return s.lower() in ["true", "t", "yes", "1"]
            else:
                return bool(s)
        if type_func.__name__ == 'bool':
            return _to_bool
        else:
            return type_func

    def _cast_value(self, value, type_func):
        if isinstance(value, list):
            return [type_func(elem) for elem in value]
        else:
            return type_func(value)

    def _get_from_env(self, item):
        if self._env_prefix is None or item.get('env', {}).get('no_prefix'):
            env_name = to_upper_snake(item['name'])
        else:
            env_name = to_upper_snake('{0}_{1}'.format(self._env_prefix, item['name']))

        if item.get('env', {}).get('ignorecase'):
            env_value = {k.upper(): v for k, v in os.environ.items()}.get(env_name.upper())
        else:
            env_value = os.environ.get(env_name)

        if isinstance(env_value, str) and item['repeatable']:
            return env_value.split(item['delimiter'])
        else:
            return env_value

    def _get_from_arg(self, item):
        return getattr(self._args, to_upper_snake(item['name']))

    def _get_from_file(self, item):
        if self._conf_file is None:
            return None
        else:
            return self._conf_file.get(item['name'].replace('-', '_'))

    def _get_from_default(self, item):
        return item['default']
