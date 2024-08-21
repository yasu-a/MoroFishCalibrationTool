from pathlib import Path

from PyQt5.QtCore import QObject, QStandardPaths
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QPushButton, \
    QFileDialog, QMessageBox

from application.dependency import get_camera_parameter_save_csv_service
from dto.equation_solution import CameraParameterSolution
from util.app_logging import create_logger
from util.fonts import font


class CameraParameterViewWidget(QWidget):
    _logger = create_logger()

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._solution: CameraParameterSolution | None = None

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        layout_root = QVBoxLayout()
        self.setLayout(layout_root)

        layout_root.addWidget(QLabel("カメラのパラメータ"))

        self._te_python = QPlainTextEdit(self)
        self._te_python.setLineWrapMode(QPlainTextEdit.NoWrap)
        self._te_python.setFont(font(monospace=True, small=True))
        self._te_python.setReadOnly(True)
        self._te_python.setFixedHeight(100)
        layout_root.addWidget(self._te_python)

        layout_button = QHBoxLayout()
        layout_root.addLayout(layout_button)

        layout_button.addStretch(1)

        self._b_export = QPushButton("csvで保存", self)
        # noinspection PyUnresolvedReferences
        self._b_export.clicked.connect(self._b_export_clicked)
        layout_button.addWidget(self._b_export)

    def _init_signals(self):
        pass

    def set_data(self, solution: CameraParameterSolution | None):
        if solution is not None and solution.is_valid():
            self._solution = solution
            matrix = solution.as_matrix()
            self._te_python.setPlainText(
                "np.array([\n" + "\n".join(
                    "    [" + ", ".join(
                        f"{matrix[i][j]:9.3f}"
                        for j in range(4)
                    ) + "],"
                    for i in range(3)
                ) + "\n])"
            )
        else:
            self._solution = None
            self._te_python.setPlainText("")

    def _b_export_clicked(self):
        if self._solution is None:
            return

        csv_fullpath, _ = QFileDialog.getSaveFileName(
            self,
            "カメラパラメータをcsvで保存",
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            "カメラパラメータ (*.csv)",
        )

        csv_fullpath = Path(csv_fullpath)

        try:
            get_camera_parameter_save_csv_service().save_as_csv(
                solution=self._solution,
                csv_fullpath=csv_fullpath,
            )
        except:
            self._logger.exception(f"Failed to save csv to \"{csv_fullpath}\"")
        else:
            QMessageBox.information(
                self,
                "カメラパラメータのcsvへの保存",
                f"カメラパラメータがcsvに正常に保存されました。\n保存先：{csv_fullpath}",
            )
