from dataclasses import dataclass

import numpy as np


@dataclass
class ImagePoint:
    pos_world: tuple[float, float, float]
    name: str
    pos_camera: tuple[float, float] | None = None

    @classmethod
    def create_default(cls, pos_world: tuple[float, float, float], name: str):
        return ImagePoint(pos_world=pos_world, name=name, pos_camera=None)

    @property
    def has_pos_camera(self) -> bool:
        return self.pos_camera is not None


class ImagePointMapping(dict[tuple[float, float, float], ImagePoint]):
    def ordered_keys(self) -> list[tuple[float, float, float]]:
        return list(self.keys())

    def get_first(self) -> ImagePoint:
        return self[self.ordered_keys()[0]]

    def get_next(self, image_point: ImagePoint) -> ImagePoint | None:  # None if no next item found
        i = self.ordered_keys().index(image_point.pos_world)
        i += 1
        if i >= len(self.ordered_keys()):
            return None
        return self[self.ordered_keys()[i]]

    @property
    def points_array(self) -> np.ndarray:
        points_world = np.array([
            image_point.pos_world
            for image_point in self.values()
            if image_point.has_pos_camera
        ])
        points_camera = np.array([
            image_point.pos_camera
            for image_point in self.values()
            if image_point.has_pos_camera
        ])
        return np.hstack([points_world, points_camera])

    @classmethod
    def create_default(cls):
        points_xy = [
            (1, 1, 0),
            (2, 1, 0),
            (3, 1, 0),
            (1, 2, 0),
            (2, 2, 0),
            (3, 2, 0),
            (1, 3, 0),
            (2, 3, 0),
            (3, 3, 0),
        ]
        points_yz = [
            (0, 1, 1),
            (0, 2, 1),
            (0, 3, 1),
            (0, 1, 2),
            (0, 2, 2),
            (0, 3, 2),
            (0, 1, 3),
            (0, 2, 3),
            (0, 3, 3),
        ]
        points_zx = [
            (1, 0, 1),
            (1, 0, 2),
            (1, 0, 3),
            (2, 0, 1),
            (2, 0, 2),
            (2, 0, 3),
            (3, 0, 1),
            (3, 0, 2),
            (3, 0, 3),
        ]
        points_world_int = [
            *points_xy,
            *points_yz,
            *points_zx,
        ]
        names = [
            *[f"XY-{i + 1}" for i, _ in enumerate(points_xy)],
            *[f"YZ-{i + 1}" for i, _ in enumerate(points_yz)],
            *[f"ZX-{i + 1}" for i, _ in enumerate(points_zx)],
        ]
        points_world: list[tuple[float, float, float]] = [
            (xi * 20.0, yi * 20.0, zi * 20.0)
            for xi, yi, zi in points_world_int
        ]
        return cls({
            pw: ImagePoint.create_default(pos_world=pw, name=name)
            for i, (pw, name) in enumerate(zip(points_world, names))
        })
