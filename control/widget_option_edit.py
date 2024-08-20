from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from domain.option import Options


class OptionEditWidget(QWidget):
    changed = pyqtSignal(name="changed")

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self._cb_enable_snap = QCheckBox(self)
        self._cb_enable_snap.setText("点にスナップする")
        layout.addWidget(self._cb_enable_snap)

        self._cb_record_snapped_positions_only = QCheckBox(self)
        self._cb_record_snapped_positions_only.setText("スナップした点のクリックのみ記録")
        layout.addWidget(self._cb_record_snapped_positions_only)

    def _init_signals(self):
        # noinspection PyUnresolvedReferences
        self._cb_enable_snap.stateChanged.connect(self.changed)
        # noinspection PyUnresolvedReferences
        self._cb_record_snapped_positions_only.stateChanged.connect(self.changed)

    def set_data(self, options: Options):
        self._cb_enable_snap.setChecked(options.enable_snap)
        self._cb_record_snapped_positions_only.setChecked(options.record_snapped_positions_only)

    def get_data(self) -> Options:
        return Options(
            enable_snap=self._cb_enable_snap.isChecked(),
            record_snapped_positions_only=self._cb_record_snapped_positions_only.isChecked(),
        )
