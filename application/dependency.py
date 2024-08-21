import functools

from application.current_project import get_current_project
from service.camera_parameter_save_csv import CameraParameterSaveCSVService
from service.equation import EquationSolveService
from service.image_dot_snap import ImageDotSnapService


@functools.cache  # スコープ：プロジェクト
def get_image_dot_snap_service() -> ImageDotSnapService:
    return ImageDotSnapService(
        project=get_current_project(),
    )


@functools.cache  # スコープ：プロジェクト
def get_equation_solve_service() -> EquationSolveService:
    return EquationSolveService(
        project=get_current_project(),
    )


@functools.cache  # スコープ：プロジェクト
def get_camera_parameter_save_csv_service() -> CameraParameterSaveCSVService:
    return CameraParameterSaveCSVService()
