## README for Imeon Inverter Home Assistant Custom Integration

### Imeon Inverter

This repository contains a custom integration for Home Assistant to support Imeon Inverters. The integration allows for local polling of the inverter data and provides a hub for managing your solar energy system.

### Installation

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

### Configuration

The Imeon Inverter integration supports configuration via the Home Assistant UI. To set it up:

1. **Access Integrations:**
   - Go to the Home Assistant UI, navigate to `Configuration` > `Integrations`.

2. **Add Integration:**
   - Click the "+" button to add a new integration and search for "Imeon Inverter".

3. **Follow Setup Wizard:**
   - Follow the on-screen instructions to complete the integration setup.

### Features

- **Local Polling:** The integration communicates with the Imeon Inverter using local polling, ensuring data privacy and reducing latency.
- **Config Flow:** Supports configuration through the Home Assistant UI for ease of use.
- **Hub Integration:** Acts as a hub for managing multiple devices and sensors associated with the Imeon Inverter.

### Requirements

- Home Assistant version that supports custom integrations.
- Python package: `imeon_inverter_api`

### Version

- Current version: 0.5.7

### Troubleshooting

If you encounter any issues, please ensure that all requirements are installed and that Home Assistant is properly configured to allow custom integrations. For further assistance, consider reaching out to the Home Assistant community or checking the logs for more detailed error messages.

### Contribution

Contributions to improve the Imeon Inverter integration are welcome. Please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more details.
