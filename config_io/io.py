import json
import yaml
import os


def _load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def _dump_json(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=4)


def _load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def _dump_yaml(path, obj):
    with open(path, 'w') as f:
        yaml.dump(obj, f)


LOADERS = {
    '.json': _load_json,
    '.yaml': _load_yaml,
    '.yml': _load_yaml
}

DUMPERS = {
    '.json': _dump_json,
    '.yaml': _dump_yaml,
    '.yml': _dump_yaml
}


def load(path):
    extension = os.path.splitext(path)[1].lower()
    if extension in LOADERS:
        return LOADERS[extension](path)
    else:
        raise TypeError(f'Unsupported extension {extension}')


def dump(path, obj):
    extension = os.path.splitext(path)[1].lower()
    if extension in DUMPERS:
        return DUMPERS[extension](path, obj)
    else:
        raise TypeError(f'Unsupported extension {extension}')
