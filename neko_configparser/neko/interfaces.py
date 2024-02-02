from ..modules.toml_parser import TomlConfig
from ..modules.writer import WriteTomlConfig
from typing import Dict, Any


class ConfigParserInterface:
    @staticmethod
    def parse_config(config_path: str = 'config.neko.toml') -> TomlConfig:
        """
        Get toml configuration in our handy representation
        :param config_path:
        :return:
        """
        return TomlConfig(config_path)

    @staticmethod
    def ensure_config(
            partition: str,
            module_config: Dict[str, Any],
            config_path: str = 'config.neko.toml'
    ) -> None:
        """
        Validates your module config and adds values if needed
        :param partition: Your module name or any name under which you want to see this
        key-value configuration table
        :param module_config: Dictionary of default config keys and values, so they will
        be added and verified in config
        :param config_path: Path of config, if you want to use custom
        """
        WriteTomlConfig(config_path).ensure({partition: module_config})
