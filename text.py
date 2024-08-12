'''
Home Assistant integration for Imeon Inverters
---
Rodrigue Lemaire
---
July 2024
'''

import logging

from .const import DOMAIN
from .path import LIST_TEXT, GET_REQUESTS, TIMELINE_WARNINGS
from .inverter import InverterCoordinator

from homeassistant.components.text import TextEntity                   # type: ignore
from homeassistant.helpers.update_coordinator import CoordinatorEntity # type: ignore
from homeassistant.core import HomeAssistant, callback                 # type: ignore
from homeassistant.config_entries import ConfigEntry                   # type: ignore
from homeassistant.helpers.entity_platform import AddEntitiesCallback  # type: ignore

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, 
                            async_add_entities: AddEntitiesCallback) -> None:

    IC: InverterCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [] #[InverterText(IC, str(val), entry) for val in LIST_TEXT]

    # Init "sensor" entities
    for key in LIST_TEXT:
        val = GET_REQUESTS[key]
        e = InverterText(IC, key, entry, val["friendly_name"])
        entities.append(e)

    # Init timeline entity
    e = InverterText(IC, "timeline", entry, "Timeline")
    entities.append(e)

    async_add_entities(entities, True)


# A sensor that returns text values
class InverterText(CoordinatorEntity, TextEntity):

    device_title = ""

    def __init__(self, coordinator, data_key, entry, friendly_name):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.data_key = data_key
        self._entry_id = entry.entry_id
        self._namespace = DOMAIN + "." + data_key
        self._device = entry.title

        self._attr_name = friendly_name
        self._attr_native_value = None
        self._attr_mode = "text"
        self._attr_icon = "mdi:alphabetical" 
        self._attr_unique_id = f"{self._entry_id}_{self.data_key}"  
        self._attr_editable = False

        self._attr_has_entity_name = True
    
    @property
    def device_info(self):
        """Return device information about this entity."""
        # This needs to be strictly identical for every entity
        # so as to have every entity grouped under one single
        # device in the integration menu.
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._device,
            "manufacturer": "Imeon Energy",
            "model": "Home Assistant Integration",
            "sw_version": "1.0",
        }

    @property
    def native_value(self):
        """Return the native value of the text entity."""

        # Treat special cases that need formatting to be readable
        if self.data_key == "mode_name":
            match self._attr_native_value:
                case "SMG" : return "Smart Grid"
                case "BUP" : return "Backup"
                case "100" : return "On Grid"
                case "150" : return "Off Grid"
        
        # Send raw data for the rest
        return self._attr_native_value
    
    async def async_set_value(self, value: str) -> None:
        """Change the value of the text entity."""
        if self._attr_editable == False:
            self.async_write_ha_state()
            return 
        else: return # TODO implement edition after POST

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        try:
            # Timeline requires special handling
            if self.data_key == "timeline":
                fetched = self.coordinator.data.get("timeline", None)[0]

                if self._attr_native_value == fetched["message"]: return None 
                self._attr_native_value = fetched["message"]
                
                # Attempt to change icons to match the event type
                try: self._attr_icon = TIMELINE_WARNINGS[fetched["type"]]
                except: pass

            # Rest of the data is passed as is
            else: 
                fetched = str(self.coordinator.data.get(self.data_key, None))
                if self._attr_native_value == fetched: return None 
                self._attr_native_value = fetched
        except Exception as e:
            self._attr_native_value = None # N/A

        # Request a data update
        self.async_write_ha_state()
        return None
    
