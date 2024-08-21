import cv2
import numpy as np
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QAbstractSlider

from dto.equation_solution import CameraParameterSolution
from dto.image_view_annotation import Annotation
from dto.image_view_mouse_event import ImageViewMousePressEvent, ImageViewMouseMoveEvent


class ImageViewWidget(QGraphicsView):
    image_clicked = pyqtSignal(ImageViewMousePressEvent, name="image_clicked")
    image_mouse_moved = pyqtSignal(ImageViewMouseMoveEvent, name="image_mouse_moved")

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._im_bgr: QPixmap = QPixmap()
        self._scaling: float = 1.0
        self._pointer_pos: tuple[float, float] = 0, 0
        self._pointer_color: tuple[int, int, int] = 0, 0, 0
        self._annotations: list[Annotation] = []
        self._camera_parameter_solution: CameraParameterSolution | None = None

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        self.setMouseTracking(True)
        # noinspection PyTypeChecker
        self.setVerticalScrollBar(None)
        # noinspection PyTypeChecker
        self.setHorizontalScrollBar(None)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

    def _init_signals(self):
        pass

    def _update_view(self):
        # https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
        im_bgr = self._im_bgr.copy()
        im_bgr = cv2.resize(im_bgr, None, fx=self._scaling, fy=self._scaling)

        # 座標系の描画
        if self._camera_parameter_solution is not None \
                and self._camera_parameter_solution.is_valid():
            p_origin, p_norm_x, p_norm_y, p_norm_z \
                = self._camera_parameter_solution.calculate_2d_units()
            cv2.circle(
                im_bgr,
                (int(p_origin[0] * self._scaling), int(p_origin[1] * self._scaling)),
                3,
                (0, 0, 0),
                -1,
                cv2.LINE_AA,
            )
            for p_norm, color in zip(
                    [p_norm_x, p_norm_y, p_norm_z],
                    [(0, 0, 255), (0, 255, 0), (255, 0, 0)],
            ):
                cv2.line(
                    im_bgr,
                    (int(p_origin[0] * self._scaling), int(p_origin[1] * self._scaling)),
                    (int(p_norm[0] * self._scaling), int(p_norm[1] * self._scaling)),
                    color,
                    1,
                    cv2.LINE_AA,
                )

        # 十字のポインターと座標の描画
        cv2.line(
            im_bgr,
            (int(self._pointer_pos[0]) - 10, int(self._pointer_pos[1])),
            (int(self._pointer_pos[0]) + 10, int(self._pointer_pos[1])),
            self._pointer_color,
            1,
            cv2.LINE_AA,
        )
        cv2.line(
            im_bgr,
            (int(self._pointer_pos[0]), int(self._pointer_pos[1]) - 10),
            (int(self._pointer_pos[0]), int(self._pointer_pos[1]) + 10),
            self._pointer_color,
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            im_bgr,
            f"({int(self._pointer_pos[0] / self._scaling)},"
            f" {int(self._pointer_pos[1] / self._scaling)})",
            (int(self._pointer_pos[0]) + 10, int(self._pointer_pos[1]) + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            self._pointer_color,
            1,
            cv2.LINE_AA,
        )

        # アノテーションの描画
        for annot in self._annotations:
            x, y = annot.pos
            x, y = int(x * self._scaling), int(y * self._scaling)
            cv2.circle(
                im_bgr,
                (x, y),
                3,
                (255, 0, 0),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                im_bgr,
                annot.text,
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1,
                cv2.LINE_AA,
            )

        # 画像をビューに反映
        # https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
        # img = QImage(im_bgr.data, im_bgr.shape[1], im_bgr.shape[0], 3 * im_bgr.shape[1], QImage.Format_RGB888)
        # self.setSceneRect(0, 0, im

        # ビューへの画像の割り当て
        height, width, channel = im_bgr.shape
        img = QImage(im_bgr, width, height, 3 * width, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(img)
        self._scene.clear()
        self._scene.addPixmap(pixmap)

    def set_data(self, im_bgr: np.ndarray):
        self._im_bgr = im_bgr
        self._update_view()

    def set_scaling(self, scaling: float) -> None:
        self._scaling = scaling
        self._update_view()

    def set_pointer(self, *, pos: tuple[float, float], color: tuple[int, int, int]) -> None:
        self._pointer_pos = pos[0] * self._scaling, pos[1] * self._scaling
        self._pointer_color = color
        self._update_view()

    def set_annotations(self, annotations: list[Annotation]) -> None:
        self._annotations = annotations
        self._update_view()

    def set_camera_parameter_solution(self, camera_parameter_solution: CameraParameterSolution):
        self._camera_parameter_solution = camera_parameter_solution

    def mousePressEvent(self, evt: QMouseEvent):
        pos = self.mapToScene(evt.pos())
        param: ImageViewMousePressEvent = ImageViewMousePressEvent(
            pos_camera=(
                pos.x() / self._scaling,
                pos.y() / self._scaling,
            ),
            right_clicked=evt.button() == Qt.RightButton,
        )
        # noinspection PyUnresolvedReferences
        self.image_clicked.emit(param)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = self.mapToScene(event.pos())
        param: ImageViewMouseMoveEvent = ImageViewMouseMoveEvent(
            pos_camera=(
                pos.x() / self._scaling,
                pos.y() / self._scaling,
            ),
        )
        # noinspection PyUnresolvedReferences
        self.image_mouse_moved.emit(param)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.ControlModifier:
            wheel_event: QWheelEvent = event
            if wheel_event.angleDelta().y() > 0:
                self.set_scaling(self._scaling * 1.05)
            else:
                self.set_scaling(self._scaling / 1.05)
        else:
            if event.modifiers() == Qt.ShiftModifier:
                scrollbar = self.horizontalScrollBar()
            else:
                scrollbar = self.verticalScrollBar()

            action = QAbstractSlider.SliderSingleStepAdd
            if event.angleDelta().y() > 0:
                action = QAbstractSlider.SliderSingleStepSub

            for _ in range(2):
                scrollbar.triggerAction(action)
