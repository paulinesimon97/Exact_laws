from typing import List
from numba import njit

from .abstract_term import AbstractTerm, calc_source_with_numba


class SourceRvbetadu(AbstractTerm):
    def __init__(self):
        pass

    def calc(self, vector: List[int], cube_size: List[int], rho, vx, vy, vz, pm, ppol, dxupol, dyupol, dzupol, **kwarg) -> List[float]:
        return calc_source_with_numba(calc_in_point, *vector, *cube_size, rho, vx, vy, vz, pm, ppol, dxupol, dyupol, dzupol)

    def variables(self) -> List[str]:
        return ["rho", "gradupol", "v", "pm", "ppol"]


def load():
    return SourceRvbetadu()


@njit
def calc_in_point(i, j, k, ip, jp, kp, rho, vx, vy, vz, pm, ppol, dxupol, dyupol, dzupol):
    
    vNPgraduP = vx[i, j, k] * dxupol[ip, jp, kp] + vy[i, j, k] * dyupol[ip, jp, kp] + vz[i, j, k] * dzupol[ip, jp, kp]
    vPgraduNP = vx[ip, jp, kp] * dxupol[i, j, k] + vy[ip, jp, kp] * dyupol[i, j, k] + vz[ip, jp, kp] * dzupol[i, j, k]

    return (
        rho[i, j, k] * pm[ip, jp, kp] / ppol[ip, jp, kp] * vNPgraduP
        + rho[ip, jp, kp] * pm[i, j, k] / ppol[i, j, k] * vPgraduNP
    )