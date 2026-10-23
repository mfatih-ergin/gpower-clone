"""
gpower-clone calculation engine for t2-indep test family.
Clean-room implementation based strictly on SPEC.md and CONTRACT.md.
Authors citation: Faul, Erdfelder, Lang, and Buchner (2007, 2009).
"""

import math
from typing import Dict, Any, Tuple
from scipy.stats import t, nct, norm
from scipy.optimize import brentq


class EngineError(Exception):
    def __init__(self, message: str, code: str, field: str = "", exit_code: int = 2):
        super().__init__(message)
        self.message = message
        self.code = code
        self.field = field
        self.exit_code = exit_code

    def to_dict(self) -> Dict[str, Any]:
        res = {"error": self.message, "code": self.code}
        if self.field:
            res["field"] = self.field
        return res


def compute_t2_power(tails: int, df: int, delta: float, critical_t: float) -> float:
    """Computes statistical power for two-sample independent t-test."""
    if tails == 1:
        return float(1.0 - nct.cdf(critical_t, df, delta))
    else:
        # Two-tailed power incorporates both rejection regions
        return float((1.0 - nct.cdf(critical_t, df, delta)) + nct.cdf(-critical_t, df, delta))


def validate_common(params: Dict[str, Any], required_fields: Tuple[str, ...]) -> None:
    # Check missing fields
    for f in required_fields:
        if f not in params or params[f] is None:
            raise EngineError(f"Gerekli alan eksik: {f}", code="MISSING_PARAM", field=f, exit_code=2)

    # Check unknown fields
    allowed = set(required_fields) | {"test", "mode"}
    for k in params.keys():
        if k not in allowed:
            raise EngineError(f"Tanınmayan ya da bu mod için gereksiz alan: {k}", code="UNKNOWN_PARAM", field=k, exit_code=2)

    # Validate tails
    if "tails" in params:
        tails = params["tails"]
        if not isinstance(tails, int) or tails not in (1, 2):
            raise EngineError("tails 1 ya da 2 olmalıdır", code="OUT_OF_RANGE", field="tails", exit_code=2)

    # Validate d
    if "d" in params:
        d = params["d"]
        if not isinstance(d, (int, float)) or d <= 0:
            raise EngineError("Effect size d sıfırdan büyük olmalıdır", code="OUT_OF_RANGE", field="d", exit_code=2)

    # Validate alpha
    if "alpha" in params:
        alpha = params["alpha"]
        if not isinstance(alpha, (int, float)) or not (0.0 < alpha < 1.0):
            raise EngineError("alpha 0 ile 1 arasında olmalıdır", code="OUT_OF_RANGE", field="alpha", exit_code=2)

    # Validate power
    if "power" in params:
        pwr = params["power"]
        if not isinstance(pwr, (int, float)) or not (0.0 < pwr < 1.0):
            raise EngineError("power 0 ile 1 arasında olmalıdır", code="OUT_OF_RANGE", field="power", exit_code=2)
        if "alpha" in params and pwr <= params["alpha"]:
            raise EngineError("power, alpha değerinden büyük olmalıdır", code="INCONSISTENT", field="power", exit_code=2)

    # Validate ratio
    if "ratio" in params:
        ratio = params["ratio"]
        if not isinstance(ratio, (int, float)) or ratio <= 0:
            raise EngineError("Allocation ratio sıfırdan büyük olmalıdır", code="OUT_OF_RANGE", field="ratio", exit_code=2)

    # Validate n1, n2
    for n_field in ("n1", "n2"):
        if n_field in params:
            val = params[n_field]
            if not isinstance(val, int) or val < 2:
                raise EngineError(f"{n_field} en az 2 olmalıdır", code="OUT_OF_RANGE", field=n_field, exit_code=2)

    # Validate beta_alpha_ratio
    if "beta_alpha_ratio" in params:
        bar = params["beta_alpha_ratio"]
        if not isinstance(bar, (int, float)) or bar <= 0:
            raise EngineError("beta_alpha_ratio sıfırdan büyük olmalıdır", code="OUT_OF_RANGE", field="beta_alpha_ratio", exit_code=2)


