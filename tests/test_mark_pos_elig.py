"""
Tests positional eligibility setting for players
"""

import random

from builders import mark_positional_eligibility
import const
from models import Player


def test_position_prioritization(app_config):
    """Ensures correct position insertion order
    """

    schema = Player()

    player = schema.dump({
        'player_type': 'b',
        'positions': {
            '3B': 50,
            'SS': 12,
            'SP': 14,  # ohtani time
        },
        'player_id': 1,
        'components': {},
    })

    player_pool = mark_positional_eligibility([player], app_config['lg_pos'],
                                              app_config['eligibility'])
    player = player_pool[0]

    assert player['pos_mv'] == 'ss'
    assert player['pos_eligible'] == ['ss', 'b3', 'sp']


def test_all_batters_get_dh(app_config):
    """Ensures all batters receive DH (U) eligibility
    """

    schema = Player()

    player_pool = [
        schema.dump({
            'player_type': 'b',
            'positions': {
                '1B': 50,
            },
            'player_id': i,
            'components': {},
        }) for i in range(20)
    ]

    player_pool = mark_positional_eligibility(
        player_pool, app_config['lg_pos'], app_config['eligibility'])

    for player in player_pool:
        assert player['pos_mv'] == 'b1'
        assert 'dh' in player['pos_flex']


def test_pitchers_coerced_to_rp_if_empty(app_config):
    """Ensures pitchers are marked as RP if no games started are projected
    """

    schema = Player()

    player = schema.dump({
        'player_type': 'p',
        'positions': {},
        'player_id': 1,
        'components': {},  # implicitly no games started
    })

    player_pool = mark_positional_eligibility([player], app_config['lg_pos'],
                                              app_config['eligibility'])
    player = player_pool[0]
    assert player['pos_mv'] == 'rp'
    assert 'dh' not in player['pos_eligible']  # dh for batters only


def test_pitchers_set_to_sp(app_config):
    """Pitchers with GS projected should be marked as SP
    """

    schema = Player()

    player = schema.dump({
        'player_type': 'p',
        'positions': {},
        'player_id': 1,
        'components': {
            'P_GS': 1,
        },
    })

    player_pool = mark_positional_eligibility([player], app_config['lg_pos'],
                                              app_config['eligibility'])
    player = player_pool[0]
    assert player['pos_mv'] == 'sp'
