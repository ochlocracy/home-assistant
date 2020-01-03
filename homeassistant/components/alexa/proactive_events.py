"""Alexa models."""
import logging
from uuid import uuid4

from .const import (
    API_BODY,
    API_CONTEXT,
    API_DIRECTIVE,
    API_ENDPOINT,
    API_EVENT,
    API_HEADER,
    API_PAYLOAD,
    API_REQUEST,
    API_SCOPE,
)
from .entities import ENTITY_ADAPTERS
from .errors import AlexaInvalidEndpointError

_LOGGER = logging.getLogger(__name__)


class AlexaProactiveEvent:
    """Base class for Alexa proactive event notification."""

    event_name = None

    def __init__(self, payload=None):
        """Initialize the notification."""
        payload = payload or {}
        self._event = {API_EVENT: {"name": self.event_name, API_PAYLOAD: payload}}

    @property
    def name(self):
        """Return the name of this response."""
        return self._event[API_EVENT]["name"]

    @staticmethod
    def localized_attributes():
        """Returns the localized attributes."""
        return None

    def serialize(self):
        """Return response as a JSON-able data structure."""
        return self._event


class AlexaMessageAlert(AlexaProactiveEvent):
    """Message reminder proactive event."""

    event_name = "AMAZON.MessageAlert.Activated"

    def __init__(self, payload=None):
        """Initialize the notification."""
        payload = payload or {
            "state": {"status": "UNREAD", "freshness": "NEW"},
            "messageGroup": {
                "creator": {"name": "Andy"},
                "count": 5,
                "urgency": "URGENT",
            },
        }
        super().__init__(payload)


class AlexaWeatherAlert(AlexaProactiveEvent):
    """Weather alert proactive event."""

    event_name = "AMAZON.WeatherAlert.Activated"

    def __init__(self, payload=None):
        """Initialize the notification."""
        payload = payload or {
            "weatherAlert": {
                "source": "localizedattribute:source",
                "alertType": "TORNADO",
            }
        }
        super().__init__(payload)

    def localized_attributes(self):
        """Returns the localized attributes."""
        localized_attributes = [{"locale": "en-US", "source": "Example Weather Corp"}]
        return localized_attributes
