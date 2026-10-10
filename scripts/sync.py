"""Snapshot the public columns of the Google Sheet into data/ as a fallback for the live fetch."""
import csv, io, urllib.request

BASE = "https://docs.google.com/spreadsheets/d/15tpVhsFph5AHnAuUsHFBY82zPciBDJzpfQzWKZ_cNP0/gviz/tq?tqx=out:csv&gid="
TABS = {
    "incidents": ("1500637786", ["Incident ID", "Event title", "Occurrence label", "Disclosed on", "Company",
                                  "Model", "Category", "Incident summary", "Outcome", "Evidence"]),
    "sources": ("1116836595", ["Incident ID", "Publisher", "Source title", "URL"]),
}

for name, (gid, keep) in TABS.items():
    raw = urllib.request.urlopen(BASE + gid, timeout=30).read().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows:
        raise SystemExit(f"{name}: sheet returned no rows, keeping previous snapshot")
    with open(f"data/{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keep, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(name, len(rows))
