from domain.camera_image import CameraImage
from domain.image_points import ImagePointMapping
from domain.option import Options


class Project:
    def __init__(
            self,
            *,
            camera_image: CameraImage,
            image_points: ImagePointMapping,
            options: Options,
    ):
        self._camera_image = camera_image
        self._image_points = image_points
        self._options = options

    @property
    def camera_image(self) -> CameraImage:
        return self._camera_image

    @property
    def image_points(self) -> ImagePointMapping:
        return self._image_points

    @property
    def options(self) -> Options:
        return self._options

    @options.setter
    def options(self, value):
        self._options = value
