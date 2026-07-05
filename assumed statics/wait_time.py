#!/usr/bin/env python3
"""
wait_time.py -- Checks-in, and Balances: a Matter of Time.
FIFO wait engine and counter-allocation rule (Equations (7) to (16)).

This is the reference implementation of the wait-time logic documented in
Methodology_Counter_Allocation.md and wait_time_model.Rmd:

  Equation (7)  clock entry            a = dep - e
  Equation (8)  service start          s_i = max(a_i, d_{i-1})
  Equation (9)  processed time         d_i = s_i + t
  Equation (10) wait                   w_i = s_i - a_i
  Equation (11) increment (Lindley)    w_i = max(0, w_{i-1} + t - (a_i - a_{i-1}))
  Equation (12) closed form            w_i = max_j ( j*t - (a_i - a_{i-j}) )
  Equation (14) c-counter recursion    d_i = max(a_i, d_{i-c}) + t
  Equation (15) counter capacity       N = target / t
  Equation (16) counters at a minute   D(m) = ceil( A_W(m) / N )

Restored to the folder on July 05, 2026 (the original engine referenced in
Methodology_Counter_Allocation.md Section XII was not present in the handoff
copy); validated against worked_example.csv and the equivalence checks of
Equations (10) to (12).

Author: Yash Moitra, Delhi International Airport Limited.
"""
import math
from bisect import bisect_left


def fifo_wait(arrivals, t):
    """Single-counter FIFO waits, Equations (8) to (10).

    arrivals : iterable of clock times (minutes), any order
    t        : service time, minutes per passenger
    Returns (arrivals_sorted, waits, processed).
    """
    a = sorted(arrivals)
    waits, processed = [], []
    prev_done = -math.inf
    for ai in a:
        s = max(ai, prev_done)
        d = s + t
        waits.append(s - ai)
        processed.append(d)
        prev_done = d
    return a, waits, processed


def fifo_wait_lindley(arrivals, t):
    """Equation (11): increment form. Equivalent to fifo_wait."""
    a = sorted(arrivals)
    waits = []
    w = 0.0
    for i, ai in enumerate(a):
        w = 0.0 if i == 0 else max(0.0, w + t - (ai - a[i - 1]))
        waits.append(w)
    return a, waits


def multi_counter_wait(arrivals, t, c):
    """Equation (14): c identical counters, one pooled FIFO queue.

    Passenger i reuses the counter that served passenger i-c, so the system
    decomposes into c interleaved single-counter queues.
    """
    a = sorted(arrivals)
    waits, processed = [], []
    done = [-math.inf] * c
    for i, ai in enumerate(a):
        s = max(ai, done[i % c])
        d = s + t
        waits.append(s - ai)
        processed.append(d)
        done[i % c] = d
    return a, waits, processed


def desks_required(arrivals, t, target):
    """Equations (15) and (16): time-varying counters per minute.

    Returns (minutes, D) where D[j] = ceil(A_W(m)/N) for minute m = minutes[j],
    A_W(m) = arrivals in (m - target, m], N = target / t.
    """
    a = sorted(arrivals)
    if not a:
        return [], []
    n_cap = target / t
    m0, m1 = int(math.floor(a[0])), int(math.ceil(a[-1]))
    minutes, D = [], []
    for m in range(m0, m1 + 1):
        lo = bisect_left(a, m - target + 1e-9)
        hi = bisect_left(a, m + 1e-9)
        aw = hi - lo
        minutes.append(m)
        D.append(math.ceil(aw / n_cap) if aw else 0)
    return minutes, D


def _selftest():
    # Worksheet correction (Methodology_Counter_Allocation.md, Section IV):
    # arrivals 0,1,2 at t = 1.5 give waits 0.0, 0.5, 1.0 (2t-2 = 1.0, not 2t-3).
    _, w, _ = fifo_wait([0, 1, 2], 1.5)
    assert w == [0.0, 0.5, 1.0], w

    # Equations (10) vs (11) agree on random sequences.
    import random
    random.seed(0)
    for _ in range(200):
        arr = [random.uniform(0, 300) for _ in range(60)]
        t = random.choice([3.0, 10 / 3])
        _, w1, _ = fifo_wait(arr, t)
        _, w2 = fifo_wait_lindley(arr, t)
        assert all(abs(x - y) < 1e-9 for x, y in zip(w1, w2))

    # c-counter recursion vs direct c-server simulation.
    import heapq
    for _ in range(50):
        arr = sorted(random.uniform(0, 200) for _ in range(80))
        t, c = 3.0, random.randint(1, 6)
        _, w1, _ = multi_counter_wait(arr, t, c)
        free = [0.0] * c  # heap of counter-free times
        heapq.heapify(free)
        w2 = []
        for ai in arr:
            f = heapq.heappop(free)
            s = max(ai, f)
            w2.append(s - ai)
            heapq.heappush(free, s + t)
        assert all(abs(x - y) < 1e-9 for x, y in zip(w1, w2))
    print("wait_time.py selftest: all checks pass")


if __name__ == "__main__":
    _selftest()
