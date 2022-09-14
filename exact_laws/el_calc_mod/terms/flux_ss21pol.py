from typing import List
from numba import njit
import sympy as sp

from .abstract_term import calc_flux_with_numba
from .flux_ss21 import FluxSs21, calc_in_point_with_sympy

class FluxSs21Pol(FluxSs21):
    def __init__(self):
        FluxSs21.__init__(self)
    
    def calc(self, vector:List[int], cube_size:List[int], vx, vy, vz, bx, by, bz, rho, upol, **kwarg) -> List[float]:
        return calc_flux_with_numba(calc_in_point_with_sympy, *vector, *cube_size, vx, vy, vz, bx, by, bz, rho, upol)

    def variables(self) -> List[str]:
        return ['v', 'b', 'rho', 'upol']

def load():
    return FluxSs21Pol()

def print_expr():
    return FluxSs21Pol().print_expr()
