#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
import requests

COST_QUERY = open(Path(__file__).with_name('cost_query.sql')).read()

def token():
    host = os.environ['DBX_ML_RAY_HOSTNAME']
    r = requests.post(
        f'https://{host}/oidc/v1/token',
        data={'grant_type': 'client_credentials', 'scope': 'all-apis'},
        auth=(os.environ['DBX_ML_OAUTH_CLIENT_ID'], os.environ['DBX_ML_OAUTH_CLIENT_SECRET']),
        timeout=30,
    )
    r.raise_for_status()
    return r.json()['access_token']

def run_query(statement: str):
    host = os.environ['DBX_ML_RAY_HOSTNAME']
    warehouse_id = os.environ['DBX_ML_RAY_HTTP_PATH'].split('/')[-1]
    headers = {'Authorization': f'Bearer {token()}'}
    r = requests.post(
        f'https://{host}/api/2.0/sql/statements/',
        headers=headers,
        json={'warehouse_id': warehouse_id, 'statement': statement, 'wait_timeout': '50s'},
        timeout=120,
    )
    r.raise_for_status()
    payload = r.json()
    while payload.get('status', {}).get('state') in ('PENDING', 'RUNNING'):
        time.sleep(2)
        sid = payload['statement_id']
        r = requests.get(f'https://{host}/api/2.0/sql/statements/{sid}', headers=headers, timeout=60)
        r.raise_for_status()
        payload = r.json()
    if payload.get('status', {}).get('state') != 'SUCCEEDED':
        raise RuntimeError(payload)
    result = payload.get('result', {})
    data = result.get('data_array') or []
    cols = [c['name'] for c in payload['manifest']['schema']['columns']]
    rows = []
    for item in data:
        vals = item if isinstance(item, list) else [v.get('string_value') for v in item['values']]
        row = dict(zip(cols, vals))
        row['month_start'] = row['month_start']
        row['owninguser'] = int(row['owninguser'])
        for k in ['status_quo_cost', 'all_anthropic_cost', 'optimized_cost']:
            row[k] = float(row[k])
        rows.append(row)
    return rows

if __name__ == '__main__':
    out = Path(sys.argv[1] if len(sys.argv) > 1 else 'team_9109857_costs.json')
    rows = run_query(COST_QUERY)
    out.write_text(json.dumps(rows, indent=2))
    print(f'Wrote {len(rows)} rows to {out}')
