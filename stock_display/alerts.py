import pusher
import json

# Initialize Pusher
pusher_client = pusher.Pusher(
    
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
