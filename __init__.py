'''
Home Assistant integration for Imeon Inverters
---
Rodrigue Lemaire
---
July 2024
'''

from __future__ import annotations

import logging
import re
import unicodedata

from .inverter import InverterCoordinator
from .const import *

from homeassistant.core import HomeAssistant        # type: ignore
from homeassistant.helpers.typing import ConfigType # type: ignore
from homeassistant import config_entries            # type: ignore
from homeassistant.exceptions import ConfigEntryNotReady # type: ignore

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["text", "sensor"]

# __INIT__ #
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """
    Load the integration into HASSOS (asynchronous). 
    
    This function recovers config entries and for each one create 
    the HUB instances needed to update data. It then updates config 
    entries accordingly.
    """

    # Re-instanciate the HUBs on startup
    entries = hass.config_entries.async_entries(DOMAIN)
    for entry in entries:
        # Create the corresponding HUB
        data = {
            "address"  : entry.data.get("address", ""),
            "username" : entry.data.get("username", ""),
            "password" : entry.data.get("password", "")
        }
        IC = InverterCoordinator(hass, data, entry.entry_id, entry.title)

        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = IC

    # Return boolean to indicate that initialization was successfully.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """
    Handle the creation of a new config entry for the integration (asynchronous).

    This function creates the HUB corresponding to the data in the entry.
    It then updates the config entry accordingly. It forces a first
    update to avoid having empty data before the first refresh.
    After filtering the user's input through Unicodedata and RegEx
    the function will create a dashboard for this specific entry.
    """

    # Create the corresponding HUB
    data = {
        "address"  : entry.data.get("address", ""),
        "username" : entry.data.get("username", ""),
        "password" : entry.data.get("password", "")
    } # NOTE UUID allows updates instead of creating new hubs
    IC = InverterCoordinator(hass, data, entry.entry_id, entry.title)
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = IC

    # Call for HUB creation then each entity as a List
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Gather a first round of data to avoid empty data before refresh
    hass.async_create_task(IC.async_config_entry_first_refresh()) 
    #await IC.async_config_entry_first_refresh()

    return True

async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Handle entry unloading."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def update_listener(hass: HomeAssistant, entry: config_entries.ConfigFlow) -> None:
    """Handle options update."""
    # hass.config_entries.async_update_entry(entry, data=new_data, minor_version=3, version=1)
    # Handle the updated options
    await hass.config_entries.async_reload(entry.entry_id)
