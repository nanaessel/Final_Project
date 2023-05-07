from typing import List

class MessageBus:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, handler, event_types):
        for event_type in event_types:
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            self.handlers[event_type].append(handler)

    def handle(self, message):
        event_handlers = self.handlers.get(type(message), [])
        for handler in event_handlers:
            handler.handle(message)

    def handle_command(self, command):
        events = command.handle()
        for event in events:
            self.handle(event)
