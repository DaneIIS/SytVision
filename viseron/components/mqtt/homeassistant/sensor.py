"""Home Assistant MQTT sensor."""
from __future__ import annotations

from typing import Final

from viseron.components.mqtt.entity.sensor import SensorMQTTEntity

from .entity import HassMQTTEntity

DOMAIN: Final = "sensor"


class HassMQTTSensor(HassMQTTEntity[SensorMQTTEntity]):
    """Base class for all Home Assistant MQTT sensors."""

    # These should NOT be overridden.
    domain = DOMAIN

    @property
    def config_payload(self):
        """Return config payload."""
        payload = super().config_payload
        if self._mqtt_entity.entity.device_class:
            payload["device_class"] = self._mqtt_entity.entity.device_class
        return payload
