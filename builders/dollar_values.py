"""
Builds dollar values
"""

import const


def apply_dollar_values(player_pool):
    """Sets dollar values for pool of players based on % contribution
    """

    batting_value = sum([
        player['fvarz'] for player in player_pool
        if player['fvarz'] > 0 and player['player_type'] == 'b'
    ])
    pitching_value = sum([
        player['fvarz'] for player in player_pool
        if player['fvarz'] > 0 and player['player_type'] == 'p'
    ])

    batting_var = const.LEAGUE_BATTING_BUDGET / batting_value
    pitching_var = const.LEAGUE_PITCHING_BUDGET / pitching_value

    for player in player_pool:
        mult = batting_var if player['player_type'] == 'b' else pitching_var
        player['dollars'] = player['fvarz'] * mult

    return player_pool
