class Event:
    def __init__(self, event):
        self._event = event

    @property
    def id(self):
        return self._event['message']['id']

    @property
    def event_type(self):
        return self._event['eventType']
