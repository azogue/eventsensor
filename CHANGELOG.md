# Changelog

## [v2.4.0](https://github.com/azogue/eventsensor/tree/v2.4.0) (2021-03-07)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v2.3.0...v2.4.0)

**Changes:**

- Disable listening to EVENT_STATE_CHANGED even with manual YAML.
- Add version tag to hacs.json & manifest.json, and declare a zip release file.
- Share event listeners for multiple sensors, and dispatch all event filters for each sensor derived from a specific event.
- Parse boolean values in event data, so "true"/"false" are processed as expected.

## [v2.3.0](https://github.com/azogue/eventsensor/tree/v2.3.0) (2020-08-06)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v2.2.0...v2.3.0)

**Implemented enhancements:**

- Add default mapping templates for Philips Hue Smart Button.

## [v2.2.0](https://github.com/azogue/eventsensor/tree/v2.2.0) (2020-08-02)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v2.1.0...v2.2.0)

**Implemented enhancements:**

- Better filter of event_data, using `dot.notation` for nested keys.
- Add default mapping templates for Aqara Smart Button and Aqara Cube.

## [v2.1.0](https://github.com/azogue/eventsensor/tree/v2.1.0) (2020-04-29)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v2.0.0...v2.1.0)

**Changes:**

- Rename translations folder to follow HA Core changes for HA >= v0.109. (#6 from @tmcarr)
- Increase min HA version to 0.109
- Add Github Action to validate for HACS
- Add Github Action to validate for HA Core (with `hassfest`)

## [v2.0.0](https://github.com/azogue/eventsensor/tree/v2.0.0) (2020-04-22)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v1.0.0...v2.0.0)

**Implemented enhancements:**

- Add config entry support + full UI support with config flows.
- Support of nested attribute as sensor state, using dot notation.
- Support of nested dicts for better event filter.

## [v1.0.0](https://github.com/azogue/eventsensor/tree/v1.0.0) (2020-04-17)

**Initial version**
