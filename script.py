from pathlib import Path

import modules.shared as shared

params = {
    "display_name": "Token Blocker",
    "is_tab": False,
}

BASE_PATH = Path(__file__).parent

loaded_blocklist = None
blocklist: str = ''


def state_modifier(state):
    global blocklist, loaded_blocklist

    if loaded_blocklist != shared.model_name:
        path = BASE_PATH / 'block-lists' / shared.model_name
        loaded_blocklist = shared.model_name

        if not path.exists():
            return state

        with open(path, "r") as f:
            blocklist = f.read()

    state["custom_token_bans"] = (state["custom_token_bans"] + ', ' if state["custom_token_bans"] else '') + blocklist

    return state
