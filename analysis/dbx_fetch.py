#!/usr/bin/env python3
"""Fetch team usage via Databricks SQL Statement Execution API using OAuth M2M."""

import json
import os
import sys
import time
from pathlib import Path

import requests

HOST = os.environ["DBX_ML_RAY_HOSTNAME"].rstrip("/")
if not HOST.startswith("http"):
    HOST = f"https://{HOST}"
WAREHOUSE_ID = os.environ["DBX_ML_RAY_HTTP_PATH"].rsplit("/", 1)[-1]
CLIENT_ID = os.environ["DBX_ML_OAUTH_CLIENT_ID"]
CLIENT_SECRET = os.environ["DBX_ML_OAUTH_CLIENT_SECRET"]

QUERY = """
SELECT e.user_id as owninguser,
       date_format(e.earliest_timestamp, 'yyyy-MM') as month,
       e.requested_model as model_name,
       SUM(e.input_tokens) as input_tokens,
       SUM(e.output_tokens) as output_tokens,
       SUM(e.cache_write_tokens) as cache_write_tokens,
       SUM(e.cache_read_tokens) as cache_read_tokens,
       u.email
FROM main.dbt.int_usage_events e
LEFT JOIN main.dbt.stg_user u ON e.user_id = u.user_id
WHERE e.team_id = 2354493
  AND e.earliest_timestamp >= '2026-02-01'
  AND e.earliest_timestamp < '2026-05-01'
  AND e.has_billable_event = 1
GROUP BY e.user_id, month, e.requested_model, u.email
ORDER BY month, owninguser, model_name
"""


def get_token() -> str:
    resp = requests.post(
        f"{HOST}/oidc/v1/token",
        data={"grant_type": "client_credentials", "scope": "all-apis"},
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_chunk(token: str, statement_id: str, chunk_idx: int):
    r = requests.get(
        f"{HOST}/api/2.0/sql/statements/{statement_id}/result/chunks/{chunk_idx}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def main():
    token = get_token()
    r = requests.post(
        f"{HOST}/api/2.0/sql/statements/",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "statement": QUERY,
            "warehouse_id": WAREHOUSE_ID,
            "wait_timeout": "50s",
            "disposition": "INLINE",
            "format": "JSON_ARRAY",
        },
        timeout=120,
    )
    r.raise_for_status()
    payload = r.json()
    sid = payload["statement_id"]

    # Poll if PENDING/RUNNING
    while payload["status"]["state"] in ("PENDING", "RUNNING"):
        time.sleep(3)
        r = requests.get(
            f"{HOST}/api/2.0/sql/statements/{sid}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=60,
        )
        r.raise_for_status()
        payload = r.json()

    if payload["status"]["state"] != "SUCCEEDED":
        print(f"Query failed: {payload['status']}", file=sys.stderr)
        sys.exit(1)

    # Collect rows across chunks
    rows = []
    result = payload.get("result", {})
    rows.extend(result.get("data_array", []))
    next_idx = result.get("next_chunk_index")
    while next_idx is not None:
        chunk = fetch_chunk(token, sid, next_idx)
        rows.extend(chunk.get("data_array", []))
        next_idx = chunk.get("next_chunk_index")

    cols = ["owninguser", "month", "model_name",
            "input_tokens", "output_tokens",
            "cache_write_tokens", "cache_read_tokens", "email"]
    out = [dict(zip(cols, row)) for row in rows]
    out_path = Path(__file__).parent / "usage_data.json"
    with open(out_path, "w") as f:
        json.dump(out, f)
    print(f"Saved {len(out)} rows to {out_path}")


if __name__ == "__main__":
    main()
