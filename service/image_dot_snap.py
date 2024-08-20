import functools

import cv2
import numpy as np

from domain.project import Project


class DotSnapPositionComputer:
    def __init__(self, *, snap_analyze_radius: int, im_gray: np.ndarray):
        self._crop_radius = snap_analyze_radius
        self._im_gray = im_gray

    @functools.cache
    def compute_snap_pos(self, current_pos: tuple[float, float]) \
            -> tuple[float, float] | None:  # スナップできない場合はNone
        # 画像をポインタの回りで切り出す
        x_begin = int(current_pos[0] - self._crop_radius)
        x_end = int(current_pos[0] + self._crop_radius)
        y_begin = int(current_pos[1] - self._crop_radius)
        y_end = int(current_pos[1] + self._crop_radius)
        im_gray_crop = self._im_gray[y_begin:y_end, x_begin:x_end]
        if np.prod(im_gray_crop.shape[:2]) != (self._crop_radius * 2) ** 2:  # 端で切り出した時
            return None
        if im_gray_crop.std() <= 2:  # コントラストが低い
            return None

        # 大津の二値化
        _, im_thresh = cv2.threshold(im_gray_crop, 0, 1, cv2.THRESH_OTSU)
        if len(np.unique(im_thresh)) != 2:
            return None
        n_connected_components, _ = cv2.connectedComponents(im_thresh)
        if n_connected_components != 2:
            return None

        # 中心座標と標準偏差を出す
        points_2d = (
                np.indices(im_gray_crop.shape).transpose((2, 1, 0))  # x, y, [idx_x, idx_y]
                + np.array(current_pos)[None, None, :] - self._crop_radius
        )
        mean_lst, std_lst = [], []
        for cls in 0, 1:
            points = points_2d[im_thresh == cls, :]
            mean_lst.append(points.mean(axis=0))
            std_lst.append(np.linalg.norm(points.std(axis=0)))

        # 点の方のクラスを出す
        cls = np.argmin(std_lst)

        # クロップ領域の端にかかっていないか検証
        def mask_borders(arr, num=1):
            # https://stackoverflow.com/questions/41200719/how-to-get-all-array-edges
            mask = np.zeros(arr.shape, bool)
            for dim in range(arr.ndim):
                mask[tuple(
                    slice(0, num) if idx == dim else slice(None) for idx in range(arr.ndim))] = True
                mask[tuple(slice(-num, None) if idx == dim else slice(None) for idx in
                           range(arr.ndim))] = True
            return mask

        edge_classes = im_thresh[mask_borders(im_thresh)]
        if np.any(edge_classes == cls):
            return None

        # スナップ位置を出す
        snap_x, snap_y = mean_lst[cls]
        return snap_x, snap_y


class ImageDotSnapService:
    def __init__(self, project: Project):
        self._computer = DotSnapPositionComputer(
            snap_analyze_radius=50,
            im_gray=project.im_gray,
        )

    def get_snap_pos(
            self,
            *,
            current_pos: tuple[float, float],
    ) -> tuple[float, float] | None:  # スナップできない場合はNone
        # キャッシュを有効活用するためにcurrent_posを量子化する
        x, y = current_pos
        n = 4
        x = int(x / n) * n
        y = int(y / n) * n
        current_pos = x, y
        # print(self._computer.compute_snap_pos.cache_info())
        return self._computer.compute_snap_pos(current_pos)
