"""Event sensor integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.typing import HomeAssistantType

from .common import DOMAIN, DOMAIN_DATA

PLATFORMS: list[Platform] = [Platform.SENSOR]
CONFIG_SCHEMA = cv.removed(DOMAIN, raise_if_present=False)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up the component from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    # forward unload
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        # remove update listener
        hass.data[DOMAIN_DATA].pop(entry.entry_id)()

        # remove entity from registry
        entity_registry = er.async_get(hass)
        entity_registry.async_clear_config_entry(entry.entry_id)

    return unload_ok
