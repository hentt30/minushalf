"""
Test make_minushalf_results function
in utils
"""
import os
from minushalf.utils import make_minushalf_results


def test_only_valence_cuts(file_path):
    """
    Test function only with valence cuts
    """
    expected_file_path = file_path(
        "/minushalf_results/minushalf_results_only_valence_cuts.dat")
    valence_cuts = {
        "Ag": 1.23,
        "Br": 2.33,
    }
    gap = 2.334
    filename = "minushalf_results_only_valence_cuts.dat"
    make_minushalf_results(valence_cuts=valence_cuts, gap=gap, name=filename)

    try:
        expected_file = open(expected_file_path, "r")
        file = open(filename, "r")
        assert expected_file.read() == file.read()
    finally:
        expected_file.close()
        file.close()
        os.remove(filename)


def test_conduction_cuts(file_path):
    """
    Test function only with valence and conduction cuts
    """
    expected_file_path = file_path(
        "/minushalf_results/minushalf_results_conduction_cuts.dat")
    valence_cuts = {
        "Ag": 1.23,
        "Br": 2.33,
    }
    conduction_cuts = {
        "Ag": 1.23,
        "Br": 2.33,
    }
    gap = 2.334
    filename = "minushalf_results_conduction_cuts.dat"
    make_minushalf_results(
        valence_cuts=valence_cuts,
        gap=gap,
        conduction_cuts=conduction_cuts,
        name=filename,
    )
    try:
        expected_file = open(expected_file_path, "r")
        file = open(filename, "r")
        assert expected_file.read() == file.read()
    finally:
        expected_file.close()
        file.close()
        os.remove(filename)