def calculate_t2_indep(mode: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main dispatch engine for t2-indep test family.
    Supports modes: a-priori, post-hoc, compromise, criterion, sensitivity.
    """
    if mode == "a-priori":
        required = ("tails", "d", "alpha", "power", "ratio")
        validate_common(params, required)
        
        tails = int(params["tails"])
        d = float(params["d"])
        alpha = float(params["alpha"])
        target_power = float(params["power"])
        ratio = float(params["ratio"])

        # Initial sample size estimate via normal approximation
        z_alpha = norm.ppf(1.0 - alpha / tails)
        z_beta = norm.ppf(target_power)
        n1_approx = int(((z_alpha + z_beta) / d) ** 2 * (1.0 + ratio) / ratio)
        n1 = max(2, n1_approx - 25)

        # Iterative search for smallest integer n1 achieving target power
        while True:
            n2 = math.ceil(n1 * ratio)
            df = n1 + n2 - 2
            delta = d * math.sqrt((n1 * n2) / (n1 + n2))
            crit_t = float(t.ppf(1.0 - alpha / tails, df))
            act_power = compute_t2_power(tails, df, delta, crit_t)

            if act_power >= target_power:
                return {
                    "ncp": delta,
                    "critical_t": crit_t,
                    "df": df,
                    "n1": n1,
                    "n2": n2,
                    "n_total": n1 + n2,
                    "actual_power": act_power
                }
            n1 += 1

    elif mode == "post-hoc":
        required = ("tails", "d", "alpha", "n1", "n2")
        validate_common(params, required)

        tails = int(params["tails"])
        d = float(params["d"])
        alpha = float(params["alpha"])
        n1 = int(params["n1"])
        n2 = int(params["n2"])

        df = n1 + n2 - 2
        delta = d * math.sqrt((n1 * n2) / (n1 + n2))
        crit_t = float(t.ppf(1.0 - alpha / tails, df))
        power_val = compute_t2_power(tails, df, delta, crit_t)

        return {
            "ncp": delta,
            "critical_t": crit_t,
            "df": df,
            "power": power_val
        }

    elif mode == "compromise":
        required = ("tails", "d", "beta_alpha_ratio", "n1", "n2")
        validate_common(params, required)

        tails = int(params["tails"])
        d = float(params["d"])
        q = float(params["beta_alpha_ratio"])
        n1 = int(params["n1"])
        n2 = int(params["n2"])

        df = n1 + n2 - 2
        delta = d * math.sqrt((n1 * n2) / (n1 + n2))

        def obj(tc: float) -> float:
            alpha_val = tails * float(1.0 - t.cdf(tc, df))
            beta_val = float(nct.cdf(tc, df, delta))
            if tails == 2:
                beta_val -= float(nct.cdf(-tc, df, delta))
            return beta_val - q * alpha_val

        crit_t = float(brentq(obj, 0.001, 20.0))
        alpha_res = float(tails * (1.0 - t.cdf(crit_t, df)))
        beta_res = float(nct.cdf(crit_t, df, delta))
        if tails == 2:
            beta_res -= float(nct.cdf(-crit_t, df, delta))

        return {
            "ncp": delta,
            "critical_t": crit_t,
            "df": df,
            "alpha": alpha_res,
            "beta": beta_res,
            "power": 1.0 - beta_res
        }

    elif mode == "criterion":
        required = ("tails", "d", "power", "n1", "n2")
        validate_common(params, required)

        tails = int(params["tails"])
        d = float(params["d"])
        target_power = float(params["power"])
        n1 = int(params["n1"])
        n2 = int(params["n2"])

        df = n1 + n2 - 2
        delta = d * math.sqrt((n1 * n2) / (n1 + n2))

        def obj(tc: float) -> float:
            pwr = compute_t2_power(tails, df, delta, tc)
            return pwr - target_power

        crit_t = float(brentq(obj, 0.001, 25.0))
        alpha_res = float(tails * (1.0 - t.cdf(crit_t, df)))

        return {
            "ncp": delta,
            "critical_t": crit_t,
            "df": df,
            "alpha": alpha_res
        }

    elif mode == "sensitivity":
        required = ("tails", "alpha", "power", "n1", "n2")
        validate_common(params, required)

        tails = int(params["tails"])
        alpha = float(params["alpha"])
        target_power = float(params["power"])
        n1 = int(params["n1"])
        n2 = int(params["n2"])

        df = n1 + n2 - 2
        crit_t = float(t.ppf(1.0 - alpha / tails, df))

        def obj(delta_val: float) -> float:
            pwr = compute_t2_power(tails, df, delta_val, crit_t)
            return pwr - target_power

        delta_res = float(brentq(obj, 0.0001, 30.0))
        d_res = delta_res / math.sqrt((n1 * n2) / (n1 + n2))

        return {
            "ncp": delta_res,
            "critical_t": crit_t,
            "df": df,
            "d": d_res
        }

    else:
        raise EngineError(f"Desteklenmeyen mod: {mode}", code="UNSUPPORTED_MODE", exit_code=2)
