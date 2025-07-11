"""
main.py - Multi-Asset Mean Reversion Quant Trading Pipeline

This script runs the full quant trading pipeline:
- Loads config and validates parameters
- Fetches and preprocesses data
- Computes signals and weights
- Runs backtest and calculates metrics
- Generates plots and exports results

Author: Neil Chandran
Date: 2025-07-10
"""

import argparse
import sys
import os
import logging
import datetime
import yaml
import pandas as pd
import numpy as np

import data_loader
import signals as sig
import portfolio as pf
import backtester as bt
import metrics as mt
import visualization as vz

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-Asset Mean Reversion Quant Trading Pipeline"
    )
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Path to configuration YAML file')
    parser.add_argument('--start_date', type=str, help='Override start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, help='Override end date (YYYY-MM-DD)')
    parser.add_argument('--assets', type=str, nargs='+', help='Override asset list')
    parser.add_argument('--plot', action='store_true', help='Show plots interactively')
    parser.add_argument('--export', type=str, default='', help='Export results to CSV (provide filename)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    return parser.parse_args()

def validate_config(config):
    required_keys = [
        'assets', 'start_date', 'end_date', 'initial_capital',
        'lookback_window', 'entry_zscore', 'exit_zscore',
        'max_position_size', 'transaction_cost'
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    # Additional validation
    assert isinstance(config['assets'], list) and len(config['assets']) > 0, "Assets list must not be empty."
    assert config['initial_capital'] > 0, "Initial capital must be positive."
    assert config['lookback_window'] > 0, "Lookback window must be positive."
    assert config['max_position_size'] > 0 and config['max_position_size'] <= 1, "max_position_size must be in (0, 1]."
    assert 0 <= config['transaction_cost'] < 0.01, "Transaction cost should be reasonable (0 <= x < 0.01)."
    logging.info("Config validated successfully.")

def apply_overrides(config, args):
    if args.start_date:
        config['start_date'] = args.start_date
    if args.end_date:
        config['end_date'] = args.end_date
    if args.assets:
        config['assets'] = args.assets
    return config

def print_config_summary(config):
    logging.info("Configuration Summary:")
    for k, v in config.items():
        logging.info(f"  {k}: {v}")

def print_data_summary(data):
    logging.info("Data Summary:")
    logging.info(f"  Shape: {data.shape}")
    logging.info(f"  Date Range: {data.index.min().date()} to {data.index.max().date()}")
    logging.info(f"  Assets: {list(data.columns)}")
    logging.info(f"  Head:\n{data.head()}")

def print_signals_summary(signals):
    logging.info("Signals Summary:")
    logging.info(f"  Unique signal values: {signals.stack().unique()}")
    logging.info(f"  Non-zero signals per asset:\n{signals.abs().sum()}")
    logging.info(f"  Head:\n{signals.head()}")

def print_weights_summary(weights):
    logging.info("Weights Summary:")
    logging.info(f"  Max abs weight per asset:\n{weights.abs().max()}")
    logging.info(f"  Head:\n{weights.head()}")

def print_backtest_summary(equity_curve, net_returns, turnover):
    logging.info("Backtest Summary:")
    logging.info(f"  Final portfolio value: {equity_curve.iloc[-1]:,.2f}")
    logging.info(f"  Total return: {100 * (equity_curve.iloc[-1] / equity_curve.iloc[0] - 1):.2f}%")
    logging.info(f"  Mean daily return: {net_returns.mean():.5f}")
    logging.info(f"  Std daily return: {net_returns.std():.5f}")
    logging.info(f"  Average daily turnover: {turnover.mean():.5f}")

def print_metrics_summary(net_returns, equity_curve):
    sharpe = mt.sharpe_ratio(net_returns)
    max_dd = mt.max_drawdown(equity_curve)
    win = mt.win_rate(net_returns)
    logging.info("Performance Metrics:")
    logging.info(f"  Sharpe Ratio: {sharpe:.3f}")
    logging.info(f"  Max Drawdown: {100 * max_dd:.2f}%")
    logging.info(f"  Win Rate: {100 * win:.2f}%")

def export_results(equity_curve, net_returns, turnover, filename):
    df = pd.DataFrame({
        'equity_curve': equity_curve,
        'net_returns': net_returns,
        'turnover': turnover
    })
    df.to_csv(filename)
    logging.info(f"Results exported to {filename}")

def run_pipeline(config, show_plots=False, export_file=''):
    # Step 1: Load and preprocess data
    data = data_loader.fetch_data(config['assets'], config['start_date'], config['end_date'])
    data = data_loader.preprocess_data(data)
    print_data_summary(data)

    # Step 2: Compute z-score signals
    zscores = sig.compute_zscore(data, config['lookback_window'])
    signals = sig.generate_signals(zscores, config['entry_zscore'], config['exit_zscore'])
    print_signals_summary(signals)

    # Step 3: Portfolio weights
    weights = pf.position_sizing(signals, config['max_position_size'])
    print_weights_summary(weights)

    # Step 4: Backtest
    equity_curve, net_returns, turnover = bt.backtest(
        data, weights, config['initial_capital'], config['transaction_cost']
    )
    print_backtest_summary(equity_curve, net_returns, turnover)

    # Step 5: Metrics
    print_metrics_summary(net_returns, equity_curve)

    # Step 6: Visualization
    if show_plots:
        vz.plot_equity_curve(equity_curve)
        vz.plot_drawdown(equity_curve)
        vz.plot_signal_heatmap(signals)

    # Step 7: Export
    if export_file:
        export_results(equity_curve, net_returns, turnover, export_file)

    # Step 8: Report summary
    logging.info("Pipeline completed successfully.")

def interactive_menu():
    print("="*50)
    print("Quant Trading Pipeline - Interactive Menu")
    print("="*50)
    print("1. Run with default config")
    print("2. Run with custom dates")
    print("3. Run with custom asset list")
    print("4. Run with plotting")
    print("5. Export results to CSV")
    print("6. Exit")
    choice = input("Select an option (1-6): ")
    return choice

def main():
    args = parse_args()
    # Load config
    config = data_loader.load_config(args.config)
    config = apply_overrides(config, args)
    validate_config(config)
    print_config_summary(config)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Interactive menu if no CLI args
    if len(sys.argv) == 1:
        while True:
            choice = interactive_menu()
            if choice == '1':
                run_pipeline(config)
            elif choice == '2':
                sd = input("Enter start date (YYYY-MM-DD): ")
                ed = input("Enter end date (YYYY-MM-DD): ")
                config['start_date'] = sd
                config['end_date'] = ed
                run_pipeline(config)
            elif choice == '3':
                assets = input("Enter comma-separated asset tickers: ").split(',')
                config['assets'] = [a.strip().upper() for a in assets]
                run_pipeline(config)
            elif choice == '4':
                run_pipeline(config, show_plots=True)
            elif choice == '5':
                fname = input("Enter export filename (e.g. results.csv): ")
                run_pipeline(config, export_file=fname)
            elif choice == '6':
                print("Exiting.")
                break
            else:
                print("Invalid choice. Try again.")
    else:
        run_pipeline(config, show_plots=args.plot, export_file=args.export)

    # Example extension: custom risk model or strategy
    # Uncomment and implement as needed
    # custom_strategy = CustomStrategy(params)
    # signals = custom_strategy.generate_signals(data)
    # weights = pf.position_sizing(signals, config['max_position_size'])
    # equity_curve, net_returns, turnover = bt.backtest(data, weights, config['initial_capital'], config['transaction_cost'])
    # print_metrics_summary(net_returns, equity_curve)

if __name__ == "__main__":
    main()

# --- End of main.py ---
