import numpy as np
import yfinance as yf
import pandas as pd


def fetch_historical_data(ticker, start_date='2000-01-01', end_date=None):
    """
    Fetch historical stock data for a given ticker using yfinance.
    """
    if not end_date:
        end_date = pd.Timestamp.now().strftime('%Y-%m-%d')

    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data


def calculate_moving_averages(df, short_window=50, long_window=200):
    """
    Calculate short and long moving averages.
    """
    df['SMA50'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
    df['SMA200'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
    return df


def identify_crossovers(df, short_window=50, long_window=200):
    """
    Identify golden and death crossovers.
    Golden crossover: Short-term moving average crosses above long-term moving average.
    Death crossover: Short-term moving average crosses below long-term moving average.
    """
    crossovers = []
    df['Signal'] = 0  # 1 for Golden Crossover, -1 for Death Crossover

    # Calculate signals where moving average conditions are met
    df['Signal'][short_window:] = np.where(df['SMA50'][short_window:] > df['SMA200'][short_window:], 1, 0)
    df['Crossover'] = df['Signal'].diff()

    # Identify golden and death crossovers
    golden_cross = df[df['Crossover'] == 1]
    death_cross = df[df['Crossover'] == -1]

    for _, row in golden_cross.iterrows():
        crossovers.append({
            'date': row.name,
            'type': 'Golden Crossover'
        })

    for _, row in death_cross.iterrows():
        crossovers.append({
            'date': row.name,
            'type': 'Death Crossover'
        })

    return crossovers

