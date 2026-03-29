import sys, argparse, re

def parse_semver(s):
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)(?:-(\S+))?(?:\+(\S+))?", s)
    if not m:
        return None
    return (int(m[1]), int(m[2]), int(m[3]), m[4] or "", m[5] or "")

def cmp_semver(a, b):
    for i in range(3):
        if a[i] != b[i]:
            return -1 if a[i] < b[i] else 1
    if a[3] and not b[3]: return -1
    if not a[3] and b[3]: return 1
    if a[3] < b[3]: return -1
    if a[3] > b[3]: return 1
    return 0

def main():
    p = argparse.ArgumentParser(description="Semantic version tool")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("parse").add_argument("version")
    c = sub.add_parser("compare")
    c.add_argument("a"); c.add_argument("b")
    b = sub.add_parser("bump")
    b.add_argument("version"); b.add_argument("part", choices=["major","minor","patch"])
    s = sub.add_parser("sort")
    s.add_argument("versions", nargs="+")
    args = p.parse_args()
    if args.cmd == "parse":
        v = parse_semver(args.version)
        if v: print(f"major={v[0]} minor={v[1]} patch={v[2]} pre={v[3]} build={v[4]}")
        else: print("Invalid semver")
    elif args.cmd == "compare":
        a, b = parse_semver(args.a), parse_semver(args.b)
        r = cmp_semver(a, b)
        print("equal" if r == 0 else ("less" if r < 0 else "greater"))
    elif args.cmd == "bump":
        v = list(parse_semver(args.version))
        i = {"major":0,"minor":1,"patch":2}[args.part]
        v[i] += 1
        for j in range(i+1, 3): v[j] = 0
        v[3] = v[4] = ""
        print(f"{v[0]}.{v[1]}.{v[2]}")
    elif args.cmd == "sort":
        vers = [(parse_semver(v), v) for v in args.versions if parse_semver(v)]
        from functools import cmp_to_key
        vers.sort(key=cmp_to_key(lambda a,b: cmp_semver(a[0],b[0])))
        for _, v in vers: print(v)

if __name__ == "__main__":
    main()
