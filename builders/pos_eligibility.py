"""
Calculates positional eligibility
"""

import itertools

from pydash import sorted_index_by

import const
import helpers


def add_flex_positions(player, lg_positions):
    """Defines flex position eligibility
    """

    flex_pos = []
    pos_eligible = player['pos_eligible']

    if 'b2' in pos_eligible or 'ss' in pos_eligible:
        flex_pos.append('mi')

    if 'b1' in pos_eligible or 'b3' in pos_eligible:
        flex_pos.append('ci')

    if 'mi' in flex_pos or 'ci' in flex_pos:
        flex_pos.append('if_')

    if player['player_type'] == 'b':
        flex_pos.append('dh')

    if player['player_type'] == 'p':
        flex_pos.append('p')

    return flex_pos


def mark_positional_eligibility(player_pool, lg_positions, lg_eligibility):
    """Marks each player with all positions and most valuable position

    1. Mark core position eligibility
    2. Add flex positions
    3. Set most valuable position that isn't a flex position except OF
    """

    find_sort_pos = lambda pos: const.POS_PRIORITY[pos]

    for player in player_pool:
        player['above_repl'] = False

        pos_eligible = []  # collects all eligible positions
        player_pos = player['positions']
        player_type = player['player_type']

        # start w/ positions used by *every* league
        for pos in const.POS_CORE:
            pos_elig = (lg_eligibility['b']
                        if not pos in const.POS_P else lg_eligibility[pos])

            if player_pos[pos] >= pos_elig:
                idx = sorted_index_by(pos_eligible, pos, find_sort_pos)
                pos_eligible.insert(idx, pos)

        # sprinkle in outfield positions used by *this* league
        of_pos = [pos for pos in const.POS_OF if pos in lg_positions]
        for pos in of_pos:
            if player_pos[pos] >= lg_eligibility['b']:
                idx = sorted_index_by(pos_eligible, pos, find_sort_pos)
                pos_eligible.insert(idx, pos)

        if not pos_eligible:
            pos_eligible = helpers.force_player_positions(player)

        # set core positions
        player['pos_eligible'] = pos_eligible

        # add flex positions used by *this* league
        player['pos_flex'] = add_flex_positions(player, lg_positions)

        # find most valuable position
        player['pos_mv'] = (pos_eligible[0]
                            if pos_eligible else player['pos_flex'][0])

        player['pos_check'] = [player['pos_mv']] + player['pos_flex']
        player['pos_all'] = player['pos_eligible'] + player['pos_flex']

    return player_pool
