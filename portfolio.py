import pandas as pd
import numpy as np

def position_sizing(signals, max_position_size):
    n_assets = len(signals.columns)
    weights = signals.copy()
    for date in signals.index:
        active = signals.loc[date].abs().sum()
        if active == 0:
            weights.loc[date] = 0
        else:
            weights.loc[date] = signals.loc[date] * (max_position_size / active)
    return weights

if __name__ == "__main__":
    import signals as sig
    import data_loader
    config = data_loader.load_config()
    data = data_loader.fetch_data(config['assets'], config['start_date'], config['end_date'])
    data = data_loader.preprocess_data(data)
    zscores = sig.compute_zscore(data, config['lookback_window'])
    signals = sig.generate_signals(zscores, config['entry_zscore'], config['exit_zscore'])
    weights = position_sizing(signals, config['max_position_size'])
    print(weights.tail())
