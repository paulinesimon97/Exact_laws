from typing import List
from numba import njit
import sympy as sp

from .abstract_term import AbstractTerm, calc_source_with_numba

class Bg17Vwv(AbstractTerm):
    def __init__(self):
        self.set_sympy_expr()
        self.fct = sp.lambdify(
            sp.symbols(
                ("vx'", "vy'", "vz'",
                 "vx", "vy", "vz",
                 "wx'", "wy'", "wz'",
                 "wx", "wy", "wz"
                )),
            self.expr,
            "numpy",
        )
        
    def set_sympy_expr(self):
        vxP, vyP, vzP = sp.symbols(("vx'", "vy'", "vz'"))
        vxNP, vyNP, vzNP = sp.symbols(("vx", "vy", "vz"))
        wxP, wyP, wzP = sp.symbols(("wx'", "wy'", "wz'"))
        wxNP, wyNP, wzNP = sp.symbols(("wx", "wy", "wz"))

        dvx = vxP - vxNP
        dvy = vyP - vyNP
        dvz = vzP - vzNP

        vXwxP = vyP * wzP - vzP * wyP  
        vXwyP = vzP * wxP - vxP * wzP  
        vXwzP = vxP * wyP - vyP * wxP  
        vXwxNP = vyNP * wzNP - vzNP * wyNP  
        vXwyNP = vzNP * wxNP - vxNP * wzNP  
        vXwzNP = vxNP * wyNP - vyNP * wxNP

        self.expr = (vXwxP - vXwxNP) * dvx + (vXwyP - vXwyNP) * dvy + (vXwzP - vXwzNP) * dvz
        
    def calc(self, vector:List[int], cube_size:List[int], vx, vy, vz, wx, wy, wz, **kwarg) -> List[float]:
        #return calc_source_with_numba(calc_in_point, *vector, *cube_size, vx, vy, vz, wx, wy, wz)
        return calc_source_with_numba(calc_in_point_with_sympy, *vector, *cube_size, vx, vy, vz, wx, wy, wz)

    def variables(self) -> List[str]:
        return ['w','v']

def load():
    return Bg17Vwv()

def print_expr():
    sp.init_printing(use_latex=True)
    return Bg17Vwv().expr


@njit
def calc_in_point_with_sympy(i, j, k, ip, jp, kp, 
                             vx, vy, vz, 
                             wx, wy, wz,
                             f=njit(Bg17Vwv().fct)):
    vxP, vyP, vzP = vx[ip, jp, kp], vy[ip, jp, kp], vz[ip, jp, kp]
    vxNP, vyNP, vzNP = vx[i, j, k], vy[i, j, k], vz[i, j, k]
    wxP, wyP, wzP = wx[ip, jp, kp], wy[ip, jp, kp], wz[ip, jp, kp]
    wxNP, wyNP, wzNP = wx[i, j, k], wy[i, j, k], wz[i, j, k]
    return f(
        vxP, vyP, vzP, 
        vxNP, vyNP, vzNP, 
        wxP, wyP, wzP, 
        wxNP, wyNP, wzNP
    )
       
@njit
def calc_in_point(i, j, k, ip, jp, kp, vx, vy, vz, wx, wy, wz):
    
    dvx = vx[ip,jp,kp] - vx[i,j,k]
    dvy = vy[ip,jp,kp] - vy[i,j,k]
    dvz = vz[ip,jp,kp] - vz[i,j,k]
    
    vXwxP = vy[ip,jp,kp] * wz[ip,jp,kp] - vz[ip,jp,kp] * wy[ip,jp,kp]  
    vXwyP = vz[ip,jp,kp] * wx[ip,jp,kp] - vx[ip,jp,kp] * wz[ip,jp,kp]  
    vXwzP = vx[ip,jp,kp] * wy[ip,jp,kp] - vy[ip,jp,kp] * wx[ip,jp,kp]  
    vXwxNP = vy[i,j,k] * wz[i,j,k] - vz[i,j,k] * wy[i,j,k]  
    vXwyNP = vz[i,j,k] * wx[i,j,k] - vx[i,j,k] * wz[i,j,k]  
    vXwzNP = vx[i,j,k] * wy[i,j,k] - vy[i,j,k] * wx[i,j,k]  
    
    return (vXwxP - vXwxNP) * dvx + (vXwyP - vXwyNP) * dvy + (vXwzP - vXwzNP) * dvz