import numpy as np


class CameraImage:
    def __init__(self, *, im_bgr: np.ndarray, im_gray: np.ndarray):
        self._im_bgr = im_bgr.copy()
        self._im_bgr.setflags(write=False)
        self._im_gray = im_gray.copy()
        self._im_gray.setflags(write=False)
        assert self._im_bgr.shape[:2] == self._im_gray.shape

    @property
    def bgr(self) -> np.ndarray:
        return self._im_bgr

    @property
    def gray(self) -> np.ndarray:
        return self._im_gray

    @property
    def shape(self) -> np.array([int, int]):
        return np.array(self._im_bgr.shape[:2])
