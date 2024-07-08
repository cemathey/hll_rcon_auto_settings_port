import json
from pprint import pprint

from hll_rcon_auto_settings_port.constants import Versions
from hll_rcon_auto_settings_port.utils import upgrade, validate_settings

if __name__ == "__main__":
    with open("example.json") as fp:
        data = json.load(fp)
        # pprint(data)

        # validate_settings(data)
        upgrade(
            from_version=Versions.v9_9_1.value,
            to_version=Versions.v10_0_0.value,
            payload=data,
        )
