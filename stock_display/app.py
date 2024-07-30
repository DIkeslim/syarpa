from flask import Flask, render_template, jsonify
from stock_analysis import fetch_historical_data, calculate_moving_averages, identify_crossovers
from alerts import send_alert

app = Flask(__name__)


@app.route('/')
def index():
    # Fetch and process stock data
    stocks = ['AAPL', 'MSFT', 'GOOGL']  # Add more stocks as needed
    results = []

    for stock in stocks:
        df = fetch_historical_data(stock)
        df = calculate_moving_averages(df)
        crossovers = identify_crossovers(df)

        for crossover in crossovers:
            crossover_data = {
                'stock': stock,
                'date': crossover['date'],
                'type': crossover['type']
            }
            results.append(crossover_data)
            # Send an alert for each crossover
            send_alert(crossover_data)

    return render_template('index.html', results=results)



@app.route('/api/alerts')
def api_alerts():
    # For API requests to get alerts
    stocks = ['AAPL', 'MSFT', 'GOOGL']  # Add more stocks as needed
    results = []

    for stock in stocks:
        df = fetch_historical_data(stock)
        df = calculate_moving_averages(df)
        crossovers = identify_crossovers(df)

        for crossover in crossovers:
            results.append({
                'stock': stock,
                'date': crossover['date'].strftime('%Y-%m-%d'),
                'type': crossover['type']
            })

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
