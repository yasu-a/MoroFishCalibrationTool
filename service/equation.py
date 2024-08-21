import numpy as np
import sympy
from sympy import symbols, Eq, solve

from domain.project import Project
from dto.equation_solution import CameraParameterSolution


class EquationSolveService:
    def __init__(self, project: Project):
        self._project = project

    # noinspection PyPep8Naming
    @staticmethod
    def _solve_equations_matrix(points: np.ndarray) -> dict[sympy.Symbol, float]:
        # 未知数
        a = np.array(symbols('a11 a12 a13 a14 a21 a22 a23 a24 a31 a32 a33'))

        # 行列の初期化
        A = np.zeros((len(points) + sum(1 for _, _, _, _, v in points if v is not None), 11))
        B = np.zeros((len(points) + sum(1 for _, _, _, _, v in points if v is not None), 1))

        # 行列AとBの構築
        row_index = 0
        for x, y, z, u, v in points:
            A[row_index, 0:4] = [x, y, z, 1]
            A[row_index, 8:11] = [-u * x, -u * y, -u * z]
            B[row_index, 0] = u
            row_index += 1

        for x, y, z, u, v in points:
            if v is not None:
                A[row_index, 4:8] = [x, y, z, 1]
                A[row_index, 8:11] = [-v * x, -v * y, -v * z]
                B[row_index, 0] = v
                row_index += 1

        # 行列Aの擬似逆行列を計算
        A_pseudo_inv = np.linalg.pinv(A)

        # パラメータの解を計算
        solution_matrix = np.dot(A_pseudo_inv, B)

        # 解を辞書形式に変換
        solution = {a_ij: float(solution_matrix[i, 0]) for i, a_ij in enumerate(a)}

        # noinspection PyTypeChecker
        return solution

    def solve_camera_parameters(self) -> CameraParameterSolution | None:
        points = self._project.image_points.points_array
        try:
            solution = self._solve_equations_matrix(points)
        except np.linalg.LinAlgError:
            return None
        else:
            return CameraParameterSolution(
                solution=solution,
            )

    @staticmethod
    def _solve_equations_laser(points: np.ndarray):
        # 未知数
        b11, b12, b13 = symbols('b11 b12 b13')

        # 連立方程式の作成
        equations = [
            Eq(x * b11 + y * b12 + z * b13 + 1, 0) for x, y, z in points
        ]

        # 連立方程式の解
        solution = solve(equations, (b11, b12, b13))
        # 解を少数に変換
        decimal_solution = {var: val.evalf() for var, val in solution.items()}

        return decimal_solution
