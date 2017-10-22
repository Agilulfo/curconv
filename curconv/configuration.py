import os

from yaml import load


class ConfigurationFileLoader:
    def __init__(self, file=None, default_paths=None):
        if file:
            self.configuration_file = file
        elif default_paths:
            self.configuration_file = self._get_file_from_default(
                default_paths)
        else:
            self.configuration_file = None

    def _get_file_from_default(self, default_paths):
        for path in default_paths:
            if os.path.exists(path):
                return open(path, 'r')


class YAMLConfigurationFileLoader(ConfigurationFileLoader):
    def load_from_file(self):
        return load(self.configuration_file)
