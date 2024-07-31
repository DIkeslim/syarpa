import pusher
import json

# Initialize Pusher
pusher_client = pusher.Pusher(
    app_id='1842229',
    key='6b6d47b4380aea6e6cb1',
    secret='c1ab10572596bd24d516',
    cluster='mt1',
    ssl=True
)


def send_alert(crossover):
    """
    Send an alert via Pusher.
    """
    channel = 'stock-alerts'
    message = {
        'stock': crossover['stock'],
        'date': crossover['date'].strftime('%Y-%m-%d'),
        'type': crossover['type']
    }

    pusher_client.trigger(channel, 'crossover_event', message)
    print(f"Alert sent: {message}")


if __name__ == "__main__":
    # Example usage
    test_crossover = {
        'date': '2024-07-30',
        'type': 'Golden Crossover'
    }
    send_alert(test_crossover)
