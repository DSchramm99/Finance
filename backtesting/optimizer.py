import itertools
from .engine import run_backtest
import numpy as np


def train_test_split(data, train_end_date):
    train = data[data.index <= train_end_date]
    test = data[data.index > train_end_date]
    return train, test


def score_function(metrics):
    total_return = metrics["total_return"]
    max_drawdown = metrics["max_drawdown"]

    return total_return - abs(max_drawdown)


def optimize_parameters(
    train_data,
    k_values,
    stop_percent_values
):

    best_score = -np.inf
    best_params = None
    best_metrics = None

    for k, stop_pct in itertools.product(k_values, stop_percent_values):

        _, metrics = run_backtest(
            train_data,
            k_atr=k,
            fixed_stop_pct=stop_pct
        )

        score = score_function(metrics)

        if score > best_score:
            best_score = score
            best_params = {
                "k": k,
                "fixed_stop_pct": stop_pct
            }
            best_metrics = metrics

    if best_params is None:
        return None

    return {
        **best_params,
        **best_metrics,
        "score": best_score
    }


def evaluate_on_test(test_data, k, fixed_stop_pct):

    df, metrics = run_backtest(
        test_data,
        k_atr=k,
        fixed_stop_pct=fixed_stop_pct
    )

    return metrics, df