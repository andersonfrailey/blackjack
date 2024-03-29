"""
Test utils module of Py21
"""
import pandas as pd
import pytest
from py21.utils import (results_pct, result_heatmap, outcome_bars, house_edge,
                        detailed_results_pct)
from py21 import Game


def test_charts(basic_player):
    game = Game([basic_player])
    game.simulate(10000)
    # heatmap
    chart = result_heatmap(basic_player.history)
    # outcome bars
    chart = outcome_bars(basic_player.history)


def test_results_pct(basic_player):
    data = pd.DataFrame(basic_player.history)
    results = results_pct(data)
    assert 1 <= len(results) <= 4
    assert results.sum() == pytest.approx(1.0)
    # test when results are returned as a tuple
    results = results_pct(data, as_series=False)
    assert len(results) == 4
    assert sum(results) == pytest.approx(1.0)


def test_detailed_results_pct(basic_player):
    data = pd.DataFrame(basic_player.history)
    results = detailed_results_pct(data)
    assert len(results) == 8
    assert results.sum() == pytest.approx(1.0)


def test_house_edge(basic_player):
    g = Game([basic_player])
    edge = house_edge(basic_player, g.game_params)
    assert isinstance(edge, float)
