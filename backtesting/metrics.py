import numpy as np


def calculate_metrics(df):
    returns = df["Equity"].pct_change().dropna()

    total_return = df["Equity"].iloc[-1] - 1

    # Profit Factor
    gains = returns[returns > 0].sum()
    losses = returns[returns < 0].sum()

    profit_factor = abs(gains / losses) if losses != 0 else np.inf

    # Max Drawdown
    cummax = df["Equity"].cummax()
    drawdown = (df["Equity"] - cummax) / cummax
    max_drawdown = drawdown.min()

    return {
        "total_return": total_return,
        "profit_factor": profit_factor,
        "max_drawdown": max_drawdown,
    }