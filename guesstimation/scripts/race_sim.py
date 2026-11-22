#!/usr/bin/env python3
"""Template: simulate a race between accumulation and clearance, find the break point.

Use for dynamic guesstimates where a static multiplication misses the tipping point
(swarm vs. one fighter, queue vs. server, stock vs. restocking).

How to use:
  1. Edit PARAMS with your assumptions (each one is a row in the assumptions table).
  2. Edit step() so it advances the state by one second and returns
     "win", "lose" or None (still running).
  3. Run: python race_sim.py            -> win chance per N and the break point
          python race_sim.py sweep       -> break point with each param moved low/high
  Edit LOW_HIGH to set the sensitivity ranges.

The example below is a crowd of N opponents vs. one person who removes them
two at a time; he loses if pinned (>= pin_at clinging) for 10 straight seconds.
"""
import random
import sys

PARAMS = dict(
    engage=0.3,    # share of opponents actively trying
    arrive=0.08,   # chance per second an engaged free opponent reaches him
    fall=0.04,     # chance per second each clinger lets go
    pin_at=8,      # clingers that knock him down
    up_at=5,       # he can stand again below this many
    carry=2,       # removed per trip
    trip=8,        # seconds per removal trip
    shed=1.0,      # clingers shaken off per second while standing
    tmax=1800,     # seconds before he is exhausted (counts as a loss)
)
LOW_HIGH = dict(engage=(0.2, 0.5), pin_at=(6, 12), carry=(1, 3))
N_VALUES = range(10, 201, 5)
RUNS = 300


def new_state(N, p):
    return dict(N=N, free=N, cling=0, out=0, down=0, t=0)


def step(s, p):
    s["t"] += 1
    fat = max(0.4, 1 - s["t"] / 1500)  # fatigue: pace falls to 40%
    new = sum(random.random() < p["engage"] * p["arrive"] for _ in range(s["free"]))
    s["free"] -= new
    s["cling"] += new
    let_go = sum(random.random() < p["fall"] for _ in range(s["cling"]))
    s["cling"] -= let_go
    s["free"] += let_go
    if s["cling"] >= p["pin_at"] or (s["down"] and s["cling"] >= p["up_at"]):
        s["down"] += 1
        if s["down"] >= 10:
            return "lose"
        if random.random() < p["shed"] * fat * 0.5:
            s["cling"] -= 1
            s["free"] += 1
        return None
    s["down"] = 0
    if s["cling"] > 2 and random.random() < p["shed"] * fat:
        s["cling"] -= 1
        s["free"] += 1
    elif random.random() < fat * p["carry"] / p["trip"]:
        if s["cling"]:
            s["cling"] -= 1
        else:
            s["free"] -= 1
        s["out"] += 1
    if s["out"] >= s["N"]:
        return "win"
    if s["t"] >= p["tmax"]:
        return "lose"
    return None


def win_rate(N, p):
    wins = 0
    for _ in range(RUNS):
        s = new_state(N, p)
        while (r := step(s, p)) is None:
            pass
        wins += r == "win"
    return wins / RUNS


def break_point(p, verbose=False):
    best = None
    for N in N_VALUES:
        w = win_rate(N, p)
        if verbose:
            print(f"N={N:<5} win {w:4.0%}")
        if w >= 0.5:
            best = N
        elif best is not None and w < 0.05:
            break
    return best


if __name__ == "__main__":
    random.seed(1)
    if len(sys.argv) > 1 and sys.argv[1] == "sweep":
        print(f"base: break point {break_point(PARAMS)}")
        for k, (lo, hi) in LOW_HIGH.items():
            for v in (lo, hi):
                print(f"{k}={v}: break point {break_point({**PARAMS, k: v})}")
    else:
        print(f"Break point (largest N with >=50% win): {break_point(PARAMS, verbose=True)}")
