from dataclasses import dataclass

import numpy as np
import sympy.core


@dataclass
class CameraParameterSolution:  # TODO: freeze and implement cache
    solution: dict[sympy.core.Symbol, float]

    def values(self) -> list[float]:
        return list(self.solution.values())

    def as_matrix(self) -> np.ndarray:
        matrix = np.empty(shape=(3, 4), dtype=np.float64)
        values = self.values()
        indexes = [
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 1),
            (3, 2),
            (3, 3),
        ]
        for v, (row, col) in zip(values, indexes):
            matrix[row - 1, col - 1] = v
        matrix[2, 3] = 1
        return matrix

    def transform_3d_to_2d(self, points: tuple[float, float, float]) -> tuple[float, float]:
        x, y, _ = self.as_matrix() @ np.array((*points, 1))
        s = np.dot(self.as_matrix()[2, :], np.array((*points, 1)))
        return float(x / s), float(y / s)

    def calculate_2d_units(self, unit_mm=20) -> tuple[
                                                    tuple[float, float],  # origin
                                                    tuple[float, float],  # norm_x
                                                    tuple[float, float],  # norm_y
                                                    tuple[float, float],  # norm_z
                                                ] | None:
        p_origin = self.transform_3d_to_2d((0, 0, 0))
        p_norm_x = self.transform_3d_to_2d((unit_mm, 0, 0))
        p_norm_y = self.transform_3d_to_2d((0, unit_mm, 0))
        p_norm_z = self.transform_3d_to_2d((0, 0, unit_mm))
        return p_origin, p_norm_x, p_norm_y, p_norm_z

    def is_valid(self) -> bool:
        p_origin, p_norm_x, p_norm_y, p_norm_z = self.calculate_2d_units()
        values = np.array([*p_origin, *p_norm_x, *p_norm_y, *p_norm_z])
        if np.any(~np.isfinite(values)):
            return False
        if np.any(np.abs(values) > 1e+4):
            return False
        return True
