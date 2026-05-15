#!/usr/bin/env python3
import json, sys
from pathlib import Path

def _cell_value(cell):
    if cell.get("string_value") is not None:
        return cell["string_value"]
    if cell.get("str") is not None:
        return cell["str"]
    return None

def parse_mcp_rows(data_array):
    rows = []
    for item in data_array:
        vals = [_cell_value(v) for v in item["values"]]
        rows.append({
            "month_start": vals[0],
            "owninguser": int(vals[1]) if vals[1] is not None else None,
            "email": vals[2],
            "status_quo_cost": float(vals[3]) if vals[3] is not None else 0.0,
            "all_anthropic_cost": float(vals[4]) if vals[4] is not None else 0.0,
            "optimized_cost": float(vals[5]) if vals[5] is not None else 0.0,
        })
    return rows

if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    payload = json.loads(src.read_text())
    result = payload["result"]
    key = "data_typed_array" if "data_typed_array" in result else "data_array"
    rows = parse_mcp_rows(result[key])
    dst.write_text(json.dumps(rows, indent=2))
    print(f"Wrote {len(rows)} rows to {dst}")
