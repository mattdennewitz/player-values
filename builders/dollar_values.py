"""
Builds dollar values
"""

import statistics

import const


def apply_dollar_values(context: dict, pool_type: str):
    """Sets dollar values for pool of players based on % contribution
    """

    player_pool = context[pool_type]['players']
    n_draftable = context[pool_type]['n_draftable']
    split = context[pool_type]['split']
    pool_type_budget = split * (context['budget'] * context['teams'])

    marginal_money = pool_type_budget - (1 * n_draftable)

    total_value = sum(
        [p['fvarz'] for p in player_pool[:n_draftable] if p['fvarz'] > 0])
    scale_factor = marginal_money / total_value

    print('budg', pool_type_budget)
    print('marg', marginal_money)
    print('totalv', total_value)
    print('scale', scale_factor)

    for player in player_pool:
        player['dollars'] = player['fvarz'] * scale_factor + 1

    return context
