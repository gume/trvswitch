import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.components.switch import SwitchEntity

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME

#from homeassistant.helpers.entity_component import async_set_icon

#from homeassistant.helpers.service import async_call_service
#from homeassistant.components.climate import async_set_temperature

# Configuration and options
CONF_CLIMATE = "climate"
CONF_OPEN_TEMP = "open_temperature"
CONF_CLOSE_TEMP = "close_temperature"


_LOGGER: logging.Logger = logging.getLogger(__package__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CLIMATE): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_OPEN_TEMP, default=40.0): vol.Schema(float),
    vol.Optional(CONF_CLOSE_TEMP, default=0.0): vol.Schema(float),
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info = None) -> None:
    climate_e = config.get(CONF_CLIMATE)
    open_temp = config.get(CONF_OPEN_TEMP)
    close_temp = config.get(CONF_CLOSE_TEMP)
    name = config.get(CONF_NAME)

    async_add_entities([TRVSwitch(hass, name, climate_e, open_temp, close_temp)])

class TRVSwitch(SwitchEntity):

    def __init__(self, hass, name, climate, open_temp, close_temp):
        self._attr_unique_id = "trvswitch_" + name
        self._attr_icon = "mdi:valve"
        self._name = name
        self._climate = climate
        self._open_temp = open_temp
        self._close_temp = close_temp
        self._state = False
        self._hass = hass

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self._hass.services.async_call("climate", "turn_on", {"entity_id": self._climate})
        #await self._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._climate, "preset_mode": "manual"})
        await self._hass.services.async_call("climate", "set_temperature", {"entity_id": self._climate, "temperature": self._open_temp})
        self._state = True
        self._attr_icon = "mdi:valve-open"
        self._attr_icon_color = "on"
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self._hass.services.async_call("climate", "turn_on", {"entity_id": self._climate})
        #await self._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._climate, "preset_mode": "manual"})
        await self._hass.services.async_call("climate", "set_temperature", {"entity_id": self._climate, "temperature": self._close_temp})
        self._state = False
        self._attr_icon = "mdi:valve-closed"
        self._attr_icon_color = "red"
        self.schedule_update_ha_state()