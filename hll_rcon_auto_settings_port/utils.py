import json
from pprint import pprint
from typing import Any

from loguru import logger

from hll_rcon_auto_settings_port import constants


def validate_settings(payload: dict[str, Any]) -> bool:
    # check top level keys
    # check nested keys
    # check validity of conditions

    for key, value in payload.items():
        if key not in constants.VALID_TOP_LEVEL_KEYS:
            raise ValueError(key)

        print(f"{key=}")
        logger.debug(f"{key=}")
        if isinstance(payload[key], dict):
            for sub_key, sub_value in payload[key].items():
                print(f"{sub_key=}")
                logger.debug(f"{sub_key=}")

    return True


def replace_args(
    arg_mapping: dict[str, dict[str, str]],
    deprecated_arg_mapping: dict[str, set[str]],
    cmd_name: str,
    old_args: dict[str, Any],
) -> dict[str, Any] | None:
    new_mapping: dict[str, Any] = {}
    old_format = arg_mapping.get(cmd_name)

    print(f"{cmd_name=} {old_format=} {old_args=}")
    logger.debug(f"{cmd_name=} {old_format=} {old_args=}")
    logger.info(f"{deprecated_arg_mapping=}")
    if old_format:
        for k, v in old_args.items():
            arg = old_format.get(k)
            deprecated_arg = deprecated_arg_mapping.get(cmd_name)
            logger.info(f"{k=}")
            if arg:
                new_mapping[arg] = v
                print(f"{k=} {v=} {arg=}")
                logger.debug(f"{k=} {v=} {arg=}")
            elif deprecated_arg:
                logger.info(f"{k} in {deprecated_arg_mapping} skipping")
                continue
            else:
                new_mapping[k] = v

        print(f"{new_mapping=}")
        logger.debug(f"{new_mapping=}")
    elif cmd_name == "set_votekick_threshold":
        pairs = old_args["threshold_pairs"].split(",")
        pair_list: list[tuple[int, int]] = []
        for p1, p2 in zip(pairs[0::2], pairs[1::2]):
            pair_list.append((int(p1), int(p2)))
        logger.info(f"set_votekick_threshold {pairs=} {pair_list=}")
        new_mapping["threshold_pairs"] = pair_list
    else:
        new_mapping = old_args
    return new_mapping


def replace_command(cmd_mapping: dict[str, str], old_name: str) -> str | None:
    new_cmd = cmd_mapping.get(old_name)
    logger.debug(f"{old_name=} {new_cmd=}")

    if not new_cmd and old_name == "do_set_map_whitelist":
        logger.debug(f"{cmd_mapping=}")

    return new_cmd


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
    logger.debug(f"{from_version=} {type(from_version)=}")
    logger.debug(f"{to_version=} {type(to_version)=}")
    from_version_lookup = constants.Versions(from_version)
    to_version_lookup = constants.Versions(to_version)

    cmd_mapping = constants.UP_VERSION_TO_CMD_MAPPING[from_version_lookup]
    cmd_mapping = cmd_mapping[to_version_lookup]
    print(f"{cmd_mapping=}")
    logger.debug(f"{cmd_mapping=}")

    arg_mapping = constants.UP_VERSION_TO_ARG_MAPPING[from_version_lookup][
        to_version_lookup
    ]

    deprecated_arg_mapping = constants.UP_VERSION_TO_REMOVED_ARG_MAPPING[
        from_version_lookup
    ][to_version_lookup]

    updated_auto_settings = {
        constants.ALWAYS_APPLY_DEFAULTS: False,
        constants.DEFAULTS: {},
        constants.RULES: [],
        constants.AVAILABLE_COMMANDS: {},
        constants.AVAILABLE_CONDITIONS: {},
        constants.AVAILABLE_SETTINGS: {
            "always_apply_defaults": "Whether or not to apply the settings defined in the default section in each iteration. Allowed values: true / false",
            "can_invoke_multiple_rules": "Whether or not to allow the invocation of multiple rules e.g. don't stop after the first fulfilled rule. Allowed values: true / false",
        },
    }

    # top level keys
    for key, value in payload.items():
        logger.debug(f"{key=} {value=}")
        if key in (constants.AVAILABLE_COMMANDS, constants.AVAILABLE_CONDITIONS):
            continue
        elif key == constants.RULES:
            for obj in payload[key]:
                new_commands = {}
                conditions = obj["conditions"]

                for sub_key, sub_value in obj["commands"].items():
                    new_cmd = (
                        replace_command(cmd_mapping=cmd_mapping, old_name=sub_key)
                        or sub_key
                    )
                    new_args = replace_args(
                        arg_mapping=arg_mapping,
                        deprecated_arg_mapping=deprecated_arg_mapping,
                        cmd_name=sub_key,
                        old_args=sub_value,
                    )
                    print(f"{key=} {sub_key=} {sub_value=} {new_cmd=} {new_args=}")
                    logger.debug(
                        f"{key=} {sub_key=} {sub_value=} {new_cmd=} {new_args=}"
                    )
                    # updated_auto_settings[key][new_cmd] = new_args
                    new_commands[new_cmd] = new_args
                updated_auto_settings[key].append(
                    {"commands": new_commands, "conditions": conditions}
                )
        elif isinstance(payload[key], dict):
            for sub_key, sub_value in payload[key].items():
                new_cmd = (
                    replace_command(cmd_mapping=cmd_mapping, old_name=sub_key)
                    or sub_key
                )
                new_args = replace_args(
                    arg_mapping=arg_mapping,
                    deprecated_arg_mapping=deprecated_arg_mapping,
                    cmd_name=sub_key,
                    old_args=sub_value,
                )
                print(f"{key=} {sub_key=} {sub_value=} {new_cmd=} {new_args=}")
                logger.debug(f"{key=} {sub_key=} {sub_value=} {new_cmd=} {new_args=}")
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
