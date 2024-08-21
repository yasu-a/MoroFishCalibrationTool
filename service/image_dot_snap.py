from domain.project import Project
from util.dot_snap import DotSnapComputer


class ImageDotSnapService:
    def __init__(self, project: Project):
        self._computer = DotSnapComputer(
            im_gray=project.camera_image.gray,
            crop_radius=30,
            min_samples=5,
            snap_radius=100,
            stride=10,
        )

    def get_snap_pos(
            self,
            *,
            current_pos: tuple[float, float],
    ) -> tuple[float, float] | None:  # スナップできない場合はNone
        return self._computer.find_snap_pos((int(current_pos[0]), int(current_pos[1])))
