"""
Analyze VTOTAL
"""
from __future__ import annotations
import re
from itertools import islice, chain
import numpy as np


class Vtotal():
    """
    Output for ATOM that contains the
    pseudopotential generated by an atom
    """
    def __init__(self, radius: np.array, down_potential: np.array) -> None:
        """
            Args:

                radius (np.array): rays for which the potential calculations will be made made.

                down_potential (np.array): potentials calculated to the state of spin Down for
                each value of radius
        """
        self.vtotal_header_size = 1
        self.radius = radius
        self.down_potential = down_potential

    @staticmethod
    def from_file(filename: str = './VTOTAL.ae') -> Vtotal:
        """
        Parse VTOTAL and extract the following informations
        """
        radius = Vtotal.read_radius(filename)
        down_potential = Vtotal.read_down_potential(filename)
        return Vtotal(radius, down_potential)

    @staticmethod
    def read_down_potential(filename: str) -> np.array:
        """
        Extracts the potentials related to the state
        of spin Down calculated for the main elements
            Args:
                filename (str): Name of the VTOTAL file
        """

        with open(filename, 'r') as vtotal:
            initial_regex = re.compile(r"^.*Down\s+potential\s+follows")
            for line in vtotal:
                if initial_regex.match(line):
                    break
            else:
                raise ValueError(
                    "Potential informations do not found in vtotal")

            stop_regex = re.compile(r"^.*Up\s+potential\s+follows")
            down_potential = []
            vtotal_header_size = 1  # Skip the line containing the spin value

            for line in islice(vtotal, vtotal_header_size, None):

                if stop_regex.match(line):
                    down_potential = list(chain.from_iterable(down_potential))
                    return np.array(down_potential, dtype=np.float)

                down_potential.append(line.split())

    @staticmethod
    def read_radius(filename: str) -> np.array:
        """
        Extracts from the file information regarding the rays for
        which the potential calculations will be made made.
            Args:
                filename (str): Name of the VTOTAL file
        """

        with open(filename, 'r') as vtotal:
            radius = []
            vtotal_header_size = 1  # Skip the header Raios
            stop_regex = re.compile(r"^.*Down\s+potential\s+follows")
            for line in islice(vtotal, vtotal_header_size, None):

                if stop_regex.match(line):
                    radius = list(chain.from_iterable(radius))
                    return np.array(radius, dtype=np.float)

                radius.append(line.split())
