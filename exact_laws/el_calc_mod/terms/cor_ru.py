from typing import List
from numba import njit
import sympy as sp

from .abstract_term import AbstractTerm, calc_source_with_numba

class CorRu(AbstractTerm):
    def __init__(self):
        self.set_sympy_expr()
        self.fct = sp.lambdify(
            sp.symbols(
                ("rho'","rho",
                 "u'", "u"
                )),
            self.expr,
            "numpy",)

    def set_sympy_expr(self):
        rhoP, rhoNP = sp.symbols(("rho'", "rho"))
        uP, uNP = sp.symbols(("u'", "u"))

        self.expr =  (rhoP*uNP+rhoNP*uP)/2  

    def calc(
        self, vector: List[int], cube_size: List[int], rho,  ugyr, **kwarg
    ) -> List[float]:
        return calc_source_with_numba(
            calc_in_point_with_sympy, *vector, *cube_size, rho,  ugyr)

    def variables(self) -> List[str]:
        return [ "rho", "ugyr"]
    
    def print_expr(self):
        sp.init_printing(use_latex=True)
        return self.expr


def load():
    return CorRu()


def print_expr():
    return CorRu().print_expr()


@njit
def calc_in_point_with_sympy(i, j, k, ip, jp, kp, 
                             rho,
                             u, 
                             f=njit(CorRu().fct)):
    
    
    rhoP, rhoNP = rho[ip, jp, kp], rho[i, j, k]
    uP, uNP = u[ip, jp, kp], u[i, j, k]
    
    return f(rhoP, rhoNP,
        uP, uNP
    )