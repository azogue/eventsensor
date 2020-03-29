"""Event sensor."""
import logging

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_EVENT,
    CONF_EVENT_DATA,
    CONF_NAME,
    CONF_STATE,
)
from homeassistant.core import callback
from homeassistant.helpers.config_validation import string
from homeassistant.helpers.event import Event
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import slugify

_LOGGER = logging.getLogger(__name__)

CONF_STATE_MAP = "state_map"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): string,
        vol.Required(CONF_STATE): string,
        vol.Required(CONF_EVENT): string,
        vol.Optional(CONF_EVENT_DATA): dict,
        vol.Optional(CONF_STATE_MAP): dict,
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):
    """Set up event sensors platform."""
    async_add_entities(
        [
            EventSensor(
                name=config.get(CONF_NAME),
                event=config.get(CONF_EVENT),
                event_data=config.get(CONF_EVENT_DATA, {}),
                state=config.get(CONF_STATE),
                state_map=config.get(CONF_STATE_MAP, {}),
            )
        ],
        False,
    )


class EventSensor(RestoreEntity):
    """Sensor to store information originated with events."""

    should_poll = False

    def __init__(
        self,
        name: str,
        event: str,
        event_data: dict,
        state: str,
        state_map: dict,
    ):
        self._event = event
        self._event_data: dict = event_data
        self._name = name
        self._unique_id = "_".join(
            [event, slugify(str(event_data)), state, slugify(str(state_map))]
        )
        self._event_listener = None
        self._state = None
        self._attributes = {}
        self._state_key = state
        self._state_map = state_map

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID, made with the event name and data filters."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_added_to_hass(self) -> None:
        """Add event listener when adding entity to Home Assistant."""
        # Recover last state
        last_state = await self.async_get_last_state()
        if last_state is not None:
            self._state = last_state.state
            self._attributes = dict(last_state.attributes)

        @callback
        def async_update_sensor(event: Event):
            """Update state when event is received."""
            _LOGGER.debug("%s: Event received -> %s", self.entity_id, event)
            if self._event_data.items() < event.data.items():
                new_state = event.data[self._state_key]
                if new_state in self._state_map:
                    new_state = self._state_map[new_state]

                self._state = new_state
                self._attributes = {
                    **event.data,
                    "origin": event.origin.name,
                    "time_fired": event.time_fired,
                }
                _LOGGER.debug("%s: New state: %s", self.entity_id, self._state)
                self.async_write_ha_state()

        # Listen for event
        self._event_listener = self.hass.bus.async_listen(
            self._event, async_update_sensor
        )

    async def async_will_remove_from_hass(self):
        """Remove listeners when removing entity from Home Assistant."""
        if self._event_listener is not None:
            self._event_listener()
            self._event_listener = None
