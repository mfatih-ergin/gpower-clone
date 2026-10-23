"""
Tests proving equivalence between CLI/Engine output and MCP tool output.
Requirement: CONTRACT.md Section 7.
"""

import pytest
import json
import asyncio
from src.engine import calculate_t2_indep
from src.mcp_server import server

TEST_VECTORS = [
    {
        "test": "t2-indep",
        "mode": "a-priori",
        "tails": 1,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.95,
        "ratio": 1.0
    },
    {
        "test": "t2-indep",
        "mode": "a-priori",
        "tails": 2,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.95,
        "ratio": 1.0
    },
    {
        "test": "t2-indep",
        "mode": "post-hoc",
        "tails": 1,
        "d": 0.5,
        "alpha": 0.05,
        "n1": 88,
        "n2": 88
    },
    {
        "test": "t2-indep",
        "mode": "compromise",
        "tails": 1,
        "d": 0.5,
        "beta_alpha_ratio": 1.0,
        "n1": 88,
        "n2": 88
    },
    {
        "test": "t2-indep",
        "mode": "criterion",
        "tails": 1,
        "d": 0.5,
        "power": 0.95,
        "n1": 88,
        "n2": 88
    },
    {
        "test": "t2-indep",
        "mode": "sensitivity",
        "tails": 1,
        "alpha": 0.05,
        "power": 0.95,
        "n1": 88,
        "n2": 88
    }
]


def test_mcp_cli_exact_equivalence():
    async def _run():
        for vec in TEST_VECTORS:
            mode = vec["mode"]
            clean_args = {k: v for k, v in vec.items() if k not in ("test", "mode")}
            
            # 1. Direct engine output (what CLI outputs)
            engine_res = calculate_t2_indep(mode, clean_args)
            
            # 2. MCP tool call output
            mcp_res = await server.call_tool("power_analysis", vec)
            mcp_raw_text = mcp_res.content[0].text
            mcp_data = json.loads(mcp_raw_text)

            # 3. Assert exact equivalence
            assert mcp_data == engine_res, f"Mismatch for vector {vec}: MCP={mcp_data}, Engine={engine_res}"

    asyncio.run(_run())
