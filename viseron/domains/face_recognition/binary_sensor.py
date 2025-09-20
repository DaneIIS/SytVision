"""Binary sensor that represents face recognition."""
from __future__ import annotations

from typing import TYPE_CHECKING

from viseron.domains.camera.entity.binary_sensor import CameraBinarySensor

from .const import EVENT_FACE_DETECTED, EVENT_FACE_EXPIRED

if TYPE_CHECKING:
    from viseron import Event, Viseron
    from viseron.domains.camera import AbstractCamera
    from viseron.domains.face_recognition import EventFaceDetected, FaceDict


class FaceDetectionBinarySensor(CameraBinarySensor):
    """Entity that keeps track of face detection."""

    def __init__(self, vis: Viseron, camera: AbstractCamera, face_name: str) -> None:
        super().__init__(vis, camera)
        self._face_name = face_name
        self.object_id = f"{camera.identifier}_face_detected_{face_name}"
        self.name = f"{camera.name} Face Detected {face_name.capitalize()}"
        self.icon = "mdi:face-recognition"

        self._detected = False
        self._face: FaceDict | None = None

    def setup(self) -> None:
        """Set up event listener."""
        self._vis.listen_event(
            EVENT_FACE_DETECTED.format(
                camera_identifier=self._camera.identifier, face=self._face_name
            ),
            self.face_detected,
        )
        self._vis.listen_event(
            EVENT_FACE_EXPIRED.format(
                camera_identifier=self._camera.identifier, face=self._face_name
            ),
            self.face_expired,
        )

    @property
    def _is_on(self):
        return self._detected

    @property
    def extra_attributes(self):
        """Return entity attributes."""
        if self._face:
            return {
                "camera_identifier": self._camera.identifier,
                "camera_name": self._camera.name,
                "name": self._face.name,
                "confidence": self._face.confidence,
                "coordinates": self._face.coordinates,
                "extra_attributes": self._face.extra_attributes,
            }
        return {}

    def face_detected(self, event_data: Event[EventFaceDetected]) -> None:
        """Handle face detected event."""
        self._detected = True
        self._face = event_data.data.face
        self.set_state()

    def face_expired(self, _event_data: Event) -> None:
        """Handle face expired event."""
        self._detected = False
        self._face = None
        self.set_state()
