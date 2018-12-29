"""
Tests league rate calculation
"""

from builders import league_rates
import const
from models import Player


def test_calc_league_rates():
    """Ensures league averages are soundly calculated
    """

    schema = Player()
    player_trout = schema.dump({
        'player_name': 'Mike Trout',
        'player_type': 'b',
        'player_id': 1,
        'components': {
            'B_H': 20,
            'B_AB': 50,
            'B_HR': 30,
        }
    })
    player_stanton = schema.dump({
        'player_name': 'Giancarlo Stanton',
        'player_type': 'b',
        'player_id': 2,
        'components': {
            'B_H': 10,
            'B_AB': 40,
            'B_HR': 29,
        }
    })

    avgs, devs, rates = league_rates.calculate_league_rates(
        [player_trout, player_stanton], const.BATTING_COMPONENTS)

    assert avgs['b_hr'] == 29.5
    assert avgs['b_h'] == 15.
    assert avgs['b_ab'] == 45.
    assert rates['b_avg'], 3 == 0.333  # should be rounded
