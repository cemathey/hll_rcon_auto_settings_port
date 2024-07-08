from enum import Enum

ALWAYS_APPLY_DEFAULTS = "always_apply_defaults"
DEFAULTS = "defaults"
RULES = "rules"
AVAILABLE_COMMANDS = "_available_commands"
AVAILABLE_CONDITIONS = "_available_conditions"


class Versions(Enum):
    v9_9_1 = "v9.9.1"
    v10_0_0 = "v10.0.0"


# VERSIONS = ()

VALID_TOP_LEVEL_KEYS = (
    ALWAYS_APPLY_DEFAULTS,
    DEFAULTS,
    RULES,
    AVAILABLE_COMMANDS,
    AVAILABLE_CONDITIONS,
)

VALID_RULES_KEYS = ("commands", "conditions")

V9_9_1_TO_V_10_0_0_CMD_MAPPING = {
    "async_upload_vips": "upload_vips",
    "async_upload_vips_result": "upload_vips_result",
    "do_add_admin": "add_admin",
    "do_add_map_to_rotation": "add_map_to_rotation",
    "do_add_map_to_whitelist": "add_map_to_votemap_whitelist",
    "do_add_maps_to_rotation": "add_maps_to_rotation",
    "do_add_maps_to_whitelist": "add_maps_to_votemap_whitelist",
    "do_add_vip": "add_vip",
    "do_ban_profanities": "ban_profanities",
    "do_reconnect_gameserver": "reconnect_gameserver",
    "do_kick": "kick",
    "do_message_player": "message_player",
    "do_perma_ban": "perma_ban",
    "do_punish": "punish",
    "do_reconnect_gameserver": "reconnect_gameserver",
    "do_remove_admin": "remove_admin",
    "do_remove_all_vips": "do_remove_all_vips",
    "do_remove_map_from_rotation": "remove_map_from_rotation",
    "do_remove_map_from_whitelist": "remove_map_from_votemap_whitelist",
    "do_remove_maps_from_rotation": "remove_maps_from_rotation",
    "do_remove_maps_from_whitelist": "remove_maps_from_votemap_whitelist",
    "do_remove_perma_ban": "remove_perma_ban",
    "do_remove_temp_ban": "remove_temp_ban",
    "do_remove_vip": "remove_vip",
    "do_reset_map_whitelist": "reset_map_votemap_whitelist",
    "do_reset_votekick_threshold": "reset_votekick_thresholds",
    "do_set_map_whitelist": "set_votemap_whitelist",
    "do_switch_player_now": "switch_player_now",
    "do_switch_player_on_death": "switch_player_on_death",
    "do_temp_ban": "temp_ban",
    "do_unban": "unban",
    "do_unban_profanities": "do_unban_profanities",
    "do_unwatch_player": "unwatch_player",
    "do_watch_player": "watch_player",
    "public_info": "get_public_info",
    "server_list": "get_server_list",
    "live_scoreboard": "get_live_scoreboard",
}

V_10_0_0_TO_V9_9_1_CMD_MAPPING = {
    v: k for k, v in V9_9_1_TO_V_10_0_0_CMD_MAPPING.items()
}


UP_VERSION_TO_CMD_MAPPING = {
    Versions.v9_9_1: {Versions.v10_0_0: V_10_0_0_TO_V9_9_1_CMD_MAPPING}
}

DOWN_VERSION_TO_CMD_MAPPING = {
    Versions.v10_0_0: {Versions.v9_9_1: V_10_0_0_TO_V9_9_1_CMD_MAPPING}
}

V9_9_1_TO_V_10_0_0_ARG_MAPPING = {
    "do_add_admin": {"steam_id_64": "player_id", "name": "description"},
    "do_add_maps_to_rotation": {
        "maps": "map_names",
    },
    "do_add_vip": {"steam_id_64": "player_id", "name": "description"},
    "blacklist_player": {"steam_id_64": "player_id", "name": "player_name"},
    "flag_player": {
        "steam_id_64": "player_id",
    },
    "do_kick": {"steam_id_64": "player_id", "name": "player_name"},
    "do_message_player": {"steam_id_64": "player_id", "name": "player_name"},
    "do_perma_ban": {"steam_id_64": "player_id", "name": "player_name"},
    "post_player_comment": {"steam_id_64": "player_id"},
    "do_punish": {"steam_id_64": "player_id", "name": "player_name"},
    "do_remove_admin": {"steam_id_64": "player_id"},
    "do_remove_temp_ban": {"steam_id_64": "player_id"},
    "do_remove_vip": {"steam_id_64": "player_id"},
    "set_broadcast": {"msg": "message"},
    "do_switch_player_now": {"player": "player_name"},
    "do_switch_player_on_death": {"player": "player_name"},
    "do_temp_ban": {"steam_id_64": "player_id", "name": "player_name"},
    "do_unban": {"steam_id_64": "player_id"},
    "unblacklist_player": {"steam_id_64": "player_id"},
    "do_unwatch_player": {"steam_id_64": "player_id"},
    "get_player_info": {"player": "player_name"},
    "get_detailed_player_info": {"player": "player_name"},
    "get_ban": {"player": "player_name"},
    "set_queue_length": {"num": "value"},
    "set_vip_slots_num": {"num": "value"},
    "set_autobalance_enabled": {"bool_": "value"},
    "set_votekick_enabled": {"bool_": "value"},
}

V_10_0_0_TO_V9_9_1_ARG_MAPPING = {
    k: {k2: v2 for k2, v2 in v.items()}
    for k, v in V9_9_1_TO_V_10_0_0_ARG_MAPPING.items()
}

UP_VERSION_TO_ARG_MAPPING = {
    Versions.v9_9_1: {Versions.v10_0_0: V_10_0_0_TO_V9_9_1_ARG_MAPPING}
}
DOWN_VERSION_TO_ARG_MAPPING = {
    Versions.v10_0_0: {Versions.v9_9_1: V_10_0_0_TO_V9_9_1_ARG_MAPPING}
}
