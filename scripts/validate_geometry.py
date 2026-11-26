"""Validate candidate geometry corrections without modifying source data."""
import json
import math
from pathlib import Path
from collections import Counter

ROOT = Path("data/sivalliu")
OUT = Path("geometry-review")
SEAMS = {"R513": 21968, "R515": 22136, "R561": 22007}
# Preferred positions from adjacent stop IDs and physical endpoints, in meters.
PREFERRED = {21694: 2749, 21783: 12235, 21838: 12471, 22201: 12810, 22208: 0}

def xy(p):
    return float(p["longitude"])*109400, float(p["latitude"])*110600

def project(stop, points, preferred=None):
    x,y = xy(stop)
    along = 0
    candidates = []
    for i,(a,b) in enumerate(zip(points, points[1:]),1):
        ax,ay = xy(a)
        bx,by = xy(b)
        u,v = bx-ax,by-ay
        length = math.hypot(u,v)
        if not length:
            continue
        t = max(0,min(1,((x-ax)*u+(y-ay)*v)/(length*length)))
        px,py = ax+t*u,ay+t*v
        candidates.append(dict(distance=math.hypot(x-px,y-py), along=along+t*length,
                               index=i, point={"longitude":str(px/109400),
                               "latitude":str(py/110600),"radius":"0"}))
        along += length
    best = min(candidates,key=lambda q:q["distance"])
    if preferred is not None:
        best = min((q for q in candidates if q["distance"] <= min(50,best["distance"]+10)),
                   key=lambda q:abs(q["along"]-preferred), default=best)
    return best

def main():
    OUT.mkdir(exist_ok=True)
    network = json.loads((ROOT/"network.json").read_text())["data"]
    report = []
    sequences = []
    seen = []
    for route in network["routes"]:
        name = route["short_name"]
        d = json.loads((ROOT/"routes"/(name+".json")).read_text())["data"]
        assert len(d["polyline"]) == 1, name
        go,back = (d["polyline"][0][k] for k in ("go","back"))
        if name == "R561":
            go,back = back,go
        if name in SEAMS:
            s = next(s for s in d["stops"] if s["id"] == SEAMS[name])
            q = project(s,go)
            i,p = q["index"],q["point"]
            go,back = go[:i]+[p],[p]+go[i:]+back
        for heading,points in (("IDA",go),("REGRESO",back)):
            rows = []
            for stop in d["stops"]:
                if stop["heading"] != heading:
                    continue
                q = project(stop,points,PREFERRED.get(stop["id"]) if heading=="IDA" else None)
                rows.append({"stop_id":stop["id"],"stop_name":stop["short_name"],
                             "distance_m":round(q["distance"],3),"along_m":round(q["along"],3)})
                seen.append(stop["id"])
            rows.sort(key=lambda r:r["along_m"])
            for index,row in enumerate(rows,1):
                row["sequence"] = index
            bad = [r for r in rows if r["distance_m"]>50]
            report.append({"route":name,"heading":heading,"count":len(rows),
                           "max_distance_m":max((r["distance_m"] for r in rows),default=None),
                           "exceptions":bad,"candidate_only":True})
            sequences.append({"route":name,"heading":heading,"shape":points,"stops":rows,
                              "needs_review":bool(bad) or len(rows)<2})
    assert Counter(seen)==Counter(s["id"] for s in network["stops"])
    summary = {"stop_count":len(seen),"outside_50m":sum(len(r["exceptions"]) for r in report),
               "directions":report,"status":"candidate geometry, not production GTFS"}
    (OUT/"report.json").write_text(json.dumps(summary,indent=2)+"\n")
    (OUT/"ordered-patterns.json").write_text(json.dumps(sequences,ensure_ascii=False)+"\n")
    print(json.dumps(summary,indent=2))

if __name__ == "__main__":
    main()
