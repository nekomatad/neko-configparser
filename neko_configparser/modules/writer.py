import toml
from typing import Dict, Any


def _update_dicts(dict1, dict2):
    """
    Ensures that dict1 exists in dict2 or merges them in right way
    """
    for key in dict1:
        if key not in dict2 and not isinstance(dict1[key], WriteTomlConfig):
            dict2[key] = dict1[key]
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            _update_dicts(dict1[key], dict2[key])


class WriteTomlConfig(dict):
    def __init__(self, filename: str = 'config.neko.toml'):
        self.__filename = filename
        self.__parent = None
        super().__init__()
        self.__load_from_file(filename)

    @classmethod
    def __create_subsidiary(cls, data, parent):
        d = cls(None)  # type: ignore
        d.__parent = parent

        for key, value in data.items():
            if isinstance(value, dict):
                d[key] = cls.__create_subsidiary(value, parent=parent)

        return d

    def __getitem__(self, key):
        val = super().__getitem__(key)
        return val

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = type(self).__create_subsidiary(value, parent=self)
        super().__setitem__(key, value)
        self.__propagate_write()

    def __delitem__(self, key):
        super().__delitem__(key)
        self.__propagate_write()

    def __propagate_write(self):
        if self.__parent:
            self.__parent.__propagate_write()
        else:
            self.__write()

    def to_dict(self):
        standard_dict = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                standard_dict[key] = value.to_dict()
            else:
                standard_dict[key] = value
        return standard_dict

    def __write(self):
        with open(self.__filename, 'w') as f:
            toml.dump(self.to_dict(), f)

    def __load_from_file(self, filename=None):
        if not filename:
            return
        try:
            data = toml.load(filename)
            for key, value in data.items():
                self[key] = value
        except FileNotFoundError:
            open(filename, 'w+').close()

    def ensure(self, data: Dict[str, Any]):
        _update_dicts(data, self)
        self.__propagate_write()
