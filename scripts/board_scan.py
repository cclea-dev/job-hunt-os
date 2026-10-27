#!/usr/bin/env python3
"""Scan public job-board APIs and print a short list of matching postings.

Used by the weekly-job-recos skill so the model reads a shortlist instead of
whole job boards. Standard library only.

Usage:
  python3 scripts/board_scan.py --config scan.json [--seen seen.txt]

scan.json:
{
  "boards": [
    {"company": "Acme", "system": "greenhouse", "board": "acme"},
    {"company": "Beta", "system": "lever", "board": "beta", "region": "eu"},
    {"company": "Gamma", "system": "ashby", "board": "gamma"},
    {"company": "Delta", "system": "smartrecruiters", "board": "Delta"}
  ],
  "include": ["operations manager", "bizops", "program manager"],   # title must contain one
  "exclude": ["intern", "junior", "director", "engineer"],          # title must contain none
  "locations": ["lisbon", "porto", "remote"],         # location must contain one ([] = any)
  "max_age_days": 7                                                 # by published date when known
}

seen.txt: one posting URL per line (postings already checked in earlier runs); they're skipped.

Output: JSON with "candidates" (company, title, location, url, published, system) and
"errors" (boards that couldn't be read).
"""
import argparse
import datetime as dt
import json
import sys
import urllib.request

UA = {"User-Agent": "job-hunt-os board_scan"}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def parse_date(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):  # Lever: milliseconds since epoch
        return dt.datetime.fromtimestamp(value / 1000, dt.timezone.utc)
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def greenhouse(board):
    data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs")
    for j in data.get("jobs", []):
        yield j.get("title", ""), (j.get("location") or {}).get("name", ""), j.get("absolute_url", ""), j.get("updated_at")


def lever(board, region=None):
    host = "api.eu.lever.co" if region == "eu" else "api.lever.co"
    for j in get_json(f"https://{host}/v0/postings/{board}?mode=json"):
        cats = j.get("categories") or {}
        loc = ", ".join(filter(None, [cats.get("location")] + (cats.get("allLocations") or [])))
        yield j.get("text", ""), loc, j.get("hostedUrl", ""), j.get("createdAt")


def ashby(board):
    data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{board}")
    for j in data.get("jobs", []):
        locs = [j.get("location") or ""] + [s.get("location", "") for s in j.get("secondaryLocations") or []]
        if j.get("isRemote"):
            locs.append("Remote")
        yield j.get("title", ""), ", ".join(filter(None, locs)), j.get("jobUrl", ""), j.get("publishedAt")


def smartrecruiters(board):
    data = get_json(f"https://api.smartrecruiters.com/v1/companies/{board}/postings?limit=100")
    for j in data.get("content", []):
        loc = j.get("location") or {}
        where = ", ".join(filter(None, [loc.get("city"), loc.get("country"), "Remote" if loc.get("remote") else ""]))
        url = f"https://jobs.smartrecruiters.com/{board}/{j.get('id')}"
        yield j.get("name", ""), where, url, j.get("releasedDate")


SYSTEMS = {"greenhouse": greenhouse, "lever": lever, "ashby": ashby, "smartrecruiters": smartrecruiters}


def bare(url):
    return url.split("?")[0].rstrip("/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--seen")
    args = ap.parse_args()
    cfg = json.load(open(args.config))
    seen = set()
    if args.seen:
        seen = {bare(line.strip()) for line in open(args.seen) if line.strip()}
    include = [s.lower() for s in cfg.get("include", [])]
    exclude = [s.lower() for s in cfg.get("exclude", [])]
    locations = [s.lower() for s in cfg.get("locations", [])]
    max_age = cfg.get("max_age_days")
    now = dt.datetime.now(dt.timezone.utc)

    out, errors, scanned = [], [], 0
    for b in cfg.get("boards", []):
        fn = SYSTEMS.get(b.get("system", "").lower())
        if not fn:
            errors.append({"company": b.get("company"), "error": f"unsupported system {b.get('system')}"})
            continue
        try:
            rows = list(fn(b["board"], b.get("region")) if fn is lever else fn(b["board"]))
        except Exception as e:  # board moved, renamed, or blocked
            errors.append({"company": b.get("company"), "error": str(e)[:120]})
            continue
        for title, loc, url, published in rows:
            scanned += 1
            t, l = title.lower(), loc.lower()
            if include and not any(k in t for k in include):
                continue
            if any(k in t for k in exclude):
                continue
            if locations and not any(k in l for k in locations):
                continue
            url = bare(url)
            if url in seen:
                continue
            when = parse_date(published)
            if max_age and when and (now - when).days > max_age:
                continue
            out.append({"company": b.get("company"), "title": title, "location": loc, "url": url,
                        "published": when.date().isoformat() if when else None, "system": b.get("system")})
    json.dump({"scanned": scanned, "candidates": out, "errors": errors}, sys.stdout, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
