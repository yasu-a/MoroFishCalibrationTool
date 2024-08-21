from pathlib import Path

import pandas as pd

from dto.equation_solution import CameraParameterSolution


class CameraParameterSaveCSVService:
    def __init__(self):
        pass

    def save_as_csv(
            self,
            *,
            solution: CameraParameterSolution,
            csv_fullpath: Path,
    ) -> None:
        values = solution.values()
        df = pd.DataFrame(values)
        df.to_csv(csv_fullpath, index=False, header=False, float_format="%.15f")
