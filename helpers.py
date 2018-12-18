"""
Corrections
"""


def force_player_positions(player):
    """Sets positional eligibility for anyone
    """

    player_id = player['player_id']

    if player['player_type'] == 'p':
        if player['components']['p_gs'] > 0:
            return ['sp']
        return ['rp']

    return ['dh']
