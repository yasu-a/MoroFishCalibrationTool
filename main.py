from pathlib import Path

from PyQt5.QtCore import QStandardPaths
from PyQt5.QtWidgets import QApplication, QFileDialog

from application.current_project import set_current_project
from application.debug import set_debug, is_debug
from control.window_main import MainWindow
from domain.project import Project
from util.app_logging import create_logger
from util.fonts import font

if __name__ == '__main__':
    import sys

    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        # noinspection PyProtectedMember
        sys._excepthook(exctype, value, traceback)  # type: ignore
        sys.exit(1)


    sys.excepthook = exception_hook

logger = create_logger()

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == "--debug":
        set_debug(True)

    app = QApplication(sys.argv)
    # noinspectionPyA rgumentList
    app.setFont(font())
    app.setStyle('Fusion')

    # 画像ファイルを開いてもらう
    if is_debug():
        filepath = Path(r"~\Downloads\measurement_calib_01_000.jpg").expanduser()
    else:
        filepath, _ = QFileDialog.getOpenFileName(
            None,
            "画像を開く",
            QStandardPaths.writableLocation(QStandardPaths.PicturesLocation),
            "画像ファイル (*.png *.jpg *.jpeg)",
        )
        filepath = filepath.strip()
        if filepath is None:
            sys.exit()
        filepath = Path(filepath)
        if not filepath.is_file():
            sys.exit()

    # プロジェクト生成
    project = Project.create_new_from_image_filepath(filepath)
    set_current_project(project)

    window = MainWindow()
    # noinspection PyUnresolvedReferences
    window.show()
    sys.exit(app.exec_())
