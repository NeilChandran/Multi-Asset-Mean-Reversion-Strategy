import pandas as pd

def compute_zscore(prices, window):
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()
    zscore = (prices - rolling_mean) / rolling_std
    return zscore

def generate_signals(zscores, entry_z, exit_z):
    signals = pd.DataFrame(index=zscores.index, columns=zscores.columns)
    positions = pd.DataFrame(0, index=zscores.index, columns=zscores.columns)
    for asset in zscores.columns:
        long = (zscores[asset] < -entry_z).astype(int)
        exit_long = (zscores[asset] > -exit_z).astype(int)
        short = (zscores[asset] > entry_z).astype(int)
        exit_short = (zscores[asset] < exit_z).astype(int)
        position = 0
        for i in range(len(zscores)):
            if position == 0:
                if long.iloc[i]:
                    position = 1
                elif short.iloc[i]:
                    position = -1
            elif position == 1:
                if exit_long.iloc[i]:
                    position = 0
            elif position == -1:
                if exit_short.iloc[i]:
                    position = 0
            positions.iloc[i][asset] = position
        signals[asset] = positions[asset]
    return signals

if __name__ == "__main__":
    import data_loader
    config = data_loader.load_config()
    data = data_loader.fetch_data(config['assets'], config['start_date'], config['end_date'])
    data = data_loader.preprocess_data(data)
    zscores = compute_zscore(data, config['lookback_window'])
    signals = generate_signals(zscores, config['entry_zscore'], config['exit_zscore'])
    print(signals.tail())
