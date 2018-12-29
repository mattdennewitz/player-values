"""
Creates subset of Steamer projection data
"""

import json

from pydash import pick

from models import Player

player_pool = json.load(open('steamer-2019.json'))
schema = Player()
player_pool = [schema.dump(player) for player in player_pool]
player_pool = filter(
    lambda p: p['components']['b_pa'] >= 20 or p['components']['p_ip'] >= 5,
    player_pool)

json.dump(list(player_pool), open('player-pool.json', 'w'))
