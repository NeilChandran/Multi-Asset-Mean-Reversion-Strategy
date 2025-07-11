import pandas as pd
import numpy as np

def backtest(prices, weights, initial_capital, transaction_cost):
    daily_returns = prices.pct_change().fillna(0)
    portfolio_returns = (weights.shift(1) * daily_returns).sum(axis=1)
    turnover = (weights.diff().abs()).sum(axis=1)
    costs = turnover * transaction_cost
    net_returns = portfolio_returns - costs
    equity_curve = (1 + net_returns).cumprod() * initial_capital
    return equity_curve, net_returns, turnover

if __name__ == "__main__":
    import data_loader
    import signals as sig
    import portfolio as pf
    config = data_loader.load_config()
    data = data_loader.fetch_data(config['assets'], config['start_date'], config['end_date'])
    data = data_loader.preprocess_data(data)
    zscores = sig.compute_zscore(data, config['lookback_window'])
    signals = sig.generate_signals(zscores, config['entry_zscore'], config['exit_zscore'])
    weights = pf.position_sizing(signals, config['max_position_size'])
    eq, net_ret, turnover = backtest(data, weights, config['initial_capital'], config['transaction_cost'])
    print(eq.tail())
