'''
Home Assistant integration for Imeon Inverters
---
Rodrigue Lemaire
---
July 2024
'''

import logging
from typing import Any
import voluptuous as vol                       

from homeassistant import config_entries        # type: ignore
from homeassistant.core import callback         # type: ignore

from .const import *        
from .inverter import InverterCoordinator

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle initial configuration by providing fields for the user to fill out."""

    VERSION = 4
    
    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Provide a form to fill out on HUB creation then create config entries with the provided data."""
        # Usual entry creation for HUBs
        schema = vol.Schema({
            vol.Required("inverter"): str,
            vol.Required("address" ): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

        # Define fields for user input        
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=schema)
        
        data = {
            "address"  : user_input["address"],
            "username" : user_input["username"],
            "password" : user_input["password"]
        }

        return self.async_create_entry(title=str(user_input["inverter"]), data=data)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """Handle subsequent configuration changes by providing fields for the user to edit."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Provide a form to edit then update already existing config entries accordingly."""

        HUB = InverterCoordinator.get_from_id(self.config_entry.entry_id)

        if user_input is not None:

            data = {
                "address"  : user_input["address"] ,
                "username" : user_input["username"],
                "password" : user_input["password"]
            }
            HUB.update(user_input)

            # Update config entry
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=data, options=self.config_entry.options)

            return self.async_create_entry(title=self.config_entry.title, data=data)
        
        # Put back default values in the config menu
        schema = vol.Schema({
                vol.Required("address" , default=HUB.api.get_address()): str,
                vol.Required("username", default=HUB.username): str,
                vol.Required("password", default=HUB.password): str,
            })

        return self.async_show_form(step_id="init", data_schema=schema)
