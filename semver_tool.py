#!/usr/bin/env python3
"""Semantic versioning — parse, compare, bump, range checking."""
import sys, re

class SemVer:
    PAT = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+(.+))?$")
    def __init__(self, major, minor, patch, pre=None, build=None):
        self.major, self.minor, self.patch = major, minor, patch
        self.pre, self.build = pre, build
    @classmethod
    def parse(cls, s):
        m = cls.PAT.match(s)
        if not m: raise ValueError(f"Invalid semver: {s}")
        return cls(int(m[1]), int(m[2]), int(m[3]), m[4], m[5])
    def __str__(self):
        s = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre: s += f"-{self.pre}"
        if self.build: s += f"+{self.build}"
        return s
    def _tuple(self): return (self.major, self.minor, self.patch, 0 if not self.pre else -1, self.pre or "")
    def __lt__(s, o): return s._tuple() < o._tuple()
    def __eq__(s, o): return s._tuple() == o._tuple()
    def __le__(s, o): return s < o or s == o
    def bump(self, part):
        if part == "major": return SemVer(self.major+1, 0, 0)
        if part == "minor": return SemVer(self.major, self.minor+1, 0)
        return SemVer(self.major, self.minor, self.patch+1)

def cli():
    if len(sys.argv) < 3:
        print("Usage: semver_tool <cmd> <version> [arg]"); print("  parse|bump|compare|sort"); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "parse":
        v = SemVer.parse(sys.argv[2]); print(f"Major: {v.major}, Minor: {v.minor}, Patch: {v.patch}, Pre: {v.pre}, Build: {v.build}")
    elif cmd == "bump":
        v = SemVer.parse(sys.argv[2]); part = sys.argv[3] if len(sys.argv)>3 else "patch"
        print(f"{v} → {v.bump(part)}")
    elif cmd == "compare":
        a, b = SemVer.parse(sys.argv[2]), SemVer.parse(sys.argv[3])
        r = "<" if a < b else ">" if b < a else "=="
        print(f"{a} {r} {b}")
    elif cmd == "sort":
        vs = sorted(SemVer.parse(v) for v in sys.argv[2:])
        for v in vs: print(f"  {v}")

if __name__ == "__main__": cli()
