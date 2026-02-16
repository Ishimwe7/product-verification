import logging

class DummyEventDispatcher:
    def __init__(self):
        self.dispatched_events = [] # In-memory list for testing
        logging.basicConfig(level=logging.INFO)

    def dispatch(self, event):
        """
        Logs events to console and stores them in memory.
        """
        self.dispatched_events.append(event)
        logging.info(f"[DOMAIN EVENT]: {type(event).__name__} for ID {event.product_id}")