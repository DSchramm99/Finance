import pandas as pd
import numpy as np


def run_backtest(
    df,
    k_atr=1.5,
    fixed_stop_pct=0.05,
    return_equity=False
):

    df = df.copy()

    # =========================
    # Indicators
    # =========================

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["ATR"] = (df["High"] - df["Low"]).rolling(14).mean()

    # =========================
    # Trading State
    # =========================

    position = 0
    entry_price = 0
    highest_price = 0

    equity = 1.0
    equity_curve = []

    trades = []

    # =========================
    # Backtest Loop
    # =========================

    for i in range(len(df)):

        price = df["Close"].iloc[i]
        sma20 = df["SMA20"].iloc[i]
        atr = df["ATR"].iloc[i]

        if pd.isna(sma20) or pd.isna(atr):
            equity_curve.append(equity)
            continue

        # -----------------
        # ENTRY
        # -----------------

        if position == 0:

            if price > sma20:

                position = 1
                entry_price = price
                highest_price = price

        # -----------------
        # MANAGE POSITION
        # -----------------

        else:

            highest_price = max(highest_price, price)

            atr_stop = highest_price - (k_atr * atr)
            pct_stop = entry_price * (1 - fixed_stop_pct)

            stop_level = max(atr_stop, pct_stop)

            if price < stop_level:

                trade_return = (price / entry_price) - 1

                equity *= (1 + trade_return)

                trades.append(trade_return)

                position = 0

        equity_curve.append(equity)

    # =========================
    # Metrics
    # =========================

    total_return = equity - 1

    equity_series = pd.Series(equity_curve)

    running_max = equity_series.cummax()
    drawdown = (equity_series - running_max) / running_max

    max_drawdown = drawdown.min()

    profit_factor = None

    if len(trades) > 0:

        gains = [t for t in trades if t > 0]
        losses = [t for t in trades if t < 0]

        if len(losses) > 0:
            profit_factor = abs(sum(gains) / sum(losses))

    metrics = {
        "total_return": total_return,
        "max_drawdown": max_drawdown,
        "profit_factor": profit_factor
    }

    equity_df = pd.DataFrame({
        "Portfolio_Equity": equity_series
    })

    if return_equity:
        return equity_df, metrics
    else:
        return None, metrics