# config_io
![Tests](https://github.com/fjxmlzn/config_io/workflows/test/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/fjxmlzn/config_io/badge.svg?t=nguDCe)](https://coveralls.io/github/fjxmlzn/config_io) [![PyPI version](https://badge.fury.io/py/config_io.svg)](https://badge.fury.io/py/config_io)

`config_io` is a Python package for advanced config reading/parsing/writing. `config_io` currently supports `json` and `yaml` formats.

## Installing
You can install `config_io` via `pip`:

```sh
pip install config_io
```

`config_io ` runs on Python 3, and every build is tested towards Python 3.6, 3.7, 3.8, 3.9, 3.10 on ubuntu, macOS, and windows.

## Usage
First, load the library by

```Python
>>> from config_io import Config
```
`Config` is a class for storing configs. `Config` is similar Python dictionary but with powerful reading/writing/parsing functions. 

### Config reading
`config_io` supports reading configs from `yaml` and `json` files, as well as from python dictionaries or through keyword arguments. 

Suppose we have a `json` file `config.json` with content

```json
{"key": "value"}
```
and a `yaml` file `config.yaml` with content

```yaml
key: value
```
Below are five equivalent ways to create the same `config` object:

```Python
>>> config = Config.load_from_file('config.json')
```

```Python
>>> config = Config.load_from_file('config.yaml')
```

```Python
>>> config = Config({'key': 'value'})
```

```Python
>>> config = Config(key='value')
```

```Python
>>> config = Config()
>>> config.key = 'value'
```

The `config` object is

```Python
>>> config
{'key': 'value'}
>>> type(config)
<class 'config_io.config.Config'>
```

### Config writing
Config objects (of type `config_io.config.Config`) can be dumped to `json` and `yaml` files easily by

```Python
>>> config.dump_to_file('config.json')
```
or


```Python
>>> config.dump_to_file('config.yaml')
```

### Default config

In many use cases, we may want to specify a default config (e.g., default parameters for a program). Other configs (e.g., user-specified parameters) can modify on top of it. `config_io` provides an easy way to do this. 

Suppose we have `default.yaml` with content

```yaml
k1: v1
k2: v2
k3: v3
``` 
Now, suppose that we want to specify a config that adds a new key `k4`, and changes the value of `k3` to `new_v3`. We can simply write `config.yaml` with content

```yaml
k4: v4
k3: new_v3
default: default.yaml
```

`config_io` will automatically load the config file specified by `default` as the default parameters:

```Python
>>> Config.load_from_file('config.yaml')
{'k1': 'v1', 'k2': 'v2', 'k3': 'new_v3', 'k4': 'v4', 'default': 'default.yaml'}
```

##### Advanced options
* Instead of specifying `default: default.yaml` in `config.yaml`, an alternative way is to specify it when loading the config: `Config.load_from_file('config.yaml', default='default.yaml')`.
* Default configs can be chained in any order. For example, `config1.yaml` can set `config2.yaml` as the default config, and `config2.yaml` can set another `config3.yaml` as the default config.


### Config expansion
In many scenarios, we may want to interact with a set of configs that are created by enumerating all possible combinations of values. `config_io` provides an easy way to do this. 

For example, assume that `config.json` has the content:

```json
{"k1": [1, 2],
 "k2": [3, 4],
 "k1_expand": true,
 "k2_expand": true}
```
Loading it would give a list of 4 configs

```Python
>>> Config.load_from_file('config.json', expand=True)
[{'k1': 1, 'k2': 3, 'k1_expand': True, 'k2_expand': True},
 {'k1': 1, 'k2': 4, 'k1_expand': True, 'k2_expand': True},
 {'k1': 2, 'k2': 3, 'k1_expand': True, 'k2_expand': True},
 {'k1': 2, 'k2': 4, 'k1_expand': True, 'k2_expand': True}]
```
Basically, for the keys such that `{KEY_NAME}_expand` is set to true, `config_io` treats their values as a list of candidate values, and will enumerate all possible combinations of them to generate the list of configs. Note that this feature is turned on only when `expand` is set to true either through the parameter of `load_from_file` or inside the config file.

Expansion can also happen after the config is loaded:

```Python
>>> config = Config({'k1': {'k2': [1, 2], 'k2_expand': True}})
>>> config.expand()
[{'k1': {'k2': 1, 'k2_expand': True}}, {'k1': {'k2': 2, 'k2_expand': True}}]
```
or be applied only for a sub-tree of the config:

```Python
>>> config.k1.expand()
[{'k2': 1, 'k2_expand': True}, {'k2': 2, 'k2_expand': True}]
``` 


##### Advanced options
The keys to expand can be on different levels of the config tree. For example, if `config.json` is

```json
{"k1": [1, 2],
 "k1_expand": true,
 "k2": {"k3": [3, 4],
        "k3_expand": true}}
```
`Config.load_from_file('config.json', expand=True)` would give

```Python
[{'k1': 1, 'k1_expand': True, 'k2': {'k3': 3, 'k3_expand': True}},
 {'k1': 1, 'k1_expand': True, 'k2': {'k3': 4, 'k3_expand': True}},
 {'k1': 2, 'k1_expand': True, 'k2': {'k3': 3, 'k3_expand': True}},
 {'k1': 2, 'k1_expand': True, 'k2': {'k3': 4, 'k3_expand': True}}]
```

### More on config objects
`config_io.config.Config` is extended from the powerful [addict library](https://github.com/mewwts/addict), which supports retrieving config values using either attributes or the standard dictionary item syntax:

```Python
>>> config = Config(a=1,b={'c':2})
>>> config.a
1
>>> config.b.c
2
>>> config['b'].c
2
```
For more advanced options, please refer to [addict doc](https://github.com/mewwts/addict).


## Contributing
If you find bugs/problems or want to add more features to this library, feel free to submit issues or make pull requests.