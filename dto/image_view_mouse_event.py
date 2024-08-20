from dataclasses import dataclass


@dataclass(frozen=True)
class ImageViewMousePressEvent:
    pos_camera: tuple[float, float]
    right_clicked: bool


@dataclass(frozen=True)
class ImageViewMouseMoveEvent:
    pos_camera: tuple[float, float]
