"""
Software abstract Factory
"""
from abc import ABC, abstractmethod
from .potential_file import PotentialFile
from .band_projection_file import BandProjectionFile


class SoftwaresAbstractFactory(ABC):
    """
    Abstract Factory for create instances for
    each supported software.
    """
    @abstractmethod
    def get_atoms_map(self, filename: str, base_path: str = None) -> dict:
        """
        Abstract method for returns a map
        of the atomic symbol to its index.
        """

    @abstractmethod
    def get_band_projection_class(
        self,
        filename: str,
        base_path: str = None,
    ) -> BandProjectionFile:
        """
        Abstract method for returns the class that
        handles with the projections of atoms orbitals
        in the bands.
        """

    @abstractmethod
    def get_fermi_energy(self, filename: str, base_path: str = None) -> float:
        """
        Abstract method for returna
        energy of the fermi level.
        """

    @abstractmethod
    def get_number_of_bands(self, filename: str, base_path: str = None) -> int:
        """
        Abstract method for returns the number of bands used in the calculation
        """

    @abstractmethod
    def get_number_of_kpoints(self,
                              filename: str,
                              base_path: str = None) -> int:
        """
        Abstract method for returns the number of kpoints used in the calculation
        """

    @abstractmethod
    def get_potential_class(self,
                            filename: str,
                            base_path: str = None) -> PotentialFile:
        """
        Abstract method for returns the potential class
        """

    @abstractmethod
    def get_eigenvalues(self, filename: str, base_path: str = None) -> dict:
        """
        Abstract method for returns eigenvalues
        for each band and each kpoint
        """
