import functools
from pathlib import Path

import cv2
import numpy as np

from domain.image_points import ImagePointMapping
from domain.option import Options


class Project:
    def __init__(
            self,
            *,
            im_bgr: np.ndarray,
            image_points: ImagePointMapping,
            options: Options,
    ):
        self._im_bgr = im_bgr
        self._image_points = image_points
        self._options = options

    @classmethod
    def create_new_from_image_filepath(cls, filepath: Path):  # TODO: ProjectCreateServiceに分ける
        im_bgr = cv2.imread(str(filepath), cv2.IMREAD_COLOR)
        return cls(
            im_bgr=im_bgr,
            image_points=ImagePointMapping.create_default(),
            options=Options.create_default(),
        )

    @property
    def im_bgr(self) -> np.ndarray:
        return self._im_bgr

    @functools.cached_property
    def im_gray(self) -> np.ndarray:
        return cv2.cvtColor(self._im_bgr, cv2.COLOR_BGR2GRAY)

    @property
    def image_points(self) -> ImagePointMapping:
        return self._image_points

    @property
    def options(self) -> Options:
        return self._options

    @options.setter
    def options(self, value):
        self._options = value
