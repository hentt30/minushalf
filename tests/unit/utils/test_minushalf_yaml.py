"""
Test the class that leads with the minushalf.yaml file,
the input file for the execute command
"""
import pytest
from minushalf.utils import MinushalfYaml
from minushalf.data import (
    Softwares,
    VaspDefaultParams,
    AtomicProgramDefaultParams,
    CorrectionDefaultParams,
)


def test_default_parameters():
    """
    Test minushalf.yaml class withou pass
    parameters, so all parameters
    are set to default
    """
    file = MinushalfYaml.from_file()
    assert file.software == Softwares.vasp.value
    assert file.software_configurations[str(
        VaspDefaultParams.number_of_cores)] == 4
    assert file.software_configurations[str(VaspDefaultParams.path)] == "vasp"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.exchange_correlation_code)] == "pb"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.calculation_code)] == "ae"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.max_iterations)] == 100
    assert file.correction[str(CorrectionDefaultParams.correction_code)] == "v"
    assert file.correction[str(
        CorrectionDefaultParams.potfiles_folder)] == "minushalf_potfiles"


def test_minushalf_without_filling_correction(file_path):
    """
    Test minushalf.yaml class without filling
    correction section in minushalf.yaml
    """
    minushalf_path = file_path(
        "/minushalf_yaml/minushalf_partially_filled.yaml")
    file = MinushalfYaml.from_file(minushalf_path)
    assert file.software == Softwares.vasp.value
    assert file.software_configurations[str(
        VaspDefaultParams.number_of_cores)] == 6
    assert file.software_configurations[str(
        VaspDefaultParams.path)] == "../vasp"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.exchange_correlation_code)] == "wi"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.calculation_code)] == "ae"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.max_iterations)] == 200
    assert file.correction[str(CorrectionDefaultParams.correction_code)] == "v"
    assert file.correction[str(
        CorrectionDefaultParams.potfiles_folder)] == "minushalf_potfiles"


def test_minushalf_filled_out(file_path):
    """
    Test minushalf.yaml class with all
    parameters modified
    """
    minushalf_path = file_path("/minushalf_yaml/minushalf_filled_out.yaml")
    file = MinushalfYaml.from_file(minushalf_path)
    assert file.software == Softwares.vasp.value
    assert file.software_configurations[str(
        VaspDefaultParams.number_of_cores)] == 6
    assert file.software_configurations[str(
        VaspDefaultParams.path)] == "../vasp"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.exchange_correlation_code)] == "wi"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.calculation_code)] == "ae"
    assert file.atomic_program[str(
        AtomicProgramDefaultParams.max_iterations)] == 200
    assert file.correction[str(
        CorrectionDefaultParams.correction_code)] == "vf"
    assert file.correction[str(
        CorrectionDefaultParams.potfiles_folder)] == "../potcar"


@pytest.mark.xfail
def test_minushalf_wrong_software_name(file_path):
    """
    Test minushalf.yaml passing
    a wrong software name
    """
    minushalf_path = file_path(
        "/minushalf_yaml/minushalf_invalid_software.yaml")
    MinushalfYaml.from_file(minushalf_path)


@pytest.mark.xfail
def test_minushalf_wrong_correction_code_name(file_path):
    """
    Test minushalf.yaml passing
    a invalid correction code
    """
    minushalf_path = file_path(
        "/minushalf_yaml/minushalf_invalid_correction_code.yaml")
    MinushalfYaml.from_file(minushalf_path)
