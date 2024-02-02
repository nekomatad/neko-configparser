import toml


class TomlConfig(dict):
    def __init__(self, config_path: str = 'config.neko.toml', _config: dict = None):
        try:
            if _config is None:
                super().__init__(**toml.load(config_path))
            else:
                super().__init__(**_config)

        except FileNotFoundError:
            super().__init__()

    def __getattr__(self, item):
        if type(self.get(item)) is not dict:
            return self.get(item)
        else:
            return TomlConfig(_config=self.get(item))
