import altair as alt
import pandas as pd


def results_pct(data):
    """
    Return the percentage of hands won, lost, and pushed
    in a given dataset
    """
    num_hands = len(data)
    pct_loss = len(data[data["result"] == "loss"]) / num_hands
    pct_win = len(data[data["result"] == "win"]) / num_hands
    pct_push = len(data[data["result"] == "push"]) / num_hands
    return round(pct_win, 3), round(pct_loss, 3), round(pct_push, 3)


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
    grouped_pct = sub_data.groupby(["total", "dealer_up"]).apply(results_pct)
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
        win, loss, push = results_pct(_data)
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
    if isinstance(data, list):
        data = pd.DataFrame(data)
    # find probability of each event
    _, loss_prob, push_prob = results_pct(data)
    # separate winning events into blackjack and non-blackjack wins
    num_hands = len(data)
    blackjack_prob = len(data[data["blackjack"] == 1]) / num_hands
    win_prob = (len(data[(data["blackjack"] == 0) &
                         (data["result"] == "win")]) /
                num_hands)
    # calculate expected payout
    expected_value = (
        (game_params.payout * win_prob) +
        (game_params.blackjack_payout * blackjack_prob) +
        (-1 * loss_prob) +
        (0 * push_prob)
    )

    return expected_value * -1
