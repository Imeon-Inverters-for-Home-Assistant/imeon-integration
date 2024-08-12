'''
Home Assistant integration for Imeon Inverters
---
Rodrigue Lemaire
---
July 2024
'''

import logging

from .const import DOMAIN
from .path import LIST_FLOAT, GET_REQUESTS
from .inverter import InverterCoordinator

from homeassistant.components.sensor import SensorEntity               # type: ignore
from homeassistant.helpers.update_coordinator import CoordinatorEntity # type: ignore
from homeassistant.core import HomeAssistant, callback                 # type: ignore
from homeassistant.config_entries import ConfigEntry                   # type: ignore
from homeassistant.helpers.entity_platform import AddEntitiesCallback  # type: ignore

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, 
                            async_add_entities: AddEntitiesCallback) -> None:

    IC: InverterCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    # Init "sensor" entities
    for key in LIST_FLOAT:
        val = GET_REQUESTS[key]
        e = InverterSensor(IC, key, entry, val["friendly_name"], val["unit"])
        entities.append(e)

    async_add_entities(entities, True)

# A sensor that returns numerical values
class InverterSensor(CoordinatorEntity, SensorEntity):

    device_title = ""

    def __init__(self, coordinator, data_key, entry, friendly_name, unit):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.data_key = data_key
        self._entry_id = entry.entry_id
        self._namespace = DOMAIN + "." + data_key
        self._device = entry.title

        self._attr_name = friendly_name
        self._attr_native_value = None
        self._attr_native_unit_of_measurement = str(unit)
        self._attr_mode = "box"
        self._attr_icon = "mdi:numeric"
        self._attr_unique_id = f"{self._entry_id}_{self.data_key}"  
        self._attr_editable = False

        #self._attr_device_class = "energy" # only for ['kWh', 'MWh', 'Wh', 'GJ', 'MJ']

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
        """Return the native value of the sensor entity."""

        # Skip all steps if None
        if self._attr_native_value == None: return None
        
        # Treat special cases that need to be converted to proper % format
        if self.data_key in ("qu1", "qu2", "qu3", "qu4"): 
            return self._attr_native_value*100. # 0..1 -> %

        # Return raw data for the rest
        return round(self._attr_native_value, 2)
    
    '''async def async_set_value(self, value: float) -> None: # FIXME deprecated ? lacking decorator ?
        """Change the value of the sensor entity."""
        if self._attr_editable == False:
            self.async_write_ha_state()
            return 
        else: return ''' # TODO implement edition after POST

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        try:
            fetched = float(self.coordinator.data.get(self.data_key, None))
            if self._attr_native_value == fetched: return None 
            self._attr_native_value = fetched
        except Exception as e:
            self._attr_native_value = None # N/A
        
        # Request a data update
        self.async_write_ha_state()
        return None
