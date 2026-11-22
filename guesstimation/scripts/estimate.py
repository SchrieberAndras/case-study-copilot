#!/usr/bin/env python3
"""Combine estimation factors and give a realistic range.

Usage:
  python estimate.py "name=low,base,high" "name=value" ...
  python estimate.py "a=..." "b=..." + "c=..." "d=..."      sum of segments (a*b + c*d)
  python estimate.py "total=..." "/per_unit=..."             divide by a factor (prefix "/")

Each factor is one value or low,base,high (any order; sorted automatically).
Values accept scientific notation (1.4e6) and k / M / bn suffixes (1.4M, 250k, 2bn).
Factors in a segment are multiplied; a leading "/" divides instead. A lone "+"
starts a new segment, and segments are added.

Output: every factor with the running result (so each step can be shown), the
base case, and a P10-P90 range from a Monte Carlo simulation (each factor drawn
triangular in log space between low and high, peaking at base). Multiplying all
lows and all highs overstates the spread; the simulation does not. Factor ranges
you enter set the output range, so do not enter tight ranges for judgement calls.
"""
import math
import random
import sys

SUFFIX = {"k": 1e3, "m": 1e6, "bn": 1e9, "b": 1e9, "tn": 1e12, "t": 1e12}


def num(s):
    s = s.strip().replace("_", "").lower()
    for suf in ("bn", "tn", "k", "m", "b", "t"):
        if s.endswith(suf) and not s.endswith("e" + suf):
            return float(s[: -len(suf)]) * SUFFIX[suf]
    return float(s)


def parse(arg):
    div = arg.startswith("/")
    name, _, vals = arg.lstrip("/").partition("=")
    if not vals:
        sys.exit(f"Bad factor '{arg}': use name=value or name=low,base,high")
    parts = [num(v) for v in vals.split(",")]
    if len(parts) == 1:
        parts = parts * 3
    if len(parts) != 3:
        sys.exit(f"Bad factor '{arg}': give one value or low,base,high")
    low, base, high = sorted(parts)
    if low <= 0:
        sys.exit(f"Factor '{name}' must be positive")
    return name.strip(), low, base, high, div


def fmt(x):
    mag = abs(x)
    if mag >= 1e12:
        return f"{x/1e12:,.3g} tn"
    if mag >= 1e9:
        return f"{x/1e9:,.3g} bn"
    if mag >= 1e6:
        return f"{x/1e6:,.3g} M"
    if mag >= 1e3:
        return f"{float(f'{x:.3g}'):,.0f}"
    return f"{x:.3g}"


def draw(low, base, high):
    if low == high:
        return base
    return math.exp(random.triangular(math.log(low), math.log(high), math.log(base)))


def main(argv):
    if not argv:
        sys.exit(__doc__)
    segments, cur = [], []
    for a in argv:
        if a.strip() == "+":
            segments.append(cur)
            cur = []
        else:
            cur.append(parse(a))
    segments.append(cur)
    if any(not s for s in segments):
        sys.exit("Empty segment: check the '+' separators")

    total = 0.0
    for i, seg in enumerate(segments, 1):
        if len(segments) > 1:
            print(f"-- Segment {i}")
        print("Factor                     low        base        high   running result")
        r = 1.0
        for name, low, base, high, div in seg:
            r = r / base if div else r * base
            label = ("/ " if div else "") + name
            print(f"{label:<22} {fmt(low):>10} {fmt(base):>11} {fmt(high):>11}   {fmt(r)}")
        total += r
        if len(segments) > 1:
            print(f"Segment {i} base: {fmt(r)}\n")

    random.seed(42)
    sims = []
    for _ in range(20000):
        t = 0.0
        for seg in segments:
            p = 1.0
            for _, low, base, high, div in seg:
                v = draw(low, base, high)
                p = p / v if div else p * v
            t += p
        sims.append(t)
    sims.sort()
    p10, p50, p90 = (sims[int(len(sims) * q)] for q in (0.10, 0.50, 0.90))

    print()
    print(f"Base case:        {fmt(total)}")
    print(f"Realistic range:  {fmt(p10)} - {fmt(p90)}  (P10-P90, median {fmt(p50)})")
    if p90 / p10 < 1.35:
        print("NOTE: P10-P90 is narrower than +/-15%. Fine for a precisely known fact; otherwise present"
              " a final range at least as wide as the SKILL.md step 8 minimum for this kind of answer.")


if __name__ == "__main__":
    main(sys.argv[1:])
