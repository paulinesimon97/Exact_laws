from typing import List

from .abstract_law import AbstractLaw


class Ss22Cgl(AbstractLaw):
    def __init__(self):
        self.terms = [
            "flux_drvdvdv",
            "flux_drbdbdv",
            "flux_drvdbdb",
            "flux_drbdvdb",
            "flux_drducgldv",
            "flux_drdpperpcgldv",
            "flux_drdpancgldv",
            "flux_drdpmdv",
            "source_rvdvdv",
            "source_rbdbdv",
            "source_bdrbdv",
            "source_rducgldv",
            "source_rdpperpcgldv",
            "source_rdpancgldv",
            "source_rvdbdb",
            "source_rbdvdb",
            "source_bdrvdb",
            "source_pmvdrdr",
            "source_pperpcglvdrdr",
            "source_pancglvdrdr",
            "source_rvdpmdr",
            "source_rvdpperpcgldr",
            "source_rvdpancgldr"
        ]
        pass

    def terms_and_coeffs(self, physical_params):
        coeffs = {}
        coeffs["div_flux_drvdvdv"] = - 1 / 4
        coeffs["div_flux_drbdbdv"] = - 1 / 4
        coeffs["div_flux_drvdbdb"] = 1 / 4
        coeffs["div_flux_drbdvdb"] = 1 / 4
        coeffs["div_flux_drducgldv"] = - 1 / 2
        coeffs["div_flux_drdpperpcgldv"] = 1 / 4
        coeffs["div_flux_drdpancgldv"] = 1 / 4
        coeffs["div_flux_drdpmdv"] = 1 / 4
        coeffs["source_rvdvdv"] = - 1 / 4
        coeffs["source_rbdbdv"] = - 1 / 8
        coeffs["source_bdrbdv"] = 1 / 8
        coeffs["source_rducgldv"] = - 1 / 2
        coeffs["source_rdpperpcgldv"] = 1 / 2
        coeffs["source_rdpancgldv"] = 1 / 2
        coeffs["source_rvdbdb"] = 1 / 2
        coeffs["source_rbdvdb"] = 1 / 4
        coeffs["source_bdrvdb"] = -1 / 4   
        coeffs["source_pmvdrdr"] = -1 / 4   
        coeffs["source_pperpcglvdrdr"] = -1 / 4   
        coeffs["source_pancglvdrdr"] = -1 / 4 
        coeffs["source_rvdpmdr"] = 1 / 4   
        coeffs["source_rvdpperpcgldr"] = 1 / 4    
        coeffs["source_rvdpancgldr"] = 1 / 4  
        return self.terms, coeffs

    def variables(self) -> List[str]:
        return self.list_variables(self.terms)


def load():
    return Ss22Cgl()