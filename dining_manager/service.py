import math

from .config import ConfigManager
from .events import QueueSubject


def estimate_wait_seconds(queue_length, avg_service_seconds=20, counters_open=2):
    """Estimated wait for a new person joining the queue."""
    if queue_length < 0:
        raise ValueError("queue_length cannot be negative")
    if avg_service_seconds <= 0:
        raise ValueError("avg_service_seconds must be positive")
    if counters_open < 1:
        raise ValueError("at least one counter must be open")
    return (queue_length * avg_service_seconds) / counters_open


def validate_ticket(meals_taken_today, meal_limit):
    """True if the person may still take a meal today."""
    if meals_taken_today < 0:
        raise ValueError("meals_taken_today cannot be negative")
    return meals_taken_today < meal_limit


def forecast_portions(past_attendance, buffer_percent=10):
    """Average past attendance plus a safety buffer, rounded up."""
    if not past_attendance:
        raise ValueError("past_attendance cannot be empty")
    if any(a < 0 for a in past_attendance):
        raise ValueError("attendance values cannot be negative")
    avg = sum(past_attendance) / len(past_attendance)
    portions = avg * (1 + buffer_percent / 100)
    return math.ceil(portions)  # round first: 100*1.1 = 110.00000000000001


class DiningService:
    """AFTER refactoring: clean service using Singleton, Factory (users) and Observer."""

    def __init__(self, hall):
        self.hall = hall
        self.config = ConfigManager()
        self.queue = []
        self.taken = {}
        self.events = QueueSubject()

    def join_queue(self, user):
        if not validate_ticket(self.taken.get(user.user_id, 0), user.meal_limit):
            return "no more meals"
        self.taken[user.user_id] = self.taken.get(user.user_id, 0) + 1
        self.queue.append(user.user_id)
        self.events.notify(len(self.queue))
        return "ok"
