from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from application.current_project import get_current_project
from application.dependency import get_image_dot_snap_service, get_equation_solve_service
from control.widget_camera_parameter_view import CameraParameterViewWidget
from control.widget_image_points import ImagePointsWidget
from control.widget_image_view import ImageViewWidget
from control.widget_option_edit import OptionEditWidget
from dto.image_view_annotation import Annotation
from dto.image_view_mouse_event import ImageViewMousePressEvent


class MainWindowWidget(QWidget):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        layout_root = QHBoxLayout()
        self.setLayout(layout_root)

        self._w_image_view = ImageViewWidget(self)
        self._w_image_view.set_data(get_current_project().im_bgr)
        self._w_image_view.set_scaling(0.6)
        layout_root.addWidget(self._w_image_view, 1)

        layout_right = QVBoxLayout()
        layout_root.addLayout(layout_right)

        self._w_image_points = ImagePointsWidget(self)
        self._w_image_points.set_data(get_current_project().image_points)
        layout_right.addWidget(self._w_image_points, 1)

        self._w_camera_parameter_view = CameraParameterViewWidget(self)
        layout_right.addWidget(self._w_camera_parameter_view)

        self._w_option_edit = OptionEditWidget(self)
        self._w_option_edit.set_data(get_current_project().options)
        layout_right.addWidget(self._w_option_edit)

    def _init_signals(self):
        self._w_image_view.image_clicked.connect(self._w_image_view_image_clicked)
        self._w_image_view.image_mouse_moved.connect(self._w_image_view_image_mouse_moved)
        self._w_option_edit.changed.connect(self._w_option_changed)

    @pyqtSlot(ImageViewMousePressEvent)
    def _w_image_view_image_clicked(self, evt: ImageViewMousePressEvent):
        # 点を取得
        if evt.right_clicked:  # 右クリック
            pos = None
            is_snapped = False
        else:  # 左クリック
            if get_current_project().options.enable_snap:
                pos = get_image_dot_snap_service().get_snap_pos(
                    current_pos=evt.pos_camera,
                )
                if pos is None:
                    pos = evt.pos_camera
                    is_snapped = False
                else:
                    is_snapped = True
            else:
                pos = evt.pos_camera
                is_snapped = False
        # オプションによっては中断
        if get_current_project().options.record_snapped_positions_only:
            if pos is not None and not is_snapped:
                return
        # クリックされた点を書きこむ
        image_point = self._w_image_points.get_selected_image_point()
        image_point.pos_camera = pos
        get_current_project().image_points[image_point.pos_world] = image_point
        self._w_image_points.set_data(get_current_project().image_points)
        # 画像のアノテーションを更新
        annotations = []
        for image_point in get_current_project().image_points.values():
            if image_point.has_pos_camera:
                annot = Annotation(
                    pos=image_point.pos_camera,
                    text=image_point.name,
                )
                annotations.append(annot)
        self._w_image_view.set_annotations(annotations)
        # 解く
        camera_solution = get_equation_solve_service().solve_camera_parameters()
        self._w_camera_parameter_view.set_data(camera_solution)
        self._w_image_view.set_camera_parameter_solution(camera_solution)
        # もし次の点があれば次に送る
        image_point = self._w_image_points.get_selected_image_point()
        next_image_point = get_current_project().image_points.get_next(image_point)
        if next_image_point is not None:
            self._w_image_points.set_selected_image_point(next_image_point)

    @pyqtSlot(ImageViewMousePressEvent)
    def _w_image_view_image_mouse_moved(self, evt: ImageViewMousePressEvent):
        # マウスが動いたら選択されている点を更新する
        if get_current_project().options.enable_snap:
            pos = get_image_dot_snap_service().get_snap_pos(
                current_pos=evt.pos_camera,
            )
            is_snapped = True
            if pos is None:
                pos = evt.pos_camera
                is_snapped = False
        else:
            pos = evt.pos_camera
            is_snapped = False
        self._w_image_view.set_pointer(
            pos=pos,
            color=(0, 255, 0) if is_snapped else (0, 0, 255),
        )

    @pyqtSlot()
    def _w_option_changed(self):
        get_current_project().options = self._w_option_edit.get_data()


class MainWindow(QMainWindow):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        self.setWindowTitle("光切断法キャリブレーションツール")
        self.resize(1500, 700)

        self._w_main_widget = MainWindowWidget(self)
        self.setCentralWidget(self._w_main_widget)

    def _init_signals(self):
        pass
