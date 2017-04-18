# Holds functions to create plots
from collections import OrderedDict
import numpy as np
import os
import pandas as pd
try:
    bokeh_available = True
    import bokeh.io as bio
    from bokeh.charts import Bar
    from bokeh.plotting import figure
except ImportError:
    bokeh_available = False


def requires_bokeh(func):
    """
    Decorator for functions that require bokeh
    If bokeh is available, this does nothing.
    If bokeh is not available, raise an exemption error
    """
    def wrapped_f(*args, **kwargs):
        """
        Raise error if bokeh is not available, otherwise does nothing
        """
        if bokeh_available:
            return func(*args, **kwargs)
        else:
            msg = "Install graphing package bokeh"
            raise RuntimeError(msg)
    return (wrapped_f)


def write_graph_file(figure, filename, title):
    """
    """
    delete_file(filename)
    bio.output_file(filename=filename, title=title)
    bio.save(figure)


def delete_file(filename):
    """
    Remove file if it exits
    """
    if os.path.isfile(filename):
        os.remove(filename)


@requires_bokeh
def poker_plot(data):
    """
    Returns a plot showing the results of the poker side bets
    """
    keys = ['Royal Flush', 'Straight Flush', 'Flush', 'Straight',
            'Three of a Kind', 'Loss']
    pcts_list = []
    # Count separately for each deck size
    for x in np.unique(data['decks']):
        pcts = OrderedDict()
        for item in keys:
            pcts[item] = (float(len(data[(data['poker'] == item) &
                                         (data['decks'] == x)])) /
                          len(data[data['decks'] == x]))
        pcts = pd.DataFrame.from_dict(pcts, 'index')
        pcts.columns = ['Pct']
        pcts['Decks'] = x
        pcts_list.append(pcts)
    pcts_df = pd.concat(pcts_list)
    pcts_df['results'] = pcts_df.index

    # Create plot
    pkr_bar = Bar(pcts_df, 'Decks', 'Pct', agg='sum', group='results',
                  bar_width=0.4, legend='center',
                  title='Poker Side Bet Results')
    pkr_bar.legend.orientation = 'horizontal'
    return pkr_bar


@requires_bokeh
def inbtwn_plot(data):
    """
    Returns bar graph depicting results of in between side bet

    Parameters
    ----------
    data: DataFrame containing data from the data.py side_bet function

    Returns
    -------
    Bokeh Bar Chart object
    """
    keys = [0, 1, 2, 3, '4+', 'Loss']
    pcts_list = []
    # Loop through each deck value to count results for each hand
    for x in np.unique(data['decks']):
        pcts = OrderedDict()
        # Loop through each result to get the percentages
        for item in keys:
            pcts[item] = ((float(len(data[(data['inbtwn'] == item) &
                                          (data['decks'] == x)])) /
                          len(data[data['decks'] == x])))
        pcts = pd.DataFrame.from_dict(pcts, 'index')
        pcts.columns = ['Pct']
        pcts['Decks'] = x
        pcts_list.append(pcts)
    pcts_df = pd.concat(pcts_list)
    pcts_df['results'] = pcts_df.index

    # Create plot
    inbtwn_bar = Bar(pcts_df, 'Decks', 'Pct', agg='sum', group='results',
                     bar_width=1, legend='top_left',
                     title='In-Between Side Bet Results by Spread')
    return inbtwn_bar


@requires_bokeh
def results_plot(data):
    """
    Plots results of all the hands played by deck

    Parameters
    ----------
    data: DataFrame containing hand results

    Returns
    -------
    Bokeh Bar Graph
    """
    replacements = {
        'Result': {
            0: 'Busts',
            1: 'Wins',
            2: 'Loses',
            3: 'Push',
            4: 'Dealer Busts',
            5: 'Dealer Blackjack'
        }
    }
    data.replace(replacements, inplace=True)
    keys = ['Bust', 'Wins', 'Loses', 'Push', 'Dealer Busts',
            'Dealer Blackjack']
    pcts_list = []
    for x in np.unique(data['decks']):
        pcts = {}
        for i in range(0, 6):
            pcts[keys[i]] = ((float(len(data[(data['result'] == i) &
                                             (data['decks'] == x)])) /
                             len(data['decks'] == x)))
        pcts = pd.DataFrame.from_dict(pcts, 'index')
        pcts.columns = ['Pct']
        pcts['Decks'] = x
        pcts_list.append(pcts)
    pcts_df = pd.concat(pcts_list)
    pcts_df['result'] = pcts_df.index

    rslt_bar = Bar(pcts_df, 'Decks', 'Pct', agg='sum', group='result',
                   bar_width=0.4, legend='bottom_center',
                   title='Hand Results from Player Perspective')
    rslt_bar.legend.orientation = 'horizontal'
    return rslt_bar


@requires_bokeh
def results_pct_plot(data):
    """
    Returns Bokeh plot showing the result of hands by the count at the start of
    the hand

    Parameters
    ----------
    data: DataFrame containing hand results

    Returns
    -------
    Bokeh figure
    """
    p_win = OrderedDict()
    d_win = OrderedDict()
    push = OrderedDict()
    count_freq = OrderedDict()

    # Loop through each result
    for item in np.unique(data['count']):
        p_win[item] = (float(len(data[(data['result'] != 0) &
                                      (data['result'] != 2) &
                                      (data['result'] != 5) &
                                      (data['result'] != 3) &
                                      (data['count'] == item)])) /
                       len(data[data['count'] == item]))
        d_win[item] = (float(len(data[(data['result'] != 1) &
                                      (data['result'] != 4) &
                                      (data['result'] != 3) &
                                      (data['count'] == item)])) /
                       len(data[data['count'] == item]))
        push[item] = (float(len(data[(data['result'] == 3) &
                                     (data['count'] == item)])) /
                      len(data[data['count'] == item]))
        count_freq[item] = (float(len(data[data['count'] == item])) /
                            len(data['count']))
    # Create the figure
    fig = figure(title='Percentages by Count')
    fig.line(p_win.keys(), p_win.values(), legend='Player Wins', line_width=2)
    fig.line(d_win.keys(), d_win.values(), legend='Dealer Wins', line_width=2,
             color='red')
    fig.line(push.keys(), push.values(), legend='Push', line_width=2,
             color='orange')
    fig.line(count_freq.keys(), count_freq.values(), legend='Count Frequency',
             color='black')
    fig.legend.location = 'top_center'
    return fig


@requires_bokeh
def card_freq_plot(data):
    """
    Return plot of the freqency of each card in a given count
    """
    freq_dict = OrderedDict()
    for rank in np.unique(data['card']):
        card_dict = OrderedDict()
        for val in np.unique(data['count']):
            freq = (float(len(data[(data['card'] == rank) &
                                   (data['count'] == val)])) /
                    len(data[data['count'] == val]))
            card_dict[val] = freq
        freq_dict[rank] = card_dict

    fig = figure(title='Frequency of Cards Occuring Based on the Count')
    colors = ['blue', 'red', 'purple', 'green', 'pink', 'gold', 'grey',
              'lawngreen', 'orange', 'cyan']
    i = 0
    for key in freq_dict.keys():
        fig.line(freq_dict[key].keys(), freq_dict[key].values(),
                 legend=str(key), color=colors[i], line_width=2)
        i += 1
    fig.legend.location = 'top_center'
    return fig
