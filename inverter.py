'''
Home Assistant integration for Imeon Inverters
---
Rodrigue Lemaire
---
July 2024
'''

from __future__ import annotations

import async_timeout
from datetime import timedelta
import logging
from typing import Any, Dict

from imeon_inverter_api.inverter import Inverter                           # type: ignore
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator # type: ignore
from homeassistant.core import HomeAssistant                               # type: ignore

from .const import *

_LOGGER = logging.getLogger(__name__)

# HUB CREATION #
class InverterCoordinator(DataUpdateCoordinator):
    """
    Abstract representation of an inverter.

    A HUB or a data update coordinator is a HASS Object that automatically polls
    data at regular intervals. Entities representing the different sensors and
    settings then all poll data from their HUB. Each inverter is it's own HUB
    thus it's own data set. This allows this integration to handle as many
    inverters as possible in parallel.
    """
   
    _HUBs : Dict[InverterCoordinator] = {} 

    # Implement methods to fetch and update data
    def __init__(self, hass: HomeAssistant, user_input: dict[str, Any] 
                 | None = None, uuid = 0, title = HUBNAME) -> None:
        """Initialize data update coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=HUBNAME,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=1),
            always_update=True
        )
        self.api = Inverter(user_input["address"]) # API calls
        self.username = user_input["username"]
        self.password = user_input["password"]
        self.friendly_name = title

        # unique ID
        self.__id = uuid
        InverterCoordinator._HUBs[str(self.__id)] = self

        # Store request data
        self.data = {}
        self.first_call = True

        return None
    
    def update(self, user_input: dict[str, Any]) -> None:
        """Update HUB data based on user input."""
        self.api = Inverter(user_input["address"])
        self.username = user_input["username"]
        self.password = user_input["password"]
        self.first_call = True

    @property
    def id(self):
        return self.__id
    
    @staticmethod
    def get_from_id(id) -> InverterCoordinator:
        try:
            return InverterCoordinator._HUBs[str(id)]
        except:
            raise Exception("Incorrect HUB ID (" + str(id) + ") .") from None
    
    # DATA UPDATES # 
    async def _async_update_data(self) -> Dict:
        """
        Fetch and store newest data from API.

        This is the place to where entities can get their data.
        It also includes the login process. 
        """

        try:
            if self.first_call:
                # First call shouldn't slow down home assistant
                self.first_call = False
                #self.hass.async_create_task(self.api.init())
                return self.data # Send empty data on init, avoids timeout'''


            async with async_timeout.timeout(TIMEOUT*4):
                                
                # Am I logged in ? If not log in
                await self.api.login(self.username, self.password)

                # Fetch data using distant API
                if self.api.inverter.get("inverter", None) != None:
                    await self.api.update()
                else:
                    await self.api.init() # Failsafe if data is missing

                entity_dict: dict = self.api._storage

                # Store in data for entities to use
                for key in entity_dict.keys():
                    if key != 'timeline':
                        val = entity_dict[key]
                        for sub_key, sub_val in val.items():
                            self.data[key + "_" + sub_key] = sub_val
                    else: # Timeline is a list not a dict
                        self.data[key] = entity_dict[key]
                    
        except TimeoutError as e:
            _LOGGER.error(str(self.friendly_name) + ' | Timeout Error: Reconnection failed, please check credentials.'
                          + ' If the error persists check the network connection.')
        except Exception as e:
            _LOGGER.error(str(self.friendly_name) + ' | Data Update Error: ' + str(e))
                
        return self.data # send stored data so entities can poll it
