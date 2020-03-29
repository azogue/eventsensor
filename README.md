[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<br><a href="https://www.buymeacoffee.com/azogue" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-black.png" width="150px" height="35px" alt="Buy Me A Coffee" style="height: 35px !important;width: 150px !important;" ></a>

# Event sensor

Custom integration to create sensors that track, represent and store specific **events** in Home Assistant.

Created to assign HA entities for ZigBee switches that only generate events when pressed,
but could be useful in other scenarios where some specific event needs to be tracked.

## Installation

Place the `custom_components` folder in your configuration directory
(or add its contents to an existing `custom_components` folder).

## Configuration

Once installed add to your configuration the desired sensors like this one
(a [Hue tap switch](https://www2.meethue.com/en-us/p/hue-tap-switch/046677473365) integrated in HA via [deCONZ integration](https://www.home-assistant.io/integrations/deconz/))

```yaml
sensor:
  - platform: eventsensor
    name: Tap switch last press
    event: deconz_event
    event_data:
      unique_id: 00:00:00:00:00:45:51:23
    state: event
    state_map:
      34: 1_click
      16: 2_click
      17: 3_click
      18: 4_click
```

* Optionally filter events with key-value pairs inside the event data (like identifiers for item generating the event).
* Optionally define a `state_map` to define custom states from the raw event data value.

When some event that matches the filters is received, the sensor is updated:

```json
{
    "event_type": "deconz_event",
    "data": {
        "id": "hue_tap_switch_1",
        "unique_id": "00:00:00:00:00:45:51:23",
        "event": 16
    },
    "origin": "LOCAL",
    "time_fired": "2020-03-28T18:23:58.439746+00:00",
    "context": {
        "id": "298225779b1c42e7989eff0a62a4a34c",
        "parent_id": null,
        "user_id": null
    }
}
```

Making the sensor state equal to "2_click".

#### Sensor Configuration

key | optional | type | default | description
-- | -- | -- | -- | --
`name` | False | string | | Name for the event sensor
`event` | False | string | | Name of the event to track.
`event_data` | True | dict | Empty (all events) | A dict with key-value pairs required in the event data, to filter specific events.
`state` | False | string | | Event data key used for the sensor state.
`state_map` | True | map | | State conversion from raw data in event to desired state.

## TODO

- [ ] [HACS](https://hacs.xyz/) integration.
- [ ] Config flow to define these sensors via UI, so it could be used easily for debug purposes without any HA restart.
- [ ] Better docs
