"""
Builds and applies replacement levels
"""

import collections

import const


def calculate_replacement_levels(player_pool, batting_pos, pitching_pos):
    """Calculates replacement levels for each position
    """

    pos_obvs = collections.Counter()
    replacement_levels = {}

    for player in player_pool:
        positions = (batting_pos
                     if player['player_type'] == 'b' else pitching_pos)
        max_per = (const.BATTING_POS
                   if player['player_type'] == 'b' else const.PITCHING_POS)

        # indiciate replacement level for player's most valuable position
        pos = player['pos_mv']
        if pos_obvs[pos] < max_per[pos]:
            replacement_levels[pos] = player['z_value']
            pos_obvs[pos] += 1

    return replacement_levels


def apply_replacement_levels(player_pool, replacement_levels):
    """Sets replacement level for player based on most valuable position
    """

    for player in player_pool:
        player['fvarz'] = (
            player['z_value'] - replacement_levels[player['pos_mv']])

    return player_pool
