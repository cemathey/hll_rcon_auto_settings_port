import json
from pprint import pprint
from typing import Any

from hll_rcon_auto_settings_port import constants


def validate_settings(payload: dict[str, Any]) -> bool:
    # check top level keys
    # check nested keys
    # check validity of conditions

    for key, value in payload.items():
        if key not in constants.VALID_TOP_LEVEL_KEYS:
            raise ValueError(key)

        print(f"{key=}")
        if isinstance(payload[key], dict):
            for sub_key, sub_value in payload[key].items():
                print(f"{sub_key=}")

    return True


def replace_args(
    arg_mapping: dict[str, dict[str, str]], cmd_name: str, old_args: dict[str, Any]
) -> dict[str, Any] | None:
    new_mapping: dict[str, Any] = {}
    old_format = arg_mapping.get(cmd_name)
    print(f"{cmd_name=} {old_format=} {old_args=}")
    if old_format:
        for k, v in old_args.items():
            arg = old_format.get(k)
            if arg:
                new_mapping[arg] = v
                print(f"{k=} {v=} {arg=}")
            else:
                new_mapping[k] = v

        print(f"{new_mapping=}")
    else:
        new_mapping = old_args
    return new_mapping


def replace_command(cmd_mapping: dict[str, str], old_name: str) -> str | None:
    return cmd_mapping.get(old_name)


def upgrade(
    from_version: str,
    to_version: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    # try to validate it
    # update defaults
    # loop over rules
    # loop over commands for rules
    # update command names
    # update parameter names
    # updat _available commands

    print(f"{from_version=} {type(from_version)=}")
    print(f"{to_version=} {type(to_version)=}")
    from_version_lookup = constants.Versions(from_version)
    to_version_lookup = constants.Versions(to_version)

    cmd_mapping = constants.UP_VERSION_TO_CMD_MAPPING[from_version_lookup]
    print(f"{cmd_mapping=}")
    cmd_mapping = cmd_mapping[to_version_lookup]
    print(f"{cmd_mapping=}")

    arg_mapping = constants.UP_VERSION_TO_ARG_MAPPING[from_version_lookup][
        to_version_lookup
    ]

    updated_auto_settings = {
        constants.ALWAYS_APPLY_DEFAULTS: False,
        constants.DEFAULTS: {},
        constants.RULES: [],
        constants.AVAILABLE_COMMANDS: {},
        constants.AVAILABLE_CONDITIONS: {},
    }

    # top level keys
    for key, value in payload.items():
        if key in (constants.AVAILABLE_COMMANDS, constants.AVAILABLE_CONDITIONS):
            continue
        elif isinstance(payload[key], dict):
            for sub_key, sub_value in payload[key].items():
                new_cmd = (
                    replace_command(cmd_mapping=cmd_mapping, old_name=sub_key)
                    or sub_key
                )
                new_args = replace_args(
                    arg_mapping=arg_mapping, cmd_name=sub_key, old_args=sub_value
                )
                print(f"{key=} {sub_key=} {sub_value=} {new_cmd=} {new_args=}")
                updated_auto_settings[key][new_cmd] = new_args
                # if key == constants.DEFAULTS:
                #     new_cmd = (
                #         replace_command(cmd_mapping=cmd_mapping, old_name=sub_key)
                #         or sub_key
                #     )
                #     new_args = replace_args(
                #         arg_mapping=arg_mapping, cmd_name=sub_key, old_args=sub_value
                #     )
                #     print(f"{key=} {sub_key=} {sub_value=} {new_cmd=} {new_args=}")
                #     updated_auto_settings[key][new_cmd] = new_args
                # elif key == constants.RULES:
                #     pass
                # elif key == constants.AVAILABLE_COMMANDS:
                #     pass
                # elif key == constants.AVAILABLE_CONDITIONS:
                #     pass
        else:
            updated_auto_settings[key] = value

    print(f"updated_auto_settings=")
    print(f"{json.dumps(updated_auto_settings)}")
    # pprint(updated_auto_settings)

    return updated_auto_settings


def downgrade(
    from_version: str, to_version: str, payload: dict[str, Any]
) -> dict[str, Any]:
    return upgrade(from_version=to_version, to_version=from_version, payload=payload)
