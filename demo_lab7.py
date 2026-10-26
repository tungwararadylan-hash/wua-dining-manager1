"""Lab 7 demo: BEFORE (messy.py) vs AFTER (Singleton, Factory, Observer)."""
from dining_manager.messy import process
from dining_manager.config import ConfigManager
from dining_manager.users import UserFactory
from dining_manager.events import QueueSubject, KitchenAlert, DisplayBoard
from dining_manager.service import DiningService

print("=== BEFORE: messy.py ===")
queue, tickets = [], {}
print("Result:", process("student", "W1", "Main Hall", queue, "Lunch", tickets))
print("Result:", process("student", "W1", "Main Hall", queue, "Lunch", tickets))
print("Result:", process("student", "W1", "Main Hall", queue, "Lunch", tickets))

print("\n=== AFTER: Singleton ===")
print("Same settings object everywhere:", ConfigManager() is ConfigManager())

print("\n=== AFTER: Factory ===")
for role in ("student", "staff", "admin"):
    u = UserFactory.create(role, "X1")
    print(role, "->", type(u).__name__, "| meal limit:", u.meal_limit)

print("\n=== AFTER: Observer ===")
service = DiningService("Main Hall")
board, alert = DisplayBoard(), KitchenAlert(threshold=2)
service.events.subscribe(board)
service.events.subscribe(alert)
for i in range(1, 5):
    result = service.join_queue(UserFactory.create("student", f"W{i}"))
    print(f"W{i} joins:", result, "| board shows", board.last_length)
print("Kitchen alerts:", alert.alerts)
