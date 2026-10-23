"""
Differential testing suite for gpower-clone (t2-indep).
Compares output against G*Power oracle vectors from CONTRACT.md and SPEC.md.
"""

import pytest
import math
from src.engine import calculate_t2_indep, EngineError

TOLERANCE = 1e-6


def assert_close(actual: float, expected: float, name: str):
    diff = abs(actual - expected)
    rel = diff / max(abs(expected), 1e-12)
    assert diff <= TOLERANCE or rel <= TOLERANCE, f"{name} mismatch: actual={actual}, expected={expected}, diff={diff}"


class TestContractVectors:
    """Verifies against the 5 open vectors published by instructor in CONTRACT.md"""

    def test_a_priori(self):
        params = {"tails": 1, "d": 0.5, "alpha": 0.05, "power": 0.95, "ratio": 1.0}
        res = calculate_t2_indep("a-priori", params)
        
        # Exact integer matching
        assert res["n1"] == 88
        assert res["n2"] == 88
        assert res["n_total"] == 176
        assert res["df"] == 174
        
        # Decimal matching within 1e-6
        assert_close(res["ncp"], 3.3166248, "ncp")
        assert_close(res["critical_t"], 1.6536580, "critical_t")
        assert_close(res["actual_power"], 0.9514254, "actual_power")

    def test_post_hoc(self):
        params = {"tails": 1, "d": 0.5, "alpha": 0.05, "n1": 88, "n2": 88}
        res = calculate_t2_indep("post-hoc", params)

        assert res["df"] == 174
        assert_close(res["ncp"], 3.3166248, "ncp")
        assert_close(res["critical_t"], 1.6536580, "critical_t")
        assert_close(res["power"], 0.9514254, "power")

    def test_compromise(self):
        params = {"tails": 1, "d": 0.5, "beta_alpha_ratio": 1.0, "n1": 88, "n2": 88}
        res = calculate_t2_indep("compromise", params)

        assert res["df"] == 174
        assert_close(res["ncp"], 3.3166248, "ncp")
        assert_close(res["critical_t"], 1.6606859, "critical_t")
        assert_close(res["alpha"], 0.0492887, "alpha")
        assert_close(res["beta"], 0.0492887, "beta")
        assert_close(res["power"], 0.9507113, "power")

    def test_criterion(self):
        params = {"tails": 1, "d": 0.5, "power": 0.95, "n1": 88, "n2": 88}
        res = calculate_t2_indep("criterion", params)

        assert res["df"] == 174
        assert_close(res["ncp"], 3.3166248, "ncp")
        assert_close(res["critical_t"], 1.6676050, "critical_t")
        assert_close(res["alpha"], 0.0485965, "alpha")

    def test_sensitivity(self):
        params = {"tails": 1, "alpha": 0.05, "power": 0.95, "n1": 88, "n2": 88}
        res = calculate_t2_indep("sensitivity", params)

        assert res["df"] == 174
        assert_close(res["ncp"], 3.3025887, "ncp")
        assert_close(res["critical_t"], 1.6536580, "critical_t")
        assert_close(res["d"], 0.4978840, "d")


class TestBoundaryAndUnequalRatios:
    """Verifies edge cases, unequal ratios, and error behaviors"""

    def test_two_tailed_a_priori(self):
        params = {"tails": 2, "d": 0.5, "alpha": 0.05, "power": 0.95, "ratio": 1.0}
        res = calculate_t2_indep("a-priori", params)
        assert res["n1"] == 105
        assert res["n2"] == 105
        assert res["n_total"] == 210
        assert res["df"] == 208
        assert_close(res["critical_t"], 1.9714347, "critical_t")
        assert_close(res["ncp"], 3.6228442, "ncp")
        assert res["actual_power"] >= 0.95

    def test_unequal_ratio_a_priori(self):
        # ratio = 2.0 (Group 2 has twice the size of Group 1)
        params = {"tails": 2, "d": 0.5, "alpha": 0.05, "power": 0.80, "ratio": 2.0}
        res = calculate_t2_indep("a-priori", params)
        assert res["n2"] == math.ceil(res["n1"] * 2.0)
        assert res["n_total"] == res["n1"] + res["n2"]
        assert res["actual_power"] >= 0.80

    def test_missing_param_error(self):
        with pytest.raises(EngineError) as exc_info:
            calculate_t2_indep("a-priori", {"tails": 1, "d": 0.5, "alpha": 0.05, "power": 0.95})
        assert exc_info.value.code == "MISSING_PARAM"
        assert exc_info.value.field == "ratio"

    def test_inconsistent_power_error(self):
        with pytest.raises(EngineError) as exc_info:
            calculate_t2_indep("a-priori", {"tails": 1, "d": 0.5, "alpha": 0.05, "power": 0.04, "ratio": 1.0})
        assert exc_info.value.code == "INCONSISTENT"
        assert exc_info.value.field == "power"

    def test_out_of_range_tails(self):
        with pytest.raises(EngineError) as exc_info:
            calculate_t2_indep("a-priori", {"tails": 3, "d": 0.5, "alpha": 0.05, "power": 0.95, "ratio": 1.0})
        assert exc_info.value.code == "OUT_OF_RANGE"
        assert exc_info.value.field == "tails"
