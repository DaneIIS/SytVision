"""MQTT toggle entity."""
from __future__ import annotations

from typing import TYPE_CHECKING

from viseron.components.mqtt.const import CONFIG_CLIENT_ID
from viseron.components.mqtt.helpers import SubscribeTopic
from viseron.const import STATE_OFF, STATE_ON
from viseron.helpers.entity.toggle import ToggleEntity

from . import MQTTEntity

if TYPE_CHECKING:
    from viseron import Viseron


class ToggleMQTTEntity(MQTTEntity[ToggleEntity]):
    """Base toggle MQTT entity class."""

    def __init__(self, vis: Viseron, config, entity: ToggleEntity) -> None:
        super().__init__(vis, config, entity)
        self._mqtt.subscribe(
            SubscribeTopic(topic=self.command_topic, callback=self.command_handler)
        )

    @property
    def command_topic(self) -> str:
        """Return command topic."""
        return (
            f"{self._config[CONFIG_CLIENT_ID]}/{self.entity.domain}/"
            f"{self.entity.object_id}/command"
        )

    def command_handler(self, message) -> None:
        """Handle commands on the command topic."""
        payload = message.payload.decode()
        if payload == STATE_ON:
            self.entity.turn_on()
        elif payload == STATE_OFF:
            self.entity.turn_off()
