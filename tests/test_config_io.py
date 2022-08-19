import tempfile
import unittest
import shutil
import random
import os
import json
import yaml

from config_io import Config

KEY1 = 'key1'
KEY2 = 'key2'
KEY3 = 'key3'
VALUE1 = 'value1'
VALUE2 = 'value2'
VALUE2_2 = 'value2_2'
VALUE3 = 'value3'
VALUE4 = 'value4'

DEFAULT_STR = 'default'
DEFAULT_SEARCH_PATHS_STR = 'default_search_paths'
EXPAND_STR = 'expand'
EXPAND_SUFFIX_STR = 'expand_suffix'


class TestConfigIO(unittest.TestCase):

    def _random_filename(self, extension):
        return f'{random.randint(0, 10000)}.{extension}'

    def _create_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def _make_str_json(self, dictionary):
        return json.dumps(dictionary)

    def _make_str_yaml(self, dictionary):
        return yaml.dump(dictionary)

    def _write_dictionary_json(self, dictionary, sub_folder):
        self._create_folder(os.path.join(self._temp_folder, sub_folder))
        path = os.path.join(
            self._temp_folder, sub_folder, self._random_filename('json'))
        with open(path, 'w') as f:
            f.write(self._make_str_json(dictionary))
        return path

    def _write_dictionary_yaml(self, dictionary, sub_folder):
        self._create_folder(os.path.join(self._temp_folder, sub_folder))
        path = os.path.join(
            self._temp_folder, sub_folder, self._random_filename('yaml'))
        with open(path, 'w') as f:
            f.write(self._make_str_yaml(dictionary))
        return path

    def _write_dictionary(self, dictionary, format_, sub_folder=''):
        if format_ == 'json':
            return self._write_dictionary_json(dictionary, sub_folder)
        elif format_ == 'yaml':
            return self._write_dictionary_yaml(dictionary, sub_folder)
        else:
            raise ValueError(f'Unknown format {format_}')

    def test_load_from_file(self):
        for format_ in ['json', 'yaml']:
            with self.subTest(format=format_):
                dictionary = {KEY1: VALUE1, KEY2: VALUE2}
                path = self._write_dictionary(dictionary, format_=format_)
                self.assertEqual(Config.load_from_file(path), dictionary)

    def test_load_dictionary(self):
        dictionary = {KEY1: VALUE1, KEY2: VALUE2}
        self.assertEqual(Config(dictionary), dictionary)

    def test_key_assign(self):
        config = Config()
        config[KEY1] = VALUE1
        config[KEY2] = VALUE2
        dictionary = {KEY1: VALUE1, KEY2: VALUE2}
        self.assertEqual(config, dictionary)

    def test_property_assign(self):
        config = Config()
        config.key = 'value'
        dictionary = {'key': 'value'}
        self.assertEqual(config, dictionary)

    def test_missing_property(self):
        config = Config()
        with self.assertRaises(AttributeError):
            config.a.b = 1

    def test_missing_key(self):
        config = Config()
        with self.assertRaises(AttributeError):
            config['a']['b'] = 1

    def test_dump_and_load(self):
        for format_ in ['json', 'yaml']:
            with self.subTest(format=format_):
                dictionary = {KEY1: VALUE1, KEY2: VALUE2}
                path = os.path.join(
                    self._temp_folder, self._random_filename(format_))
                Config(dictionary).dump_to_file(path)
                self.assertEqual(Config.load_from_file(path), dictionary)

    def test_default_in_config(self):
        for format1 in ['json', 'yaml']:
            for format2 in ['json', 'yaml']:
                with self.subTest(format1=format1, format2=format2):
                    dictionary1 = {KEY1: VALUE1, KEY2: VALUE2}
                    path1 = self._write_dictionary(
                        dictionary1, format_=format1)
                    dictionary2 = {KEY2: VALUE2_2,
                                   KEY3: VALUE3,
                                   DEFAULT_STR: path1}
                    path2 = self._write_dictionary(
                        dictionary2, format_=format2)
                    dictionary3 = {KEY1: VALUE1,
                                   KEY2: VALUE2_2,
                                   KEY3: VALUE3,
                                   DEFAULT_STR: path1}
                    self.assertEqual(
                        Config.load_from_file(path2), dictionary3)

    def test_default_in_parameter(self):
        for format1 in ['json', 'yaml']:
            for format2 in ['json', 'yaml']:
                with self.subTest(format1=format1, format2=format2):
                    dictionary1 = {KEY1: VALUE1, KEY2: VALUE2}
                    path1 = self._write_dictionary(
                        dictionary1, format_=format1)
                    dictionary2 = {KEY2: VALUE2_2,
                                   KEY3: VALUE3}
                    path2 = self._write_dictionary(
                        dictionary2, format_=format2)
                    dictionary3 = {KEY1: VALUE1,
                                   KEY2: VALUE2_2,
                                   KEY3: VALUE3}
                    self.assertEqual(Config.load_from_file(
                        path2, default=path1), dictionary3)

    def test_default_search_path_in_config(self):
        for format1 in ['json', 'yaml']:
            for format2 in ['json', 'yaml']:
                with self.subTest(format1=format1, format2=format2):
                    dictionary1 = {KEY1: VALUE1, KEY2: VALUE2}
                    path1 = self._write_dictionary(
                        dictionary1, format_=format1, sub_folder='s')
                    dictionary2 = {
                        KEY2: VALUE2_2,
                        KEY3: VALUE3,
                        DEFAULT_STR: os.path.basename(path1),
                        DEFAULT_SEARCH_PATHS_STR: [os.path.dirname(path1)]}
                    path2 = self._write_dictionary(
                        dictionary2, format_=format2)
                    dictionary3 = {
                        KEY1: VALUE1,
                        KEY2: VALUE2_2,
                        KEY3: VALUE3,
                        DEFAULT_STR: os.path.basename(path1),
                        DEFAULT_SEARCH_PATHS_STR: [os.path.dirname(path1)]}
                    self.assertEqual(
                        Config.load_from_file(path2), dictionary3)

    def test_default_search_path_in_parameter(self):
        for format1 in ['json', 'yaml']:
            for format2 in ['json', 'yaml']:
                with self.subTest(format1=format1, format2=format2):
                    dictionary1 = {KEY1: VALUE1, KEY2: VALUE2}
                    path1 = self._write_dictionary(
                        dictionary1, format_=format1, sub_folder='s')
                    dictionary2 = {
                        KEY2: VALUE2_2,
                        KEY3: VALUE3,
                        DEFAULT_STR: os.path.basename(path1)}
                    path2 = self._write_dictionary(
                        dictionary2, format_=format2)
                    dictionary3 = {
                        KEY1: VALUE1,
                        KEY2: VALUE2_2,
                        KEY3: VALUE3,
                        DEFAULT_STR: os.path.basename(path1)}
                    self.assertEqual(
                        Config.load_from_file(
                            path2,
                            default_search_paths=[os.path.dirname(path1)]),
                        dictionary3)

    def test_expand_disabled(self):
        for format_ in ['json', 'yaml']:
            with self.subTest(format=format_):
                dictionary = {KEY1: [VALUE1, VALUE2]}
                path = self._write_dictionary(dictionary, format_=format_)
                self.assertEqual(Config.load_from_file(path), dictionary)

    def test_expand_in_parameter(self):
        for format_ in ['json', 'yaml']:
            with self.subTest(format=format_):
                dictionary = {KEY1: [VALUE1, VALUE2], KEY1 + '_expand': True}
                path = self._write_dictionary(dictionary, format_=format_)
                self.assertCountEqual(
                    Config.load_from_file(path, expand=True),
                    [{KEY1: VALUE1, KEY1 + '_expand': True},
                     {KEY1: VALUE2, KEY1 + '_expand': True}])

    def test_expand_in_config(self):
        for format_ in ['json', 'yaml']:
            with self.subTest(format=format_):
                dictionary = {
                    KEY1: [VALUE1, VALUE2],
                    KEY1 + '_expand': True,
                    EXPAND_STR: True}
                path = self._write_dictionary(dictionary, format_=format_)
                self.assertCountEqual(
                    Config.load_from_file(path),
                    [{KEY1: VALUE1, KEY1 + '_expand': True, EXPAND_STR: True},
                     {KEY1: VALUE2, KEY1 + '_expand': True, EXPAND_STR: True}])

    def test_expand_complicated_in_parameter(self):
        for format_ in ['json', 'yaml']:
            with self.subTest(format=format_):
                dictionary = {
                    KEY1: [VALUE1, VALUE2],
                    KEY1 + '_expand': True,
                    KEY2: {KEY3: [VALUE3, VALUE4],
                           KEY3 + '_expand': True}}
                path = self._write_dictionary(dictionary, format_=format_)
                self.assertCountEqual(
                    Config.load_from_file(path, expand=True),
                    [{KEY1: VALUE1,
                      KEY1 + '_expand': True,
                      KEY2: {KEY3: VALUE3, KEY3 + '_expand': True}},
                     {KEY1: VALUE2,
                      KEY1 + '_expand': True,
                      KEY2: {KEY3: VALUE3, KEY3 + '_expand': True}},
                     {KEY1: VALUE1,
                      KEY1 + '_expand': True,
                      KEY2: {KEY3: VALUE4, KEY3 + '_expand': True}},
                     {KEY1: VALUE2,
                      KEY1 + '_expand': True,
                      KEY2: {KEY3: VALUE4, KEY3 + '_expand': True}}])

    def test_expand_method(self):
        dictionary = {
            KEY1: [VALUE1, VALUE2],
            KEY1 + '_expand': True,
            KEY2: {KEY3: [VALUE3, VALUE4],
                   KEY3 + '_expand': True}}
        config = Config(dictionary)
        self.assertCountEqual(
            config.expand(),
            [{KEY1: VALUE1,
              KEY1 + '_expand': True,
              KEY2: {KEY3: VALUE3, KEY3 + '_expand': True}},
             {KEY1: VALUE2,
              KEY1 + '_expand': True,
              KEY2: {KEY3: VALUE3, KEY3 + '_expand': True}},
             {KEY1: VALUE1,
              KEY1 + '_expand': True,
              KEY2: {KEY3: VALUE4, KEY3 + '_expand': True}},
             {KEY1: VALUE2,
              KEY1 + '_expand': True,
              KEY2: {KEY3: VALUE4, KEY3 + '_expand': True}}])

    def test_expand_method_in_sub_dict(self):
        dictionary = {
            KEY1: [VALUE1, VALUE2],
            KEY1 + '_expand': True,
            KEY2: {KEY3: [VALUE3, VALUE4],
                   KEY3 + '_expand': True}}
        config = Config(dictionary)
        self.assertCountEqual(
            config[KEY2].expand(),
            [{KEY3: VALUE3, KEY3 + '_expand': True},
             {KEY3: VALUE4, KEY3 + '_expand': True}])

    def setUp(self):
        self._temp_folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._temp_folder)


if __name__ == '__main__':
    unittest.main()
