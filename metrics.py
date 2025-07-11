import numpy as np

def sharpe_ratio(returns, risk_free_rate=0):
    excess = returns - risk_free_rate / 252
    return np.sqrt(252) * excess.mean() / excess.std()

def max_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = equity_curve / roll_max - 1.0
    return drawdown.min()

def win_rate(returns):
    return (returns > 0).mean()

if __name__ == "__main__":
    import data_loader
    import signals as sig
    import portfolio as pf
    import backtester as bt
    config = data_loader.load_config()
    data = data_loader.fetch_data(config['assets'], config['start_date'], config['end_date'])
    data = data_loader.preprocess_data(data)
    zscores = sig.compute_zscore(data, config['lookback_window'])
    signals = sig.generate_signals(zscores, config['entry_zscore'], config['exit_zscore'])
    weights = pf.position_sizing(signals, config['max_position_size'])
    eq, net_ret, turnover = bt.backtest(data, weights, config['initial_capital'], config['transaction_cost'])
    print("Sharpe:", sharpe_ratio(net_ret))
    print("Max DD:", max_drawdown(eq))
    print("Win Rate:", win_rate(net_ret))

