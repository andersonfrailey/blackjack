"""
Test utils module of Py21
"""
import altair as alt
import pandas as pd
from py21.utils import results_pct, result_heatmap, outcome_bars, house_edge
from py21 import Game


def test_charts(basic_player):
    game = Game([basic_player])
    game.simulate(50)
    # heatmap
    chart = result_heatmap(basic_player.history)
    assert isinstance(chart, alt.vegalite.v3.api.Chart)
    # outcome bars
    chart = outcome_bars(basic_player.history)
    assert isinstance(chart, alt.vegalite.v3.api.Chart)


def test_results_pct(basic_player):
    data = pd.DataFrame(basic_player.history)
    results = results_pct(data)
    assert len(results) == 3


def test_house_edge(basic_player):
    game = Game([basic_player])
    edge = house_edge(basic_player.history, game.game_params)
    assert isinstance(edge, float)
