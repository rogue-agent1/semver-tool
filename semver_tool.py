#!/usr/bin/env python3
"""semver_tool - Semantic versioning utilities."""
import sys, argparse, json, re

def parse(v):
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+([a-zA-Z0-9.]+))?", v)
    if not m: return None
    return {"major": int(m.group(1)), "minor": int(m.group(2)), "patch": int(m.group(3)), "prerelease": m.group(4), "build": m.group(5)}

def compare(a, b):
    pa, pb = parse(a), parse(b)
    for k in ["major", "minor", "patch"]:
        if pa[k] != pb[k]: return 1 if pa[k] > pb[k] else -1
    if pa["prerelease"] and not pb["prerelease"]: return -1
    if not pa["prerelease"] and pb["prerelease"]: return 1
    if pa["prerelease"] and pb["prerelease"]:
        if pa["prerelease"] > pb["prerelease"]: return 1
        if pa["prerelease"] < pb["prerelease"]: return -1
    return 0

def bump(v, part):
    p = parse(v)
    if part == "major": p["major"] += 1; p["minor"] = p["patch"] = 0
    elif part == "minor": p["minor"] += 1; p["patch"] = 0
    elif part == "patch": p["patch"] += 1
    p["prerelease"] = p["build"] = None
    return f"{p['major']}.{p['minor']}.{p['patch']}"

def main():
    p = argparse.ArgumentParser(description="Semver tool")
    sub = p.add_subparsers(dest="cmd")
    pr = sub.add_parser("parse"); pr.add_argument("version")
    cmp = sub.add_parser("compare"); cmp.add_argument("a"); cmp.add_argument("b")
    bu = sub.add_parser("bump"); bu.add_argument("version"); bu.add_argument("part", choices=["major","minor","patch"])
    so = sub.add_parser("sort"); so.add_argument("versions", nargs="+")
    args = p.parse_args()
    if args.cmd == "parse": print(json.dumps(parse(args.version), indent=2))
    elif args.cmd == "compare":
        r = compare(args.a, args.b)
        print(json.dumps({"a": args.a, "b": args.b, "result": r, "description": f"{args.a} {'>' if r>0 else '<' if r<0 else '=='} {args.b}"}))
    elif args.cmd == "bump": print(json.dumps({"original": args.version, "bumped": bump(args.version, args.part), "part": args.part}))
    elif args.cmd == "sort":
        from functools import cmp_to_key
        sorted_v = sorted(args.versions, key=cmp_to_key(compare))
        print(json.dumps({"sorted": sorted_v}))
    else: p.print_help()

if __name__ == "__main__": main()
