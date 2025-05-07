# Imeon Inverter Home Assistant Custom Integration

> **Legacy integration, please use the official one available since Home Assistant 2025.5.**
> This custom integration in deprecated and no longer maintained, prefer use the official one directly in [Home Assistant](https://my.home-assistant.io/redirect/config_flow_start/?domain=imeon_inverter).

[![Website](https://img.shields.io/badge/-Imeon%20Energy-%2520?style=flat&label=Website&labelColor=grey&color=black)](https://imeon-energy.com/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-44cc11.svg)](https://www.apache.org/licenses/LICENSE-2.0)

This repository contains a custom integration for Home Assistant to support Imeon Inverters. The integration allows for local polling of the inverter data and provides a hub for managing your solar energy system.

**Please take a look at [extra ressources](https://github.com/Imeon-Inverters-for-Home-Assistant/imeon-integration-extras) for custom dashboards for this integration**.

## Requirements

- Home Assistant version that supports custom integrations.
- Python package: `imeon_inverter_api`

## Installation

To install the Imeon Inverter integration, follow these steps:

1. **Download the Integration:**
   - Clone or download this repository to your Home Assistant `custom_components` directory.

2. **Install Requirements:**
   - There should be none, as Home Assistant will ensure the following packages are downloaded:
     ```
     imeon_inverter_api
     ```

3. **Restart Home Assistant:**
   - After downloading the integration and installing the requirements, restart your Home Assistant instance to load the new integration.

## Configuration

The Imeon Inverter integration supports configuration via the Home Assistant UI. To set it up:

1. **Access Integrations:**
   - Go to the Home Assistant UI, navigate to `Configuration` > `Integrations`.

2. **Add Integration:**
   - Click the "+" button to add a new integration and search for "Imeon Inverter".

3. **Follow Setup Wizard:**
   - Follow the on-screen instructions to complete the integration setup.

## Features

- **Local Polling:** The integration communicates with the Imeon Inverter using local polling, ensuring data privacy and reducing latency.
- **Config Flow:** Supports configuration through the Home Assistant UI for ease of use.
- **Hub Integration:** Acts as a hub for managing multiple devices and sensors associated with the Imeon Inverter.
- **Services:** Allows to modify certain settings for the inverter either manually or with automations

## Services

These can be found `Developer tools` > `Actions`. For a given service name you will find it under the name `<inverter-name>_<action-name>`.

### Inverter Mode : `*_inverter_mode`

- **Friendly Name:** Inverter Mode
- **Description:** Change the mode of the inverter.
- **Fields**:
   - **mode** (string):
      - Allowed values: 'smg', 'bup', 'ong', 'ofg'
      - Example: 'smg'

### Maximum Power Point Tracking Range : `*_mppt`

- **Friendly Name:** Maximum Power Point Tracking Range
- **Description:** Change the working range of the MPPT.
- **Fields**:
   - **low** (integer):
      - Minimum value: 350
      - Example: 350
   - **high** (integer):
      - Maximum value: 700
      - Example: 700

### Grid Feed-in (Injection) : `*_feed_in`

- **Friendly Name:** Grid Feed-in (Injection)
- **Description:** Change whether or not the inverter injects power into the grid.
- **Fields**:
   - **active** (boolean):
      - Example: True

### Injection Power Limit : `*_injection_power`

- **Friendly Name:** Injection Power Limit
- **Description:** Change the power limit when injecting into the grid.
- **Fields**:
   - **limit** (integer):
      - Range: 0 - 8000
      - Example: 3000

### LCD Screen Sleep Time : `*_lcd_time`

- **Friendly Name:** LCD Screen Sleep Time
- **Description:** Change the time it takes for the LCD screen to go to sleep.
- **Fields**:
   - **time** (integer):
      - Allowed values: 0, 1, 2, 10, 20
      - Example: 0

### Battery Night Discharge : `*_night_discharge`

- **Friendly Name:** Battery Night Discharge
- **Description:** Change whether or not the battery should discharge at night.
- **Fields**:
   - **active** (boolean):
      - Allowed values: True, False
      - Example: False

### Battery Charge From Grid : `*_grid_charge`

- **Friendly Name:** Battery Charge From Grid
- **Description:** Change whether or not the battery should charge from the grid.
- **Fields**:
   - **active** (boolean):
      - Allowed values: True, False
      - Example: False

### Relay State : `*_relay`

- **Friendly Name:** Relay State
- **Description:** Change the state of the relay.
- **Fields**:
   - **active** (boolean):
      - Allowed values: True, False
      - Example: False

### AC Output State : `*_ac_output`

- **Friendly Name:** AC Output State
- **Description:** Change whether or not the AC output should be active.
- **Fields**:
   - **active** (boolean):
      - Allowed values: True, False
      - Example: True

### Smartload : `*_smartload`

- **Friendly Name:** Smartload
- **Description:** Returns the information of Smartload, which allocates energy loads over time.
- **Fields**:
   - None needed, this is _read only!_

## Service response

All service responses are composed of a JSON Serializable Object, built as such:
```json
{"result": "failed"}

{"result": "success"}
```
Smartload is an exception and sends back information within the JSON on success.

## Troubleshooting

If you encounter any issues, please ensure that all requirements are installed and that Home Assistant is properly configured to allow custom integrations. For further assistance, consider reaching out to the Home Assistant community or checking the logs for more detailed error messages.

## Contribution
sensor.inverter_86_monitoring_building_consumption_minute
Contributions to improve the Imeon Inverter integration are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more details.
