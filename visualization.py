import matplotlib.pyplot as plt
import seaborn as sns

def plot_equity_curve(equity_curve):
    plt.figure(figsize=(12,6))
    plt.plot(equity_curve)
    plt.title('Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.grid(True)
    plt.show()

def plot_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = equity_curve / roll_max - 1.0
    plt.figure(figsize=(12,4))
    plt.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
    plt.title('Drawdown')
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.grid(True)
    plt.show()

def plot_signal_heatmap(signals):
    plt.figure(figsize=(12,6))
    sns.heatmap(signals.T, cmap='RdBu', center=0)
    plt.title('Signal Heatmap')
    plt.xlabel('Date')
    plt.ylabel('Asset')
    plt.show()

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
    plot_equity_curve(eq)
    plot_drawdown(eq)
    plot_signal_heatmap(signals)
