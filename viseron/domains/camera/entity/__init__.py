"""Base class for entities tied to a camera."""
from __future__ import annotations

from typing import TYPE_CHECKING

from viseron.helpers.entity import Entity

if TYPE_CHECKING:
    from viseron import Viseron

    from .. import AbstractCamera


class CameraEntity(Entity):
    """Base class for entities tied to a specific AbstractCamera."""

    def __init__(self, vis: Viseron, camera: AbstractCamera) -> None:
        self._vis = vis
        self._camera = camera

        self.device_name = camera.name
        self.device_identifiers: list[str] | None = [camera.identifier]
