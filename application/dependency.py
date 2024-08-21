import functools

from application.current_project import get_current_project
from repository.project import ProjectRepository
from service.camera_parameter_save_csv import CameraParameterSaveCSVService
from service.equation import EquationSolveService
from service.image_dot_snap import ImageDotSnapService
from service.project_create import ProjectCreateService


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


@functools.cache  # スコープ：プロジェクト
def get_project_repository() -> ProjectRepository:
    return ProjectRepository()


@functools.cache  # スコープ：プロジェクト
def get_project_service() -> ProjectCreateService:
    return ProjectCreateService(
        project_repo=get_project_repository(),
    )
