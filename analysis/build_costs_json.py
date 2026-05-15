#!/usr/bin/env python3
"""Build team_9109857_costs.json from MCP poll result file."""

import json
import sys
from pathlib import Path

from export_costs import parse_mcp_rows


def main() -> None:
    src = Path(sys.argv[1])
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "analysis/team_9109857_costs.json")
    payload = json.loads(src.read_text())
    result = payload["result"]
    key = "data_typed_array" if "data_typed_array" in result else "data_array"
    rows = parse_mcp_rows(result[key])
    out.write_text(json.dumps(rows, indent=2))
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
