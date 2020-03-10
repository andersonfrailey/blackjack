import altair as alt
import pandas as pd
import numpy as np
import copy


def results_pct(data, as_series=True):
    """
    Return the percentage of hands won, lost, and pushed
    in a given dataset
    Parameters
    ----------
    data: DataFrame containing the player hand history
    as_series: Boolean indicating whether the results should be returned as a
        series
    Returns
    -------
    Pandas series with the percentages of hands won, lost, and pushed,
    or a tuple containing the same information if `as_series` is false
    """
    results = data["result"].value_counts(normalize=True)
    if as_series:
        return results
    else:
        # ensure that win, loss, and push are in the results index
        for result in ["win", "loss", "push"]:
            if not result in results.index:
                results[result] = 0
        return results["win"], results["loss"], results["push"]


def detailed_results_pct(data):
    """
    """
    # make a copy od the data since we'll be modifying it
    data = copy.deepcopy(data)
    if isinstance(data, list):
        data = pd.DataFrame(data)
    # find probability of each event
    # winning options
    data["detailed_results"] = np.where(
        data["result"] == "win", np.where(
            data["blackjack"] == 0, np.where(
                data["double_down"] == 0, "win_no_bj_no_double",
                "win_no_bj_double"
            ), np.where(
                data["from_split"] == 0, "win_blackjack", "win_blackjack_split"
            )
        ), ""
    )
    # losing options
    data["detailed_results"] = np.where(
        data["result"] == "loss", np.where(
            data["dealer_blackjack"] == 0, np.where(
                data["double_down"] == 0, "loss_no_dbj_no_double",
                "loss_no_dbj_double"
            ), "loss_dbj"
        ), data["detailed_results"]
    )
    # pushes
    data["detailed_results"] = np.where(
        data["detailed_results"] == "", "push", data["detailed_results"]
    )
    pcts = data["detailed_results"].value_counts(normalize=True)
    possible_results = [
        "win_no_bj_no_double", "win_no_bj_double",
        "win_blackjack", "loss_no_dbj_no_double", "loss_no_dbj_double",
        "loss_dbj", "push", "win_blackjack_split"
    ]
    for result in possible_results:
        if result not in pcts.index:
            pcts[result] = 0

    return pcts


def result_heatmap(data, result="win", title=None,
                   width=500, height=500):
    """
    Function that takes a player's history data and returns an altair chart
    showing their winning percentage based on their hand totals and the
    dealer's up card
    """
    assert result in ["win", "loss", "push"], (
        "'result' must be 'win', 'loss', or 'push'"
    )
    if not title:
        title = f"{result.title()} Percentage"
    # convert data to a DataFrame if it's just a player's history list
    if isinstance(data, list):
        data = pd.DataFrame(data)

    # remove any hands where the dealer had blackjack or the player busted
    sub_data = data[(data["dealer_blackjack"] == 0) &
                    (data["total"] <= 21)].copy()
    # calculate winning percentage for each total and dealer up card combo
    grouped_pct = sub_data.groupby(
        ["total", "dealer_up"]
    ).apply(results_pct, as_series=False)
    # unpack the tuple returned by groupby function and rename columns
    grouped_pct = grouped_pct.apply(pd.Series)
    grouped_pct.columns = ["win", "loss", "push"]
    # reset index and sort for plotting
    pct_data = grouped_pct.reset_index().sort_values("total", ascending=False)
    # dynamically determine how the legend should be labeled
    min_val = round(min(pct_data[["win", "loss", "push"]].min()), 1)
    max_val = round(max(pct_data[["win", "loss", "push"]].max()), 1)
    min_int = int(min_val * 10)
    max_int = int(max_val * 10)
    values = [
        round(x * 0.1, 1) for x in range(min_int, max_int + 1)
    ]
    # create altair heatmap
    chart = alt.Chart(
        pct_data, title=title, width=width, height=height
    ).mark_rect(binSpacing=1).encode(
        x=alt.X(
            "dealer_up:O",
            axis=alt.Axis(orient="top", labelAngle=0),
            title="Dealer Up Card"
        ),
        y=alt.Y(
            "total:O",
            title="Player Total",
            sort=alt.EncodingSortField(op="mean", order="descending")
        ),
        color=alt.Color(
            f"{result}:Q",
            legend=alt.Legend(
                title=f"{result.title()} Probability",
                values=values
            )
        ),
        tooltip=[
            alt.Tooltip("dealer_up", title="Dealer Up Card"),
            alt.Tooltip("total", title="Player Total"),
            alt.Tooltip(f"{result}", title=f"{result.title()} Probability")
        ]
    )

    return chart


def pct_bust(data):
    """
    Calculate the probability of busting in a given dataset
    """
    return round((data["new_total"] > 21).sum() / len(data), 3)


def outcome_bars(data, name=None, width=100):
    """
    Create a bar chart showing the percentage of hands won, lost, and pushed
    """
    # if it's a dataframe already, just add the name for the legend
    if isinstance(data, pd.DataFrame):
        data_list = [data]
    elif isinstance(data, list):
        # check if it's a list of dicionaries, like player history, or a list
        # of lists
        for item in data:
            l_o_d = isinstance(item, dict)
        # if it's a list of dictionaries, just convert them
        if l_o_d:
            data_list = [pd.DataFrame(data)]
        else:
            data_list = [pd.DataFrame(item) for item in data]
    else:
        msg = "'data' must be a DataFrame or list"
        raise TypeError(msg)
    # calculate percentages
    # assign name to data
    if not name:
        name = [f"Game{i}" for i in range(len(data))]
    plot_data_list = []  # list to hold dataframes that will be plotted
    for _name, _data in zip(name, data_list):
        win, loss, push = results_pct(_data, as_series=False)
        plot_data_list.append(
            {"game": _name, "result": "Win", "pct": win, "order": 1},
        )
        plot_data_list.append(
            {"game": _name, "result": "Loss", "pct": loss, "order": 2}
        )
        plot_data_list.append(
         {"game": _name, "result": "Push", "pct": push, "order": 3} 
        )
    plot_data = pd.DataFrame(plot_data_list)

    # create altair chart
    chart = alt.Chart(plot_data, width=width).mark_bar().encode(
        x=alt.X(
            "game",
            axis=alt.Axis(labelAngle=-45),
            title=None,
            sort=["Win", "Loss", "Push"]
        ),
        y=alt.Y(
            "pct:Q"
        ),
        color=alt.Color(
            "game:O",
            legend=None
        ),
        column=alt.Column(
            "result:O",
            title="Result"
        ),
        tooltip=[
            alt.Tooltip("pct", title="Pct")
        ]
    )
    return chart


def house_edge(data, game_params):
    """
    Function for calculating house edge.
    Parameters
    ----------
    data: data from your simulations
    game_params: parameters from the game you simulated
    """
    pcts = detailed_results_pct(data)
    # calculate expected payout
    expected_value = (
        (game_params.payout * pcts["win_no_bj_no_double"]) +
        (game_params.payout * pcts["win_no_bj_double"] * 2) +
        (game_params.blackjack_payout * pcts["win_blackjack"]) +
        (game_params.split_blackjack_payout * pcts["win_blackjack_split"]) -
        (pcts["loss_no_dbj_no_double"]) -
        (pcts["loss_no_dbj_double"] * 2) -
        (pcts["loss_dbj"])
    )
    print(
        "Because all in-game situations may not occur during a simulation, "
        "the expected value calculated should be interpreted as an "
        "approximation"
    )

    return expected_value
