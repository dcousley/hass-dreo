"""Diagnostics support for VeSync."""

# Suppress warnings about unused function arguments
# pylint: disable=W0613

from __future__ import annotations

from typing import Any

from .pydreo import PyDreo

from .haimports import * # pylint: disable=W0401,W0614

from .const import (
    DOMAIN,
    DREO_MANAGER
)

KEYS_TO_REDACT = {"sn", "_sn", "wifi_ssid", "module_hardware_mac"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    manager: PyDreo = hass.data[DOMAIN][DREO_MANAGER]

    data = {
        DOMAIN: {
            "fan_count": len(manager.fans),
            "raw_devicelist": _redact_values(manager.raw_response),
        },
        "devices": {
            "fans": [_redact_values(device.__dict__) for device in manager.fans],
        },
    }

    return data


def _redact_values(data: dict) -> dict:
    """Rebuild and redact values of a dictionary, recursively"""

    new_data = {}

    for key, item in data.items():
        if key not in KEYS_TO_REDACT:
            if isinstance(item, dict):
                new_data[key] = _redact_values(item)
            else:
                new_data[key] = item
        else:
            new_data[key] = REDACTED

    return new_data