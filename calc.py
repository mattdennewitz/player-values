"""
Percent Valuation
"""

import collections
import itertools
import functools
import json
import operator
import random
import statistics

from pprint import pprint

from pydash import pick, sorted_index_by

import builders
import const


def main():
    player_pool = json.load(open('player-pool.json'))
    random.shuffle(player_pool)

    outcomes = None

    # mark player's pos eligibility
    player_pool = builders.mark_positional_eligibility(
        player_pool, const.POS_ELIGIBILITY, const.POSITIONS)

    outcomes = []
    completed = False

    while not completed:
        draftable_players = player_pool[:const.DRAFTABLE_PLAYERS]

        # calculate league averages for all stats
        lg_avgs, lg_devs, lg_rates = builders.calculate_league_rates(
            draftable_players, const.BATTING_COMPONENTS,
            const.PITCHING_COMPONENTS)

        # apply z-scores for components and rates
        player_pool = builders.apply_z_scores(player_pool, lg_avgs, lg_devs,
                                              lg_rates)

        # sort by z-value
        player_pool = sorted(
            player_pool, key=operator.itemgetter('z_value'), reverse=True)

        # calculate replacement levels for each position
        replacement_levels = builders.calculate_replacement_levels(
            player_pool, const.BATTING_POS, const.PITCHING_POS)

        # calculate player value above replacement, re-sort
        player_pool = builders.apply_replacement_levels(
            player_pool, replacement_levels)
        player_pool = sorted(
            player_pool, key=operator.itemgetter('fvarz'), reverse=True)

        # check for convergence
        for prior in outcomes:
            if prior == lg_devs:  # true if we have converged
                player_pool = set_dollar_values(player_pool)
                # player_pool = sorted(
                #     player_pool,
                #     key=operator.itemgetter('dollars'),
                #     reverse=True)

                output = [
                    pick(player, 'name', 'pos_mv', 'pos_eligible', 'dollars')
                    for player in player_pool
                ]

                json.dump(output, open('final.json', 'w'))
                completed = True  # done

        outcomes.append(lg_devs)


if __name__ == '__main__':
    main()
