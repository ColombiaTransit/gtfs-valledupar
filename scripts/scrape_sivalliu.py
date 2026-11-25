"""Collect public Valledupar transit network and route details."""
import json
import hashlib
import time
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

URL = "https://android.valliu.co/api/transport-network"
BASE = {"city": "valledupar", "lat": "10.4750", "long": "-73.2500"}
EXPECTED = set("R-TUR R100 R101 R214 R313 R316 R412 R513 R561 R562 R515 R515N R313L R513L R561DA".split())

def post(payload):
    for attempt in range(3):
        try:
            req = Request(URL, data=json.dumps(payload).encode(), headers={
                "Accept": "application/json", "Content-Type": "application/json",
                "User-Agent": "ColombiaTransit static transit research"}, method="POST")
            with urlopen(req, timeout=60) as response:
                raw = response.read()
            return raw, json.loads(raw)["data"]
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
            retry = exc.headers.get("Retry-After", "")
            time.sleep(max(5 * 2**attempt, int(retry)) if retry.isdigit() else 5 * 2**attempt)
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(5 * 2**attempt)

def save(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()

def main():
    out = Path("snapshot")
    out.mkdir(exist_ok=True)
    raw, network = post(dict(BASE, stops_and_route=True))
    routes, stops = network["routes"], network["stops"]
    names = [r["short_name"] for r in routes]
    if not names or len(set(names)) != len(names) or not isinstance(stops, list):
        raise ValueError("Invalid network")
    report = {"source": URL, "collected_at": datetime.now(timezone.utc).isoformat(),
              "network_sha256": save(out / "network.json", raw),
              "network_stop_records": len(stops), "missing_baseline": sorted(EXPECTED-set(names)),
              "new_routes": sorted(set(names)-EXPECTED), "routes": [], "errors": []}
    for route in routes:
        name = route["short_name"]
        time.sleep(2)
        try:
            if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
                raise ValueError("Invalid route name")
            raw, d = post(dict(BASE, route_short_name=name, with_stops=True,
                               with_polyline=True, with_route=True))
            if d.get("short_name") != name or d.get("id") != route["id"]:
                raise ValueError("Route identity mismatch")
            sha = save(out / "routes" / (name + ".json"), raw)
            shapes = d.get("polyline") or []
            entry = {"name": name, "id": route["id"], "sha256": sha,
                     "advertised_stops": route.get("stops_number"),
                     "shape_points": {k: sum(len(p.get(k) or []) for p in shapes) for k in ("go", "back")},
                     "response_keys": sorted(d),
                     "list_counts": {k: len(v) for k,v in d.items() if isinstance(v,list)}}
            report["routes"].append(entry)
            print(json.dumps(entry), flush=True)
        except (ValueError, KeyError, TypeError, AttributeError, URLError, TimeoutError) as exc:
            report["errors"].append({"route": name, "error": str(exc)})
            if isinstance(exc, HTTPError) and exc.code in (401,403,429):
                break
    report["complete"] = len(report["routes"]) == len(routes) and not report["errors"] and not report["missing_baseline"]
    (out / "manifest.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
    if not report["complete"]:
        raise SystemExit("Incomplete snapshot; see manifest")

if __name__ == "__main__":
    main()
