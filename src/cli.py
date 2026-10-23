#!/usr/bin/env python3
"""
CLI adapter for gpower-clone adhering to CONTRACT.md specification.
"""

import sys
import json
from typing import Dict, Any
from src.engine import calculate_t2_indep, EngineError

CONTRACT_VERSION = "1.0.0"
TEAM_NAME = "K1-Team"
ENGINE_INFO = f"Python {sys.version.split()[0]} with scipy"


def parse_args(args: list) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--"):
            key = arg[2:].replace("-", "_")
            if key == "version":
                return {"_version": True}
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                val_str = args[i + 1]
                # parse numeric if possible
                if key in ("tails", "n1", "n2", "df", "groups", "predictors"):
                    try:
                        params[key] = int(val_str)
                    except ValueError:
                        params[key] = val_str
                elif key in ("d", "dz", "f", "w", "f2", "alpha", "power", "ratio", "beta_alpha_ratio"):
                    try:
                        params[key] = float(val_str)
                    except ValueError:
                        params[key] = val_str
                else:
                    params[key] = val_str
                i += 2
            else:
                # boolean or missing value
                params[key] = True
                i += 1
        else:
            i += 1
    return params


def main():
    args = sys.argv[1:]
    params = parse_args(args)

    if params.get("_version"):
        ver_resp = {
            "contract_version": CONTRACT_VERSION,
            "name": TEAM_NAME,
            "engine": ENGINE_INFO
        }
        sys.stdout.write(json.dumps(ver_resp) + "\n")
        sys.exit(0)

    test_id = params.get("test")
    mode_id = params.get("mode")

    if not test_id:
        err = {"error": "Test parametresi (--test) zorunludur", "code": "MISSING_PARAM", "field": "test"}
        sys.stdout.write(json.dumps(err) + "\n")
        sys.exit(2)

    if test_id != "t2-indep":
        err = {"error": f"Bu takım yalnızca t2-indep test ailesini gerçekler. İstenen: {test_id}", "code": "UNSUPPORTED_TEST", "field": "test"}
        sys.stdout.write(json.dumps(err) + "\n")
        sys.exit(2)

    if not mode_id:
        err = {"error": "Mod parametresi (--mode) zorunludur", "code": "MISSING_PARAM", "field": "mode"}
        sys.stdout.write(json.dumps(err) + "\n")
        sys.exit(2)

    # Clean params dict for engine (remove test, mode, internal flags)
    clean_params = {k: v for k, v in params.items() if not k.startswith("_")}

    try:
        result = calculate_t2_indep(mode_id, clean_params)
        sys.stdout.write(json.dumps(result) + "\n")
        sys.exit(0)
    except EngineError as e:
        sys.stdout.write(json.dumps(e.to_dict()) + "\n")
        sys.exit(e.exit_code)
    except Exception as e:
        err = {"error": f"İç hesaplama hatası: {str(e)}", "code": "INTERNAL_ERROR"}
        sys.stdout.write(json.dumps(err) + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
