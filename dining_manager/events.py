class QueueSubject:
    """Observer pattern: subject that notifies subscribed observers."""

    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def notify(self, queue_length):
        for obs in self._observers:
            obs.update(queue_length)


class KitchenAlert:
    def __init__(self, threshold):
        self.threshold = threshold
        self.alerts = []

    def update(self, queue_length):
        if queue_length > self.threshold:
            self.alerts.append(f"ALERT: queue at {queue_length}")


class DisplayBoard:
    def __init__(self):
        self.last_length = 0

    def update(self, queue_length):
        self.last_length = queue_length
