import os
import sys
import argparse
import json
import yaml


class Parser():
    def __init__(self, description=''):
        self._argparser = argparse.ArgumentParser(description=description)
        self._args = None
        self._conf_file = None
        self._items = []
        self._env_prefix = None
        self._order = ['env', 'arg', 'file', 'default']

    def add(self, name, short=None, type=str, default=None):
        item = {
            'name': name,
            'uname': name.upper().replace('-', '_'),
            'short': short,
            'type': type,
            'default': default,
        }
        self._items.append(item)
        self._argparser.add_argument('--' + name, dest=item['uname'], metavar=short, type=type)

    def env_prefix(self, prefix):
        self._env_prefix = prefix

    def conf_file(self, path, type='yaml'):
        with open(path) as f:
            if type == 'yaml':
                self._conf_file = yaml.load(f)
            elif type == 'json':
                self._conf_file = json.load(f)

    def order(self, *orders):
        for o in reversed(orders):
            self._order.remove(o)
            self._order.insert(0, o)

    def parse(self):
        self._args = self._argparser.parse_args()
        for item in self._items:
            for o in self._order:
                print('part', o)
                f = getattr(self, '_get_from_' + o)
                value = f(item)
                print('ret: ', value)
                if value is not None:
                    setattr(self, item['uname'], value)
                    break

    def _get_from_env(self, item):
        env_name = item['uname']
        if self._env_prefix is not None:
            env_name = '{0}_{1}'.format(self._env_prefix, env_name)
        return os.environ.get(env_name)

    def _get_from_arg(self, item):
        return getattr(self._args, item['uname'])

    def _get_from_file(self, item):
        if self._conf_file is None:
            return None
        else:
            return self._conf_file.get(item['name'].replace('-', '_'))

    def _get_from_default(self, item):
        return item['default']
