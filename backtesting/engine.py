import pandas as pd
import numpy as np
from strategy.signal_engine import add_indicators, calculate_scores

def run_backtest(
    df,
    k_atr=1.5,
    rr_ratio=2.0,
    start_capital=2000,
    return_equity=False
):
    """
    Backtest using the improved strategy setup:
    - SMA20 trend filter
    - SMA200 long term trend filter
    - RSI filter
    - ATR-based scoring
    - Chandelier Trailing Stop
    - Chandelier Take Profit
    """
    df = add_indicators(df)

    # Pre-calculate scores
    scores = df.apply(lambda row: calculate_scores(row), axis=1)
    df["trend_score"] = [s[0] for s in scores]
    df["risk_score"] = [s[1] for s in scores]
    df["final_score"] = [s[2] for s in scores]

    # Trading State
    position = 0
    entry_price = 0.0
    highest_price = 0.0
    stop_level = 0.0
    take_profit = 0.0

    capital = start_capital
    equity_curve = []
    trades = []

    for i in range(len(df)):
        row = df.iloc[i]
        price = float(row["Close"])
        sma20 = float(row["SMA20"])
        sma200 = float(row.get("SMA200", 0))
        atr = float(row["ATR"])
        rsi = float(row.get("RSI", 50))
        trend_score = row["trend_score"]
        risk_score = row["risk_score"]

        # Skip if indicators not ready
        if pd.isna(sma20) or pd.isna(atr) or pd.isna(sma200) or pd.isna(rsi):
            equity_curve.append(capital)
            continue

        # =====================
        # ENTRY
        # =====================
        if position == 0:
            # Improved entry condition aligned with signal_engine.py
            if trend_score > 65 and risk_score > 40 and price > sma200 and rsi > 45:
                position = 1
                entry_price = price
                highest_price = price

                # Initial levels
                risk_distance = k_atr * atr
                stop_level = entry_price - risk_distance
                take_profit = entry_price + (rr_ratio * risk_distance)

        # =====================
        # POSITION MANAGEMENT
        # =====================
        else:
            # Trailing Stop (Chandelier)
            highest_price = max(highest_price, price)
            current_stop = highest_price - (k_atr * atr)
            stop_level = max(stop_level, current_stop)

            # EXIT Conditions
            exit_reason = None
            if price <= stop_level:
                exit_reason = "STOP"
                exit_price = stop_level
            elif price >= take_profit:
                exit_reason = "TP"
                exit_price = take_profit

            if exit_reason:
                trade_return = (exit_price / entry_price) - 1
                capital *= (1 + trade_return)
                trades.append(trade_return)
                position = 0

        equity_curve.append(capital)

    # =========================
    # Metrics
    # =========================
    total_return = (capital / start_capital) - 1
    equity_series = pd.Series(equity_curve)

    running_max = equity_series.cummax()
    drawdown = (equity_series - running_max) / running_max
    max_drawdown = drawdown.min()

    profit_factor = 0
    win_rate = 0
    if len(trades) > 0:
        gains = [t for t in trades if t > 0]
        losses = [t for t in trades if t < 0]
        win_rate = len(gains) / len(trades)
        if len(losses) > 0:
            profit_factor = abs(sum(gains) / sum(losses))
        else:
            profit_factor = np.inf if sum(gains) > 0 else 0

    metrics = {
        "total_return": total_return,
        "max_drawdown": max_drawdown,
        "profit_factor": profit_factor,
        "win_rate": win_rate,
        "trade_count": len(trades)
    }

    if return_equity:
        return equity_series, metrics
    else:
        return None, metrics
