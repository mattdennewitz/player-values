"""
Calculates positional eligibility
"""

from pydash import sorted_index_by

import const
import helpers


def mark_positional_eligibility(player_pool, lg_positions_elig, lg_positions):
    """Marks each player with all positions and most valuable position
    """

    all_pos = const.POS_PRIORITY.keys()
    find_sort_pos = lambda pos: const.POS_PRIORITY[pos]

    for player in player_pool:
        pos_eligible = []

        for pos in all_pos:  # scan *all* positions for eligibility
            if lg_positions[pos] == 0:
                continue  # ignore positions unused by the league

            # this might need to be adjusted for ohtani
            if pos == 'dh' and player['player_type'] == 'p':
                continue
            if pos == 'p' and player['player_type'] == 'b':
                continue

            # build positional eligibility ordered by scarcity
            if player['positions'][pos] >= lg_positions[pos]:
                idx = sorted_index_by(pos_eligible, pos, find_sort_pos)
                pos_eligible.insert(idx, pos)

        if not pos_eligible:
            pos_eligible = helpers.force_player_positions(player)

        player['pos_eligible'] = pos_eligible
        player['pos_mv'] = pos_eligible[0] if pos_eligible else None

    return player_pool
