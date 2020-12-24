"""
Leads with input file (INP.ae)
read by atomic program.
"""
from __future__ import annotations
import re
import numpy as np
from pathlib import Path
from minushalf.utils import (drop_comments, ElectronicDistribution,
                             parse_valence_orbitals, PeriodicTable)


class InputFile:
    """
    Parses input file.
    """
    def __init__(self,
                 exchange_correlation_type: str,
                 calculation_code: str,
                 chemical_symbol: str,
                 esoteric_line: str,
                 number_valence_orbitals: int,
                 number_core_orbitals: int,
                 valence_orbitals: list,
                 description: str = "",
                 last_lines: list = None) -> None:
        """
        Args:
            chemical_symbol (str): Symbol of the chemical element (H, He, Li...)

            esoteric_line (str):  Its use is somewhat esoteric and for most 
            calculations it should contain just a 0.0 in the position shown. 
            
            exchange_correlation_type (str): functional of exchange and correlation
            ((r)ca(s), (r)wi(s), (r)hl(s), (r)gl(s) ,(r)bh(s), (r)pb(s), (r)rp(s), (r)rv(s), (r)bl(s))
            
            calculation code (str): Calculation code for inp file (ae)
            
            number_valence_orbitals (int): Number of orbitals in valence
            
            number_core_orbitals (int): Number of orbitals in the core
            
            valence_orbitals (list): list of dictionaries with the following
            properties: {"n": principal quantum number,"l":secondary quantum number,
            "occupation": occupation in the level}

            last_lines (list): any line or property that comes after 
            electronic distribution
        """
        self.exchange_correlation_type = exchange_correlation_type
        self.calculation_code = calculation_code
        self.description = description
        self.chemical_symbol = chemical_symbol
        self.esoteric_line = esoteric_line
        self.number_core_orbitals = number_core_orbitals
        self.number_valence_orbitals = number_valence_orbitals
        self.valence_orbitals = valence_orbitals
        if not last_lines:
            self.last_lines = []
        else:
            self.last_lines = last_lines

    @property
    def chemical_symbol(self) -> str:
        """
        Returns:
            Chemical symbol of the element (H, He, Li...)
        """
        return self._chemical_symbol

    @chemical_symbol.setter
    def chemical_symbol(self, symbol: str) -> None:
        """
        Verify if the symbol is a valid periodic table element and 
        format the string correctly.

        Args:
            symbol (str): chemical symbol of the element (H, He, Li...)
        """

        try:
            PeriodicTable[symbol]
        except KeyError:
            raise ValueError("The chemical symbol passed is not correct")

        self._chemical_symbol = symbol.capitalize()

    @property
    def exchange_correlation_type(self) -> str:
        """
        Returns:
            Functional of exchange and correlation
            ((r)ca(s), (r)wi(s), (r)hl(s), (r)gl(s) ,(r)bh(s), (r)pb(s), (r)rp(s), (r)rv(s), (r)bl(s))
        """
        return self._exchange_correlation_type

    @exchange_correlation_type.setter
    def exchange_correlation_type(self,
                                  exchange_correlation_type: str) -> None:
        """
        Verify if the functional of  exchange and correlation is valid
        conforms the ATOM documentation

        Args:
            exchange_correlation_type (str): functional of exchange and correlation
            ((r)ca(s), (r)wi(s), (r)hl(s), (r)gl(s) ,(r)bh(s), (r)pb(s), (r)rp(s), (r)rv(s), (r)bl(s))
        """
        validation_regex = re.compile(r"(ca|wi|hl|gl|bh|pb|rp|rv|bl)(s|r)?")
        if not validation_regex.match(exchange_correlation_type):
            raise ValueError(
                "Your value of exchange and correlation functional is not valid"
            )

        self._exchange_correlation_type = exchange_correlation_type

    @property
    def calculation_code(self) -> str:
        """
        Returns:
            Calculation code for inp file (ae)
        """
        return self._calculation_code

    @calculation_code.setter
    def calculation_code(self, calculation_code: str) -> None:
        """
        Verify if the calculation is valid
        conforms the ATOM documentation

        Args:
            calculation code (str): Calculation code for inp file (ae)
        """
        validation_regex = re.compile(r"(ae)")
        if not validation_regex.match(calculation_code):
            raise ValueError("Your value of calculation is not valid")

        self._calculation_code = calculation_code

    def electron_occupation(self, electron_fraction: float,
                            secondary_quantum_number: int) -> None:
        """
        Corrects the input file of the atomic program,
        decreasing a fraction of the electron in a 
        layer specified by the secondary quantum number

            Args:
                electron_fraction (float): Fraction of the electron 
                that will be decreased in the INP file. Can vary between 0 and 0.5

                secondary_quantum_number (int): Specifies the layer on which 
                the occupation is to be made.
        """
        for value in reversed(self.valence_orbitals):

            is_equal = np.isclose(value["occupation"][0],
                                  0.0,
                                  rtol=1e-04,
                                  atol=1e-08,
                                  equal_nan=False)

            if (not is_equal and value["l"] == secondary_quantum_number):
                value["occupation"][0] -= electron_fraction
                break
        else:
            raise Exception(
                "Trouble with occupation. Please verify the parameters passed and the INP file."
            )

    def to_stringlist(self) -> list:
        """
            Returns:
                List with the lines of the INP file.
        """
        input_lines = []
        input_lines.append("   {}      {}\n".format(self.calculation_code,
                                                    self.description))
        input_lines.append(" n={}".format(self.chemical_symbol))
        if len(self.chemical_symbol) == 2:
            input_lines.append(" c={}\n".format(
                self.exchange_correlation_type))
        else:
            input_lines.append("  c={}\n".format(
                self.exchange_correlation_type))
        input_lines.append(self.esoteric_line)

        if self.number_core_orbitals <= 9:
            input_lines.append("    {}    {}\n".format(
                self.number_core_orbitals, self.number_valence_orbitals))
        else:
            input_lines.append("   {}    {}\n".format(
                self.number_core_orbitals, self.number_valence_orbitals))

        for orbital in self.valence_orbitals:
            occupation = "      ".join(
                ["{:.2f}".format(value) for value in orbital["occupation"]])
            input_lines.append("    {}    {}      {}\n".format(
                orbital["n"], orbital["l"], occupation))

        for line in self.last_lines:
            input_lines.append(line)

        return input_lines

    def to_file(self, filename: str = "./INP") -> None:
        """
        Write INP file
            Args:
                filename (str): name of the output file 
        """

        with open(filename, "w") as input_file:
            lines = self.to_stringlist()
            input_file.writelines(lines)

    @staticmethod
    def from_file(filename: str = "./INP") -> InputFile:
        """
        Parse INP.ae file.

            Args:
                filename: name of the INP file.
            Returns:
                input_file: instance of InputFile class.
        """
        with open(filename) as input_file:

            lines_without_comments = drop_comments(input_file.readlines())

            try:
                calculation_code = lines_without_comments[0].split()[0]
                description = " ".join(lines_without_comments[0].split()[1:])
            except:
                raise ValueError(
                    "Description or calculation code not provided")

            try:
                chemical_symbol = lines_without_comments[1].split()[0].split(
                    '=')[1]
                exchange_correlation_type = lines_without_comments[1].split(
                )[1].split('=')[1]
            except:
                raise ValueError(
                    "Chemical symbol or exchange correlation not provided")

            esoteric_line = lines_without_comments[2]

            try:
                number_core_orbitals = int(
                    lines_without_comments[3].split()[0])
                number_valence_orbitals = int(
                    lines_without_comments[3].split()[1])
            except:
                raise ValueError(
                    "Number of core orbitals or number of valence orbitals not provided"
                )

            try:
                valence_orbitals = [
                    parse_valence_orbitals(lines_without_comments[i])
                    for i in range(4, 4 + number_valence_orbitals)
                ]
            except:
                raise ValueError("Valence orbitals do not provided correctly")

            last_lines = lines_without_comments[4 + number_valence_orbitals:]

            return InputFile(exchange_correlation_type, calculation_code,
                             chemical_symbol, esoteric_line,
                             number_valence_orbitals, number_core_orbitals,
                             valence_orbitals, description, last_lines)

    @staticmethod
    def minimum_setup(chemical_symbol: str,
                      exchange_correlation_type: str,
                      maximum_iterations: int = 100,
                      calculation_code: str = "ae") -> InputFile:
        """
        Create INP file with minimum setup.

            Args:
            chemical_symbol (str): Symbol of the chemical element (H, He, Li...).
            
            exchange_correlation_type (str): functional of exchange and correlation
            ((r)ca(s), (r)wi(s), (r)hl(s), (r)gl(s) ,(r)bh(s), (r)pb(s), (r)rp(s), (r)rv(s), (r)bl(s))

            maximum_iterations (int): Maximum number of iterations for atomic program.
            The default is 100

            Returns:
                input_file: instance of InputFile class.
        """
        description = "{}".format(chemical_symbol)
        esoteric_line = "       0.0       0.0       0.0       0.0       0.0       0.0\n"
        last_lines = ["{} maxit\n".format(maximum_iterations)]

        try:
            electronic_distribution = ElectronicDistribution[
                chemical_symbol].value
        except:
            raise ValueError("This element its not available in our database")
        number_core_orbitals = int(electronic_distribution[0].split()[0])
        number_valence_orbitals = int(electronic_distribution[0].split()[1])
        valence_orbitals = [
            parse_valence_orbitals(orbital)
            for orbital in electronic_distribution[1:]
        ]

        return InputFile(exchange_correlation_type, calculation_code,
                         chemical_symbol, esoteric_line,
                         number_valence_orbitals, number_core_orbitals,
                         valence_orbitals, description, last_lines)
