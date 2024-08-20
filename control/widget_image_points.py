import copy

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QLabel, QListWidgetItem, QVBoxLayout

from domain.image_points import ImagePointMapping, ImagePoint
from util.fonts import font


class ImagePointListItemWidget(QWidget):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._is_selected = False
        self._image_point: ImagePoint | None = None

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._l_selected = QLabel(self)
        self._l_selected.setFixedWidth(20)
        self._l_selected.setFont(font(small=True, monospace=True))
        layout.addWidget(self._l_selected)

        self._l_name = QLabel(self)
        self._l_name.setFixedWidth(50)
        self._l_name.setFont(font(small=True, monospace=True))
        layout.addWidget(self._l_name)

        self._l_point_world = QLabel(self)
        self._l_point_world.setFixedWidth(110)
        self._l_point_world.setFont(font(small=True, monospace=True))
        layout.addWidget(self._l_point_world)

        self._l_point_camera = QLabel(self)
        self._l_point_camera.setFixedWidth(150)
        self._l_point_camera.setFont(font(small=True, monospace=True))
        layout.addWidget(self._l_point_camera)

        layout.addStretch(1)

    def _init_signals(self):
        pass

    def _update_view(self):
        if self._is_selected:
            self._l_selected.setText(">>>")
        else:
            self._l_selected.setText("")

        self._l_name.setText(self._image_point.name)

        self._l_point_world.setText(
            f"({self._image_point.pos_world[0]:>2.0f},"
            f" {self._image_point.pos_world[1]:>2.0f},"
            f" {self._image_point.pos_world[2]:>2.0f})"
        )

        if self._image_point.has_pos_camera:
            self._l_point_camera.setText(
                f"({self._image_point.pos_camera[0]:>4.0f},"
                f" {self._image_point.pos_camera[1]:>4.0f})"
            )
        else:
            self._l_point_camera.setText("--")

    def set_data(self, image_point: ImagePoint | None):
        self._image_point = image_point
        self._update_view()

    def get_data(self):
        return copy.deepcopy(self._image_point)

    def set_selected(self, is_selected: bool):
        self._is_selected = is_selected
        self._update_view()

    def is_selected(self) -> bool:
        return self._is_selected


class ImagePointListWidget(QListWidget):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._w_item_mapping: dict[tuple[float, float, float], ImagePointListItemWidget] \
            = {}

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        pass

    def _init_signals(self):
        # noinspection PyUnresolvedReferences
        self.itemSelectionChanged.connect(self._item_selection_changed)

    def set_data(self, image_point_mapping: ImagePointMapping):
        if self.count() == 0:
            for pos_world, image_point in image_point_mapping.items():
                item_widget = ImagePointListItemWidget(self)
                item_widget.set_data(image_point)
                self._w_item_mapping[pos_world] = item_widget
                list_item = QListWidgetItem()
                list_item.setSizeHint(item_widget.sizeHint())
                self.addItem(list_item)
                self.setItemWidget(list_item, item_widget)
            self.setFixedWidth(self.sizeHintForColumn(0) + 20)
            self.set_selected_index(0)
        else:
            for pos_world, image_point in image_point_mapping.items():
                self._w_item_mapping[pos_world].set_data(image_point)

    def get_data(self) -> ImagePointMapping:
        mapping: ImagePointMapping = ImagePointMapping()
        for pos_world, item_widget in self._w_item_mapping.items():
            mapping[pos_world] = item_widget.get_data()
        return mapping

    def set_selected_index(self, i: int):
        for i_row in range(len(self._w_item_mapping)):
            pos_world = list(self._w_item_mapping.keys())[i_row]
            self._w_item_mapping[pos_world].set_selected(i_row == i)

    def get_selected_pos_world(self) -> tuple[float, float, float]:
        for pos_world, item_widget in self._w_item_mapping.items():
            if item_widget.is_selected():
                return pos_world
        assert False

    def get_selected_image_point(self) -> ImagePoint:
        return self._w_item_mapping[self.get_selected_pos_world()].get_data()

    def set_selected_image_point(self, image_point: ImagePoint):
        self.set_selected_index(list((self._w_item_mapping.keys())).index(image_point.pos_world))

    @pyqtSlot()
    def _item_selection_changed(self):
        i_row = self.currentRow()
        self.blockSignals(True)
        self.clearSelection()
        self.set_selected_index(i_row)
        self.blockSignals(False)


class ImagePointsWidget(QWidget):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self._w_image_point_list = ImagePointListWidget(self)
        layout.addWidget(self._w_image_point_list)

    def _init_signals(self):
        pass

    def set_data(self, image_point_mapping: ImagePointMapping):
        self._w_image_point_list.set_data(image_point_mapping)

    def get_data(self) -> ImagePointMapping:
        return self._w_image_point_list.get_data()

    def get_selected_image_point(self) -> ImagePoint:
        return self._w_image_point_list.get_selected_image_point()

    def set_selected_image_point(self, image_point: ImagePoint):
        self._w_image_point_list.set_selected_image_point(image_point)
