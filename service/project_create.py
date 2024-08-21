from pathlib import Path

import cv2

from domain.camera_image import CameraImage
from domain.project import Project
from repository.project import ProjectRepository


class ProjectCreateService:
    def __init__(self, project_repo: ProjectRepository):
        self._project_repo = project_repo

    def create_from_image_fullpath(self, im_fullpath: Path) -> Project:
        im_bgr = cv2.imread(str(im_fullpath), cv2.IMREAD_COLOR)
        im_gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
        camera_image = CameraImage(im_bgr=im_bgr, im_gray=im_gray)
        return self._project_repo.create(camera_image=camera_image)
