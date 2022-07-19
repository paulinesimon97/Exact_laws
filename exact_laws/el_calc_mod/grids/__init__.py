from typing import Dict
from warnings import warn
import importlib
import logging
import numpy as np

from .grid import Grid
from ...mathematical_tools.derivation import cdiff

def load_grid(N=[], L=[], c=[], axis=[], coords={}):
    if len(N) == 0 and len(L) == 0 and len(c) == 0 and len(coords.keys()) == 0: 
        raise Exception('Impossible to creat an empty grid, add at least the axis or the coordinates argument or two between N, L and c')
    if len(axis) == 0 and (len(c) != 0 or len(N) != 0 or len(L) != 0) and len(coords.keys()) == 0:
        warn("WARNING: The names of the axis of the grid are not defined, it will be by default ['axis_0',...]"
             "If it is not your intention, add axis in the arguments.")
        nb_axis = len(N) * (len(N) != 0) + (len(N) == 0) * (len(L) * (len(L) != 0) + len(c) * (len(L) == 0))    
        axis = [f"axis_{i}" for i in range(nb_axis)]
    if len(axis) == 0 and len(N) == 0 and len(coords.keys()) != 0 : 
        axis = [k for k in coords.keys() if len(coords[k]) != 0]
        N = [len(coords[k]) for k in coords.keys() if len(coords[k]) != 0]
    if len(c) == 0 and len(N) != 0 and len(L) != 0:
        warn('WARNING: The grid is only defined with N and L, c is by default computed as L/(N-1). If it is not your intention, add c in the arguments.')
        c = [L[i]/(N[i]-1) for i in range(len(N))]
    return Grid(N = N, L = L, c = c, axis = axis, coords = coords) 

def load_grid_from_dict(dict: Dict):
        return Grid(N=dict['N'].astype(int),L=dict['L'],c=dict['c'])   

def load_incgrid_from_grid(coord, **kargs):
    """
    Args:
        coord (str): nom du module (type de grille)
        if coord is logcyl, kargs must contain at least: 
            - original_grid (Grid object with attributes N, L and c)
            - Nmax_scale (int)
            - Nmax_list (int) 
            - kind (str) : cls or rdm
    Returns:
        IncGrid object
    """
    mod = importlib.import_module(f"exact_laws.el_calc_mod.grids.{coord}", "*")
    return mod.load(**kargs)

def load_listgrid_from_incgrid(coord, incgrid, nb_sec_by_dirr):
    """
    Args:
        coord (str): nom du module (type de grille)
        incgrid (IncGrid object)
        nb_sec_by_dirr (int) : 0, 1, 2 
    Returns:
        Grid object that contains list of coordinates
    """
    mod = importlib.import_module(f"exact_laws.el_calc_mod.grids.{coord}", "*")
    coords = {}
    coords['listprim'], coords['listsec'], coords['nb_sec_by_dirr'] = mod.build_listcoords(incgrid, nb_sec_by_dirr)    
    return load_grid(axis=['listprim','listsec'], N=[len(coords['listprim']),len(coords['listsec'])], coords=coords)

def coordinate_sec_in_primsec_grid(vect_prim,list_prim,list_sec,nb_sec_by_dirr,N):
    points_sec = [[], [], []]
    for dirr in range(3):
        for i in range(-nb_sec_by_dirr, nb_sec_by_dirr + 1):
            if not i == 0:
                vect = list(vect_prim)
                vect[dirr] = (
                    (vect[dirr] + i)
                    - (N[dirr] * ((vect[dirr] + i) >= (N[dirr] / 2)))
                    + (N[dirr] * ((vect[dirr] + i) <= (-N[dirr] / 2)))
                )
                vect = tuple(vect)
                loc = -1
                try:
                    index = list_prim.index(vect)
                    loc = 0
                except:
                    index = list_sec.index(vect)
                    loc = 1
                points_sec[dirr].append((loc, index))
    return points_sec
    
def div_on_incgrid(incgrid, dataset_terms):
    logging.info("INIT Calculation of the divergence")
    list_prim = dataset_terms.grid.coords['listprim']
    list_sec = dataset_terms.grid.coords['listsec']
    nb_sec_by_dirr = dataset_terms.grid.coords['nb_sec_by_dirr']
    N = incgrid.spatial_grid.N
    c = incgrid.spatial_grid.c
    
    output = {}
    list_flux = []
    for t in dataset_terms.quantities:
        if t.startswith("flux"):
            output["div_" + t] = np.zeros((len(list_prim)))
            list_flux.append(t)

    for ind, vect_prim in enumerate(list_prim):
        points_sec = coordinate_sec_in_primsec_grid(vect_prim,list_prim, list_sec, nb_sec_by_dirr,N)
        for t in list_flux:
            div_point = 0
            if len(points_sec[0]) == 0:
                div_point += np.nan
            else:
                for dirr in range(3):
                    values = []
                    for i in range(len(points_sec[dirr])):
                        values.append(dataset_terms.quantities[t][points_sec[dirr][i][0]][points_sec[dirr][i][1]][dirr])
                    div_point += cdiff(
                        tab = values,
                        length_case=c[dirr],
                        precision=nb_sec_by_dirr * 2,
                        period=False,
                        point=True,
                    )
            output["div_" + t][ind] = div_point
    logging.info("END Calculation of the divergence")
    return output

def reorganise_quantities(coord, incgrid, output_grid, output_quantities, nb_sec_by_dirr=1):
    mod = importlib.import_module(f"exact_laws.el_calc_mod.grids.{coord}", "*")
    return mod.reorganise_quantities(incgrid, output_grid, output_quantities, nb_sec_by_dirr)

def reformat_grid_compatible_to_h5(coord, incgrid):
    mod = importlib.import_module(f"exact_laws.el_calc_mod.grids.{coord}", "*")
    return mod.reformat_grid_compatible_to_h5(incgrid)
