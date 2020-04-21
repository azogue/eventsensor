"""Constants for eventsensor."""
from homeassistant.const import CONF_EVENT, CONF_EVENT_DATA, CONF_STATE
from homeassistant.util import slugify

# Base component constants
DOMAIN = "eventsensor"
PLATFORM = "sensor"
DOMAIN_DATA = f"{DOMAIN}_data"

CONF_STATE_MAP = "state_map"

PRESET_FOH = "FoH Switch"
PRESET_FOH_MAPPING = {
    16: "left_upper_press",
    20: "left_upper_release",
    17: "left_lower_press",
    21: "left_lower_release",
    18: "right_lower_press",
    22: "right_lower_release",
    19: "right_upper_press",
    23: "right_upper_release",
    100: "double_upper_press",
    101: "double_upper_release",
    98: "double_lower_press",
    99: "double_lower_release",
}
PRESET_HUE_DIMMER = "Hue Dimmer Switch"
PRESET_HUE_DIMMER_MAPPING = {
    1000: "1_click",
    2000: "2_click",
    3000: "3_click",
    4000: "4_click",
    1001: "1_hold",
    2001: "2_hold",
    3001: "3_hold",
    4001: "4_hold",
    1002: "1_click_up",
    2002: "2_click_up",
    3002: "3_click_up",
    4002: "4_click_up",
    1003: "1_hold_up",
    2003: "2_hold_up",
    3003: "3_hold_up",
    4003: "4_hold_up",
}
PRESET_HUE_TAP = "Hue Tap Switch"
PRESET_HUE_TAP_MAPPING = {
    34: "1_click",
    16: "2_click",
    17: "3_click",
    18: "4_click",
}


def make_unique_id(sensor_data: dict) -> str:
    """
    Generate an unique id from the listened event + data filters.

    Used for both the generated sensor entity and the config entry.
    """
    event: str = sensor_data.get(CONF_EVENT)
    state: str = sensor_data.get(CONF_STATE)
    filter_event: dict = dict(sensor_data.get(CONF_EVENT_DATA, {}))
    state_map: dict = dict(sensor_data.get(CONF_STATE_MAP, {}))
    return "_".join([event, slugify(str(filter_event)), state, slugify(str(state_map))])
