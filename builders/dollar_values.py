"""
Builds dollar values
"""

import const


def apply_dollar_values(context: dict, pool_type: str):
    """Sets dollar values for pool of players based on % contribution
    """

    player_pool = context[pool_type]['players']
    n_draftable = context[pool_type]['n_draftable']

    marginal_money = (
        context[pool_type]['split'] * const.LEAGUE_BUDGET - (1 * n_draftable))
    total_value = sum([p['fvarz'] for p in player_pool[:n_draftable]])
    scale_factor = marginal_money / total_value

    for player in player_pool:
        player['dollars'] = player['fvarz'] * scale_factor + 1

    return context
