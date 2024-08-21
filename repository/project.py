from domain.camera_image import CameraImage
from domain.image_points import ImagePointMapping
from domain.option import Options
from domain.project import Project


class ProjectRepository:
    def __init__(self):
        pass

    @staticmethod
    def create(*, camera_image: CameraImage) -> Project:
        return Project(
            camera_image=camera_image,
            image_points=ImagePointMapping.create_default(),
            options=Options.create_default(),
        )
