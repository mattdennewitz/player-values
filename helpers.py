"""
Corrections
"""


def force_player_positions(player):
    """Sets positional eligibility for anyone
    """

    if player['player_type'] == 'p':
        if player['components']['p_gs'] > player['components']['p_g'] * .33:
            return ['sp']
        return ['rp']

    return []
