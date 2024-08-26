'''
Home Assistant integration for Imeon Inverters
---
Rodrigue Lemaire
---
July 2024
'''

from __future__ import annotations

import logging
import voluptuous as vol # type: ignore

from .inverter import InverterCoordinator
from .const import *
from .path import POST_REQUEST

from homeassistant.core import HomeAssistant, ServiceCall, callback # type: ignore
from homeassistant.helpers.typing import ConfigType # type: ignore
from homeassistant import config_entries            # type: ignore


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

    # Re-instanciate HUBs and services on startup
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

        ''' Services provided for each inverter
            inverter_mode  : <str> (smg | bup | ong | ofg) 
            mppt           : [<int>, <int>]
            feed_in        : <bool>
            injection_power: <int>
            lcd_time       : <int>
            night_discharge: <bool>
            grid_charge    : <bool>
            relay          : <bool>
            ac_output      : <bool>
        '''

        # Define services for each inverter
        for service_name, service_data in POST_REQUEST.items():

            friendly_name: str = service_data.get('friendly_name')
            description: str = service_data.get('description')
            values: dict = service_data.get('fields')

            # Build the input schema with default values and limitations
            vol_dict = {'description': description}
            for value_name, value_data in values.items():
                vol_dict[vol.Required(value_name, 
                                      default=value_data.get("example"), 
                                      )] = value_data.get("type", str)
            schema = vol.Schema(vol_dict)

            # Create each service handler using default arguments
            # This allows each handler to use different field values despite being the 'same' method
            @callback
            async def service_handler(call: ServiceCall, 
                                      entry_title=entry.title, 
                                      service_name=service_name,
                                      values=values,
                                      IC_uiid = entry.entry_id) -> bool: 
                IC = InverterCoordinator.get_from_id(IC_uiid)

                api_call = getattr(IC.api, f"set_{service_name}")
                
                args = []
                for value_name in values.keys():
                    args.append(call.data.get(value_name))
                
                if len(args) == 1: result = await api_call(args[0])
                else: result = await api_call(args[0], args[1])
                _LOGGER.warning(f"{entry_title}_{service_name}({args}): {result}")
                return result
            
            # Register service in hass
            hass.services.async_register(DOMAIN, f"{entry.title}_{service_name}", 
                                         service_handler,
                                         schema=schema)

    # Return boolean to indicate that initialization was successfully
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
