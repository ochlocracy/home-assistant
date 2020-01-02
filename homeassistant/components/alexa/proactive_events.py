"""Alexa proactive events code."""
import asyncio
import json
import logging

import aiohttp
import async_timeout

from homeassistant.const import MATCH_ALL, STATE_ON
import homeassistant.util.dt as dt_util

from .const import API_CHANGE, Cause
from .entities import ENTITY_ADAPTERS
from .messages import AlexaResponse

_LOGGER = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 10


async def async_send_proactive_event_message(
    hass, config, alexa_entity, *, invalidate_access_token=True
):
    """Send a proavtive event.

    https://developer.amazon.com/en-US/docs/alexa/smapi/proactive-events-api.html
    """
    token = await config.async_get_access_token()

    headers = {"Authorization": f"Bearer {token}"}

    payload = {}

    message = AlexaResponse(name="ChangeReport", namespace="Alexa", payload=payload)
    message.set_endpoint_full(token, endpoint)

    message_serialized = message.serialize()
    session = hass.helpers.aiohttp_client.async_get_clientsession()

    try:
        with async_timeout.timeout(DEFAULT_TIMEOUT):
            response = await session.post(
                config.endpoint,
                headers=headers,
                json=message_serialized,
                allow_redirects=True,
            )

    except (asyncio.TimeoutError, aiohttp.ClientError):
        _LOGGER.error("Timeout sending report to Alexa.")
        return

    response_text = await response.text()

    _LOGGER.debug("Sent: %s", json.dumps(message_serialized))
    _LOGGER.debug("Received (%s): %s", response.status, response_text)

    if response.status == 202:
        return

    response_json = json.loads(response_text)

    if (
        response_json["payload"]["code"] == "INVALID_ACCESS_TOKEN_EXCEPTION"
        and not invalidate_access_token
    ):
        config.async_invalidate_access_token()
        return await async_send_changereport_message(
            hass, config, alexa_entity, invalidate_access_token=False
        )

    _LOGGER.error(
        "Error when sending ChangeReport to Alexa: %s: %s",
        response_json["payload"]["code"],
        response_json["payload"]["description"],
    )
