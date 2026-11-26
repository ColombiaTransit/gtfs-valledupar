"""Research-only GraphHopper travel time probe for R513L."""
import json
import math
import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import requests
from shapely.geometry import LineString, Point
from pyproj import Transformer

OUT = Path("build/r513l-travel-times")
TRANS = Transformer.from_crs("EPSG:4326", "EPSG:32618", always_xy=True)
DWELL = 15
VIA_STEP = 150
TOL = 50

def read(path):
    return json.loads(Path(path).read_text())

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + "\n")

def line(points):
    return LineString([TRANS.transform(*p) for p in points])

def sample(g, step=10):
    n = max(1, math.ceil(g.length / step))
    return [g.interpolate(g.length * i / n) for i in range(n+1)]

def check(reference, actual):
    a = max(p.distance(actual) for p in sample(reference))
    b = max(p.distance(reference) for p in sample(actual))
    ratio = actual.length / reference.length
    return {"reference_m": round(reference.length, 1), "routed_m": round(actual.length, 1),
            "reference_to_routed_max_m": round(a, 1), "routed_to_reference_max_m": round(b, 1),
            "length_ratio": round(ratio, 4), "accepted": max(a,b) <= TOL and .85 <= ratio <= 1.15}

def slice_line(g, a, b):
    from shapely.ops import substring
    return substring(g, a, b)

def endpoint():
    u = urlsplit(os.environ["GRAPHHOPPER_URL"])
    if u.scheme not in ("http","https") or not u.netloc:
        raise ValueError("Invalid GraphHopper configuration")
    p = u.path.rstrip("/")
    if p.endswith(("/route","/info")):
        p = p.rsplit("/",1)[0]
    return urlunsplit((u.scheme,u.netloc,p+"/route",u.query,""))

def route(session, ref):
    inv = Transformer.from_crs("EPSG:32618","EPSG:4326",always_xy=True)
    pts = [list(inv.transform(p.x,p.y)) for p in sample(ref,VIA_STEP)]
    try:
        r = session.post(endpoint(), json={"profile":"bus","points":pts,
            "points_encoded":False,"instructions":False,"calc_points":True,
            "ch.disable":True}, timeout=(10,90), allow_redirects=False)
        if r.status_code != 200:
            return None, {"error":"HTTP_"+str(r.status_code)}
        path = r.json()["paths"][0]
        actual = line(path["points"]["coordinates"])
        qa = check(ref,actual)
        sec = float(path["time"])/1000
        qa.update({"via_points":len(pts),"travel_seconds":round(sec,3)})
        if not math.isfinite(sec) or sec <= 0:
            qa["accepted"] = False
        return sec,qa
    except (requests.RequestException, KeyError, IndexError, ValueError, TypeError):
        return None,{"error":"routing_or_response_failure"}

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    cfg=read("research/r513l-candidate-patterns.json")
    src=read("data/sivalliu/routes/R513L.json")["data"]["polyline"][0]
    session=requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept":"application/json, text/plain, */*","Accept-Language":"en-US,en;q=0.9","Cache-Control":"no-cache","Pragma":"no-cache","Sec-Fetch-Mode":"cors","Sec-Fetch-Dest":"empty"})
    results=[]; diagnostics=[]; failed=0
    for p in cfg["patterns"]:
        k=p["shape_direction"]
        g=line([(float(s["longitude"]),float(s["latitude"])) for s in src[k]])
        stops=p["stops"]
        chain=[g.project(Point(TRANS.transform(s["lon"],s["lat"]))) for s in stops]
        t=0; times=[{"source_stop_id":stops[0]["source_stop_id"],"arrival_offset":0,"departure_offset":0}]
        valid=True
        for i,(a,b) in enumerate(zip(chain,chain[1:])):
            qa={"accepted":False,"error":"non_increasing_chainage"}
            sec=None
            if b>a:
                sec,qa=route(session,slice_line(g,a,b))
            diagnostics.append({"direction":k,"from":stops[i]["source_stop_id"],"to":stops[i+1]["source_stop_id"],**qa})
            if not qa.get("accepted"):
                failed+=1; valid=False
            if valid:
                t+=max(1,math.ceil(sec))
                arr=t
                if i+1<len(stops)-1: t+=DWELL
                times.append({"source_stop_id":stops[i+1]["source_stop_id"],"arrival_offset":arr,"departure_offset":t})
        results.append({"direction":k,"accepted":valid,"stops":times if valid else [],"total_seconds":t if valid else None})
    write("routing-validation.json",diagnostics)
    write("travel-times.json",{"route_id":"R513","shape_source":"R513L","status":"candidate_not_production","dwell_seconds":DWELL,"patterns":results})
    summary={"segments":len(diagnostics),"rejected":failed,"patterns":[{"direction":r["direction"],"accepted":r["accepted"],"total_seconds":r["total_seconds"]} for r in results]}
    write("routing-summary.json",summary)
    print(json.dumps(summary,indent=2))
    return bool(failed)

def selftest():
    g=LineString([(0,0),(100,0),(100,100)])
    assert check(g,g)["accepted"]
    assert not check(g,LineString([(0,0),(100,100)]))["accepted"]
    assert slice_line(g,50,150).length==100
    print("Synthetic geometry checks passed")

if __name__=="__main__":
    import sys
    if "--self-test" in sys.argv: selftest()
    else: sys.exit(run())
