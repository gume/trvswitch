from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.components.switch import SwitchEntity

import voluptuous as vol
import homeassistant.helpers.config_validation as cv


# Configuration and options
CONF_CLIMATE = "climate"
CONF_OPEN_TEMP = "open_temperature"
CONF_CLOSE_TEMP = "close_temperature"


_LOGGER: logging.Logger = logging.getLogger(__package__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CLIMATE): cv.string,
    vol.Optional(CONF_OPEN_TEMP, default=0.0): vol.Schema(float),
    vol.Optional(CONF_CLOSE_TEMP, default=40.0): vol.Schema(float),
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    climate = config.get(CONF_CLIMATE)
    open_temp = config.get(CONF_OPEN_TEMP)
    close_temp = config.get(CONF_CLOSE_TEMP)
    add_entities([TRVSwitch(hass, climate, open_temp, close_temp)])

class TRVSwitch(SwitchEntity):

    def __init__(self, hass, climate, open_temp, close_temp):
        """Initialize the Example switch."""
        self._name = "Kapcs"
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._state = False
        self.schedule_update_ha_state()