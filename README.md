# Multi-Asset-Mean-Reversion-Strategy

## Overview

This project implements a **multi-asset mean reversion trading strategy** with a robust, extensible backtesting and reporting framework. It is designed for consulting, quant trading research, and as a showcase of best practices in systematic trading development.

The pipeline covers the full quant workflow:
- Data acquisition and preprocessing
- Signal generation using z-score mean reversion logic
- Portfolio construction with risk management
- Backtesting with transaction cost modeling
- Performance metrics and visualization
- Configurable via YAML and command-line interface

---

## Features

- **Multi-Asset Support:** Easily select any number of assets (stocks, ETFs, etc.) for simultaneous trading.
- **Configurable Strategy:** All key parameters (lookback window, z-score thresholds, position sizing, etc.) are set in a single YAML config file.
- **Modular Codebase:** Each step (data, signals, portfolio, backtest, metrics, visualization) is a separate, reusable module.
- **Robust Backtesting:** Realistic simulation with transaction costs, turnover, and daily rebalancing.
- **Comprehensive Reporting:** Sharpe ratio, drawdown, win rate, and more, with clear logging and summary output.
- **Visualization:** Interactive equity curve, drawdown, and signal heatmap plots.
- **CLI and Interactive Menu:** Run from the command line with overrides, or use the built-in interactive menu.
- **Export Options:** Save results to CSV for further analysis or presentation.

---

## Project Structure

.
├── main.py
├── config.yaml
├── data_loader.py
├── signals.py
├── portfolio.py
├── backtester.py
├── metrics.py
├── visualization.py
├── requirements.txt
└── README.md


---

## Quick Start

### 1. Clone the repository

git clone https://github.com/yourusername/mean-reversion-quant-pipeline.git
cd mean-reversion-quant-pipeline


### 2. Install dependencies

pip install -r requirements.txt


### 3. Configure your strategy

Edit `config.yaml` to set your assets, dates, and strategy parameters.

### 4. Run the pipeline

python main.py --plot


Or, for interactive mode (no arguments):

python main.py


### 5. Export results

python main.py --export results.csv


---

## Configuration

All parameters are set in `config.yaml`:

assets: AAPL, MSFT, 
GOOG
start_date: '2018-01-01'
end_date: '2023-01-01'
initial_capital: 100000
lookback_window: 20
entry_zscore: 1.0
exit_zscore: 0.5
max_position_size: 0.2
transaction_cost: 0.0005

Override any parameter via command line, e.g.:

python main.py --assets TSLA NVDA --start_date 2020-01-01 --end_date 2023-01-01


---

## Outputs

- **Performance metrics:** Sharpe ratio, max drawdown, win rate, turnover
- **Plots:** Equity curve, drawdown chart, signal heatmap
- **CSV export:** Equity curve, returns, turnover by date

---

## Extending the Project

- Add new signal generation logic in `signals.py`
- Implement custom risk models or overlays in `portfolio.py`
- Integrate additional data sources in `data_loader.py`
- Batch run for parameter optimization

---

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies:
  - yfinance
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - pyyaml

**Happy trading!**

