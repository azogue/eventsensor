# Changelog

## [v3.2.0](https://github.com/azogue/eventsensor/tree/v3.2.0) (2023-05-13)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v3.1.0...v3.2.0)

**Changes:**
- 🐛 Fix integration missing in GUI (#54) (because of `integration_type: entity`?), and update keys in HACS file
- ♻️ Update code to follow recent HA guidelines
- 🎨 Use ruff in pre-commit instead of flake8
- 📦️ Bump version and require recent HA-Core (>= 2023.5.0), deprecating python3.9 and earlier HA-Core versions

## [v3.1.0](https://github.com/azogue/eventsensor/tree/v3.1.0) (2023-03-12)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v3.0.0...v3.1.0)

**Changes:**

- Sort `manifest.json` keys and declare `integration_type=entity`
- Update pre-commit config and apply lint fixes
- Require Home Assistant Core >= 2022.12.0

## [v3.0.0](https://github.com/azogue/eventsensor/tree/v3.0.0) (2021-12-20)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v2.4.2...v3.0.0)

**Changes:**

- Use **multiple event data keys** to compose the sensor state, to support latest Hue v2 events (using `type,subtype` as 'event field', to generate sensor states like 'initial_press-1', 'long_release-2', etc.)
- Add **new state mapping presets** for Hue Dimmer Switch and Hue Button working with new Hue Api v2
- Require Home Assistant Core >= 2021.12.0 and Python >=3.9

## [v2.4.2](https://github.com/azogue/eventsensor/tree/v2.4.2) (2021-05-08)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v2.4.1...v2.4.2)

**Changes:**

- Add "iot_class" to integration manifest
- Fix scenario when extracted state is a list, by _flattening_ the complex object into a composed string.

## [v2.4.1](https://github.com/azogue/eventsensor/tree/v2.4.1) (2021-03-07)

[Full Changelog](https://github.com/azogue/eventsensor/compare/v2.2.0...v2.4.1)

**Changes:**

- Disable listening to EVENT_STATE_CHANGED even with manual YAML.
- Add version tag to hacs.json & manifest.json.
- Share event listeners for multiple sensors, and dispatch all event filters for each sensor derived from a specific event.
- Parse boolean values in event data, so "true"/"false" are processed as expected.
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
