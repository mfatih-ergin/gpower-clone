"""
MCP (Model Context Protocol) server for gpower-clone.
Adheres strictly to CONTRACT.md Section 7.
Wraps the core engine without duplicating calculation logic.
"""

import sys
import json
import asyncio
from typing import Optional
from mcp.server.mcpserver import MCPServer
from src.engine import calculate_t2_indep, EngineError

server = MCPServer("gpower-clone-mcp")


@server.tool(name="power_analysis", description="Statistical power and sample size calculation matching G*Power 3.1.9.7")
def power_analysis(
    test: str,
    mode: str,
    tails: Optional[int] = None,
    d: Optional[float] = None,
    alpha: Optional[float] = None,
    power: Optional[float] = None,
    ratio: Optional[float] = None,
    n1: Optional[int] = None,
    n2: Optional[int] = None,
    beta_alpha_ratio: Optional[float] = None
) -> str:
    """
    Executes power analysis tool for G*Power clone.
    Returns single-line JSON string identical to CLI stdout.
    """
    if test != "t2-indep":
        err = {"error": f"Desteklenmeyen test ailesi: {test}", "code": "UNSUPPORTED_TEST", "field": "test"}
        return json.dumps(err)

    params = {}
    candidates = {
        "tails": tails,
        "d": d,
        "alpha": alpha,
        "power": power,
        "ratio": ratio,
        "n1": n1,
        "n2": n2,
        "beta_alpha_ratio": beta_alpha_ratio
    }
    for k, v in candidates.items():
        if v is not None:
            params[k] = v

    try:
        res = calculate_t2_indep(mode, params)
        return json.dumps(res)
    except EngineError as e:
        return json.dumps(e.to_dict())
    except Exception as e:
        err = {"error": f"İç hesaplama hatası: {str(e)}", "code": "INTERNAL_ERROR"}
        return json.dumps(err)


def main():
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
