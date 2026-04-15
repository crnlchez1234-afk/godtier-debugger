"""
Smoke checks for staging/prod.

Usage examples:
  python scripts/smoke.py --url http://localhost:8000/health --expect-status 200 --expect-json-key status=ok
  python scripts/smoke.py --url http://localhost:8000/api/predict --method POST --body '{"text":"hello"}' --expect-status 200
"""
import argparse
import json
import sys
from typing import Any, Dict, Optional

import requests


def parse_kv(value: str) -> Dict[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected key=value")
    key, val = value.split("=", 1)
    return {key: val}


def request_once(url: str, method: str, body: Optional[str]) -> requests.Response:
    payload: Optional[Any] = None
    headers: Dict[str, str] = {}
    if body:
        try:
            payload = json.loads(body)
            headers["Content-Type"] = "application/json"
        except json.JSONDecodeError:
            payload = body
    resp = requests.request(method=method.upper(), url=url, headers=headers, json=payload if isinstance(payload, dict) else None, data=payload if isinstance(payload, str) else None, timeout=15)
    return resp


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple smoke check")
    parser.add_argument("--url", required=True, help="Target URL (health or endpoint)")
    parser.add_argument("--method", default="GET", help="HTTP method")
    parser.add_argument("--body", help="Request body (JSON string or raw)")
    parser.add_argument("--expect-status", type=int, default=200, help="Expected HTTP status code")
    parser.add_argument("--expect-json-key", action="append", type=parse_kv, help="Expect JSON key=value (repeatable)")
    args = parser.parse_args()

    try:
        resp = request_once(args.url, args.method, args.body)
    except Exception as exc:  # pragma: no cover
        print(f"REQUEST_FAILED: {exc}")
        return 1

    if resp.status_code != args.expect_status:
        print(f"BAD_STATUS expected={args.expect_status} got={resp.status_code}")
        return 1

    if args.expect_json_key:
        try:
            data = resp.json()
        except ValueError:
            print("BAD_JSON: response is not JSON")
            return 1
        for kv in args.expect_json_key:
            for key, val in kv.items():
                actual = data
                for part in key.split("."):
                    if not isinstance(actual, dict) or part not in actual:
                        print(f"MISSING_KEY {key}")
                        return 1
                    actual = actual[part]
                if str(actual) != val:
                    print(f"BAD_VALUE {key} expected={val} got={actual}")
                    return 1

    print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
