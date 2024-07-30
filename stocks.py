import yfinance as yf
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

# Google Sheets API setup
GOOGLE_SHEET_ID = '1CygVpwAgbSw25BfIp9pd82muUAuJBayEDK3_CNRVbAo'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'stocks-431012-2f3db59ae662.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


def fetch_historical_data(ticker, start_date='2000-01-01', end_date=None):
    """
    Fetch historical stock data for a given ticker using yfinance.
    """
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data


def find_highest_volume(df):
    """
    Calculate the highest trading volume and the corresponding date.
    """
    highest_volume = df['Volume'].max()
    highest_volume_date = df[df['Volume'] == highest_volume].index[0]

    return highest_volume, highest_volume_date


def update_google_sheet(ticker, highest_volume, highest_volume_date):
    """
    Update the Google Sheet with the highest volume data for the given stock.
    """
    range_ = 'Sheet1!A:C'
    value_input_option = 'USER_ENTERED'
    values = [[ticker, highest_volume_date.strftime('%Y-%m-%d'), int(highest_volume)]]
    body = {'values': values}

    result = sheet.values().append(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=range_,
        valueInputOption=value_input_option,
        body=body
    ).execute()
    print(f'{result.get("updates").get("updatedCells")} cells updated.')


def fetch_large_cap_stocks(min_market_cap=50):
    """
    Fetch a list of stocks with a market cap exceeding the specified minimum (in billions).
    """
    # This is a sample list; you can replace it with dynamic fetching using a reliable API or database.
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NVDA', 'BRK-B', 'V', 'JPM']
    large_cap_stocks = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            market_cap = stock.info.get('marketCap', 0)
            market_cap_billion = market_cap / 1e9  # Convert to billions
            if market_cap_billion >= min_market_cap:
                large_cap_stocks.append(ticker)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    return large_cap_stocks


def main():
    stocks = fetch_large_cap_stocks(50)  # Fetch large-cap stocks
    for stock in stocks:
        df = fetch_historical_data(stock)
        highest_volume, highest_volume_date = find_highest_volume(df)
        update_google_sheet(stock, highest_volume, highest_volume_date)
        print(f"Stock: {stock}, Date: {highest_volume_date.strftime('%Y-%m-%d')}, Volume: {highest_volume}")


if __name__ == '__main__':
    main()
