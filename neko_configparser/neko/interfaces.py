import dataclasses
from ..modules.toml_parser import TomlConfig
from ..modules.writer import WriteTomlConfig
from typing import Dict, Any


@dataclasses.dataclass
class __HiddenStorage:
    nekomata_folder: str = ''


_storage = __HiddenStorage()


class ConfigParserInterface:
    @staticmethod
    def parse_config(config_path: str = None) -> TomlConfig:
        """
        Get toml configuration in our handy representation
        :param config_path:
        :return:
        """
        return TomlConfig(config_path if config_path
                          else _storage.nekomata_folder + '/config.neko.toml')

    @staticmethod
    def ensure_config(
            partition: str,
            module_config: Dict[str, Any],
            config_path: str = None
    ) -> None:
        """
        Validates your module config and adds values if needed
        :param partition: Your module name or any name under which you want to see this
        key-value configuration table
        :param module_config: Dictionary of default config keys and values, so they will
        be added and verified in config
        :param config_path: Path of config, if you want to use custom
        """
        WriteTomlConfig(
            config_path if config_path
            else _storage.nekomata_folder + '/config.neko.toml'
        ).ensure({partition: module_config})

    @staticmethod
    def get_nekomata_folder():
        return _storage.nekomata_folder


__all__ = [ConfigParserInterface]
