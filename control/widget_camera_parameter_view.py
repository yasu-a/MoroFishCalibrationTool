from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPlainTextEdit

from dto.equation_solution import CameraParameterSolution
from util.fonts import font


class CameraParameterViewWidget(QWidget):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._init_ui()
        self._init_signals()

    def _init_ui(self):
        layout_root = QVBoxLayout()
        self.setLayout(layout_root)

        layout_root.addWidget(QLabel("カメラのパラメータ"))

        self._te_python = QPlainTextEdit(self)
        self._te_python.setFont(font(monospace=True, small=True))
        self._te_python.setReadOnly(True)
        self._te_python.setFixedHeight(100)
        layout_root.addWidget(self._te_python)

    def _init_signals(self):
        pass

    def set_data(self, solution: CameraParameterSolution):
        if solution.is_valid():
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
            self._te_python.setPlainText("")
