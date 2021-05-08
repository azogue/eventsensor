"""Event sensor."""
import logging
from typing import Any, Callable, Dict, List

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.const import (
    CONF_EVENT,
    CONF_EVENT_DATA,
    CONF_NAME,
    CONF_STATE,
    EVENT_STATE_CHANGED,
)
from homeassistant.core import callback
from homeassistant.helpers.config_validation import string
from homeassistant.helpers.event import Event
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from .common import (
    CONF_STATE_MAP,
    DOMAIN,
    DOMAIN_DATA,
    check_dict_is_contained_in_another,
    extract_state_from_event,
    make_unique_id,
    parse_numbers,
)

_LOGGER = logging.getLogger(__name__)

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
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable[[List[Any], bool], None],
    discovery_info: DiscoveryInfoType = None,
):
    """
    Set up event sensors from configuration.yaml as a sensor platform.

    Left just to read deprecated manual configuration.
    """
    if config and config.get(CONF_EVENT) != EVENT_STATE_CHANGED:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, data=config, context={"source": SOURCE_IMPORT}
            )
        )
        _LOGGER.warning(
            "Manual yaml config is deprecated. "
            "You can remove it now, as it has been migrated to config entry, "
            "handled in the Integrations menu [Sensor %s, event: %s]",
            config.get(CONF_NAME),
            config.get(CONF_EVENT),
        )

    elif config and config.get(CONF_EVENT) == EVENT_STATE_CHANGED:
        _LOGGER.error(
            "Listen to the `%s` event is forbidden, "
            "so the EventSensor '%s' won't be created :(",
            EVENT_STATE_CHANGED,
            config.get(CONF_NAME),
        )

    return True


async def async_setup_entry(
    hass: HomeAssistantType,
    config_entry: ConfigEntry,
    async_add_entities: Callable[[List[Any], bool], None],
):
    """Set up the component sensors from a config entry."""
    if DOMAIN_DATA not in hass.data:
        hass.data[DOMAIN_DATA] = {}

    if "_dispatcher" not in hass.data[DOMAIN_DATA]:
        hass.data[DOMAIN_DATA]["_dispatcher"] = EventSensorDispatcher()

    async_add_entities(
        [
            EventSensor(
                config_entry.entry_id,
                config_entry.unique_id,
                config_entry.data,
                hass.data[DOMAIN_DATA]["_dispatcher"],
            )
        ],
        False,
    )

    # add an update listener to enable edition by OptionsFlow
    hass.data[DOMAIN_DATA][config_entry.entry_id] = config_entry.add_update_listener(
        update_listener
    )


async def update_listener(hass: HomeAssistantType, entry: ConfigEntry):
    """Update when config_entry options update."""
    changes = len(entry.options) > 1 and entry.data != entry.options
    if changes:
        # update entry replacing data with new options, and updating unique_id and title
        _LOGGER.debug(
            f"Config entry update with {entry.options} and unique_id:{entry.unique_id}"
        )
        hass.config_entries.async_update_entry(
            entry,
            title=entry.options[CONF_NAME],
            data=entry.options,
            options={},
            unique_id=make_unique_id(entry.options),
        )
        hass.async_create_task(hass.config_entries.async_reload(entry.entry_id))


class EventSensorDispatcher:
    """Dispatcher for EventSensors."""

    def __init__(self):
        """Set up the event sensor dispatcher."""
        self._listeners: Dict[str, Callable[[], None]] = {}
        self._filters: Dict[str, Dict[str, Any]] = {}

    async def async_add_entry(
        self,
        hass: HomeAssistantType,
        entry_id: str,
        event_type: str,
        event_data_filter: Dict[str, Any],
        callback_update_sensor: Callable[[Event], None],
    ) -> None:
        """Add event listener when adding entity to Home Assistant."""
        if event_type not in self._filters:
            # requires a new listener
            self._filters[event_type] = {}

        assert entry_id not in self._filters[event_type]
        self._filters[event_type][entry_id] = (
            event_data_filter,
            callback_update_sensor,
        )

        @callback
        def async_dispatch_by_event_type(event: Event):
            """Dispatch sensor updates when event is received."""
            for ev_filter, cb_sensor in self._filters[event.event_type].values():
                if check_dict_is_contained_in_another(ev_filter, event.data):
                    cb_sensor(event)

        if event_type not in self._listeners:
            # requires a new listener
            self._listeners[event_type] = hass.bus.async_listen(
                event_type, async_dispatch_by_event_type
            )
            _LOGGER.info("Added event listener for '%s'", event_type)

    async def async_remove_entry(self, event_type: str, entry_id: str):
        """Remove listeners when removing entity from Home Assistant."""
        assert event_type in self._filters
        assert entry_id in self._filters[event_type]
        self._filters[event_type].pop(entry_id)
        if not self._filters[event_type]:
            self._filters.pop(event_type)
            assert event_type in self._listeners
            self._listeners.pop(event_type)()
            _LOGGER.debug("Removed event listener for '%s'", event_type)


class EventSensor(RestoreEntity):
    """Sensor to store information originated with events."""

    should_poll = False
    icon = "mdi:bullseye-arrow"

    def __init__(
        self,
        entry_id: str,
        unique_id: str,
        sensor_data: Dict[str, Any],
        dispatcher: EventSensorDispatcher,
    ):
        """Set up a new sensor mirroring some event."""
        self._dispatcher = dispatcher
        self._entry_id = entry_id
        self._unique_id = unique_id
        self._name = sensor_data[CONF_NAME]
        self._event = sensor_data[CONF_EVENT]
        self._state_key = sensor_data[CONF_STATE]
        self._event_data = parse_numbers(sensor_data.get(CONF_EVENT_DATA, {}))
        self._state_map = parse_numbers(sensor_data.get(CONF_STATE_MAP, {}))
        self._state = None
        self._attributes: Dict[str, Any] = {}

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
            """Update state when a valid event is received."""
            # Extract new state
            new_state = extract_state_from_event(self._state_key, event.data)

            # Apply custom state mapping
            if self._state_map and new_state in self._state_map:
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
        await self._dispatcher.async_add_entry(
            self.hass,
            self._entry_id,
            self._event,
            self._event_data,
            async_update_sensor,
        )
        _LOGGER.info(
            "%s: Added sensor listening to '%s' with event data: %s",
            self.entity_id,
            self._event,
            self._event_data,
        )

    async def async_will_remove_from_hass(self):
        """Remove listeners when removing entity from Home Assistant."""
        await self._dispatcher.async_remove_entry(self._event, self._entry_id)
        _LOGGER.info("%s: Removed event listener", self.entity_id)
