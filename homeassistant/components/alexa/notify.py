"""Support for Alexa Notification Service."""
import asyncio
import json
import logging

import aiohttp
import async_timeout

import homeassistant.util.dt as dt_util
from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    ATTR_TITLE,
    ATTR_TITLE_DEFAULT,
    SERVICE_NOTIFY,
    BaseNotificationService,
)

from .const import Cause
from .messages import AlexaResponse
from .smart_home_http import AlexaConfig


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_get_service(hass, config, discovery_info=None):
    """Get the Alexa notification service."""
    return AlexaNotificationService(hass)


class AlexaNotificationService(BaseNotificationService):
    """Implement the notification service for Alexa."""

    def __init__(self, hass):
        """Initialize the service."""
        self.hass = hass

    async def async_send_message(self, message="", **kwargs):
        """Send a message via Alexa notify."""
        _LOGGER.debug("Message: %s, kwargs: %s", message, kwargs)
        data = kwargs.get(ATTR_DATA)
        targets = kwargs.get(ATTR_TARGET)
        title = kwargs.get(ATTR_TITLE) if ATTR_TITLE in kwargs else ATTR_TITLE_DEFAULT
        data = kwargs.get(ATTR_DATA)
