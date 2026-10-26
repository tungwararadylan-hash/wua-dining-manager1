import pytest
from dining_manager.service import (estimate_wait_seconds, validate_ticket,
                                    forecast_portions, DiningService)
from dining_manager.users import UserFactory, Student, Staff
from dining_manager.config import ConfigManager
from dining_manager.events import KitchenAlert, DisplayBoard


# --- estimate_wait_seconds ---
def test_wait_normal():
    assert estimate_wait_seconds(10, 20, 2) == 100

def test_wait_zero_queue():
    assert estimate_wait_seconds(0) == 0

def test_wait_large_queue():
    assert estimate_wait_seconds(1_000_000, 20, 2) == 10_000_000

def test_wait_negative_queue():
    with pytest.raises(ValueError):
        estimate_wait_seconds(-1)

def test_wait_no_counters():
    with pytest.raises(ValueError):
        estimate_wait_seconds(5, 20, 0)


# --- validate_ticket ---
def test_ticket_allowed():
    assert validate_ticket(1, 2) is True

def test_ticket_limit_reached():
    assert validate_ticket(2, 2) is False

def test_ticket_negative():
    with pytest.raises(ValueError):
        validate_ticket(-1, 2)


# --- forecast_portions ---
def test_forecast_basic():
    assert forecast_portions([100, 100, 100], 10) == 110

def test_forecast_rounds_up():
    assert forecast_portions([101], 10) == 112

def test_forecast_empty():
    with pytest.raises(ValueError):
        forecast_portions([])

def test_forecast_negative_value():
    with pytest.raises(ValueError):
        forecast_portions([10, -5])


# --- Factory / Singleton / Observer ---
def test_factory_creates_types():
    assert isinstance(UserFactory.create("student", "W1"), Student)
    assert isinstance(UserFactory.create("STAFF", "S1"), Staff)

def test_factory_unknown_role():
    with pytest.raises(ValueError):
        UserFactory.create("visitor", "X1")

def test_singleton_same_instance():
    assert ConfigManager() is ConfigManager()

def test_observer_notified_and_limit_enforced():
    svc = DiningService("Main Hall")
    board, alert = DisplayBoard(), KitchenAlert(threshold=1)
    svc.events.subscribe(board)
    svc.events.subscribe(alert)
    s1, s2 = UserFactory.create("student", "W1"), UserFactory.create("student", "W2")
    assert svc.join_queue(s1) == "ok"
    assert svc.join_queue(s2) == "ok"
    assert board.last_length == 2
    assert alert.alerts == ["ALERT: queue at 2"]
    staff = UserFactory.create("staff", "S1")
    svc.join_queue(staff)
    assert svc.join_queue(staff) == "no more meals"
