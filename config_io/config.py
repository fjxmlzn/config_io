import os
from addict import Dict
import itertools
import copy

from .io import dump as _dump
from .io import load as _load


class Config(Dict):
    def dump_to_file(self, path):
        _dump(path, self.to_dict())

    @classmethod
    def load_from_file(cls, path, default=None, default_search_paths=None,
                       expand=False, expand_suffix='_expand'):
        current_config = _load(path)
        if 'default' in current_config:
            default = current_config['default']
        if 'default_search_paths' in current_config:
            default_search_paths = copy.deepcopy(
                current_config['default_search_paths'])
        elif default_search_paths is None:
            default_search_paths = []
        default_search_paths.insert(0, os.path.dirname(path))
        if 'expand' in current_config:
            expand = current_config['expand']
        if 'expand_suffix' in current_config:
            expand_suffix = current_config['expand_suffix']

        if default is not None:
            default_config = None
            for path in default_search_paths:
                default_path = os.path.join(path, default)
                if os.path.exists(default_path):
                    default_config = cls.load_from_file(default_path)
                    break
            if default_config is None:
                raise ValueError(
                    f"File {default} not found in {default_search_paths}")
        else:
            default_config = {}
        default_config.update(current_config)
        default_config = cls(default_config)

        if expand:
            default_configs = default_config.expand(
                expand_suffix=expand_suffix)
        else:
            default_configs = default_config

        return default_configs

    def expand(self, expand_suffix='_expand'):
        configs = self._expand(self, expand_suffix)
        configs = [self.__class__(v) for v in configs]
        return configs

    @classmethod
    def _expand(cls, item, expand_suffix):
        if isinstance(item, cls):
            keys = list(item.keys())
            values = list(item.values())
            for i in range(len(keys)):
                expand_key = keys[i] + expand_suffix
                if expand_key in item and item[expand_key]:
                    if isinstance(values[i], list):
                        expanded = [cls._expand(v, expand_suffix)
                                    for v in values[i]]
                        values[i] = [v for sub in expanded for v in sub]
                    else:
                        raise ValueError(
                            f'The value of {keys[i]} should be a list in order'
                            f' to be expanded')
                else:
                    values[i] = cls._expand(values[i], expand_suffix)
            new_items = [dict(zip(keys, pairs))
                         for pairs in itertools.product(*values)]
            return new_items
        elif isinstance(item, (list, tuple)):
            values = [cls._expand(v, expand_suffix) for v in item]
            new_items = [type(item)(pairs)
                         for pairs in itertools.product(*values)]
            return new_items
        else:
            return [item]
