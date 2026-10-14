class ConfigManager:
    """Singleton: one shared copy of dining hall settings."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {
                "avg_service_seconds": 20,
                "counters_open": 2,
                "queue_alert_threshold": 50,
            }
        return cls._instance

    def get(self, key):
        return self.settings[key]

    def set(self, key, value):
        self.settings[key] = value
