"""Exact search for L-meta-24384: least AND/OR/NOT fan-in-two circuit, 6 inputs, mask 34630324157."""
import time
from ortools.sat.python import cp_model

MASK, N = 34630324157, 6
pairs = [(i, j) for i in range(N) for j in range(N)]
pins = [set([i]) if i == j else set([i, j]) for (i, j) in pairs]
tgt = [(MASK >> (N * min(i, j) + max(i, j))) & 1 for (i, j) in pairs]

# the desk's own held 8-gate construction, replayed
desk = [(2, 3, 'or'), (5, 6, 'or'), (4, 7, 'and'), (5, 6, 'and'),
        (0, 1, 'and'), (8, 9, 'or'), (10, 11, 'or'), (12, 12, 'not')]

def ev(gates, p):
    w = [1 if q in p else 0 for q in range(N)]
    for a, b, op in gates:
        w.append((w[a] & w[b]) if op == 'and' else (w[a] | w[b]) if op == 'or' else (1 - w[a]))
    return w[-1]

def solve(k, tlim=300, seed=0):
    T, NN = len(pairs), N + k
    m = cp_model.CpModel()
    tab = [[None] * T for _ in range(NN)]
    for w in range(N):
        for t in range(T):
            tab[w][t] = m.NewConstant(1 if w in pins[t] else 0)
    for w in range(N, NN):
        for t in range(T):
            tab[w][t] = m.NewBoolVar(f"w{w}_{t}")
    A, B, OP = [], [], []
    for i in range(k):
        a = m.NewIntVar(0, N + i - 1, f"a{i}"); b = m.NewIntVar(0, N + i - 1, f"b{i}")
        op = m.NewIntVar(0, 2, f"op{i}")
        m.Add(a <= b); A.append(a); B.append(b); OP.append(op)
        for t in range(T):
            av = m.NewBoolVar(""); bv = m.NewBoolVar("")
            m.AddElement(a, [tab[w][t] for w in range(N + i)], av)
            m.AddElement(b, [tab[w][t] for w in range(N + i)], bv)
            c0 = m.NewBoolVar(""); c1 = m.NewBoolVar("")
            m.AddBoolAnd([av, bv]).OnlyEnforceIf(c0)
            m.AddBoolOr([av.Not(), bv.Not()]).OnlyEnforceIf(c0.Not())
            m.AddBoolOr([av, bv]).OnlyEnforceIf(c1)
            m.AddBoolAnd([av.Not(), bv.Not()]).OnlyEnforceIf(c1.Not())
            c2 = m.NewBoolVar(""); m.AddBoolXOr([c2, av])
            m.AddElement(op, [c0, c1, c2], tab[N + i][t])
    for t in range(T):
        m.Add(tab[NN - 1][t] == tgt[t])
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_search_workers = 8
    s.parameters.random_seed = seed
    st = s.Solve(m)
    gates = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        names = ['and', 'or', 'not']
        gates = [(s.Value(A[i]), s.Value(B[i]), names[s.Value(OP[i])]) for i in range(k)]
    return s.StatusName(st), gates, s.WallTime()

if __name__ == "__main__":
    print("truthy points:", sum(tgt), "/", len(tgt))
    bad = [p for p in pins if ev(desk, p) != tgt[pins.index(p)]]
    print("desk 8-gate construction mismatches:", len(bad))
    st, g, w = solve(8, tlim=120, seed=0)
    print(f"k=8: {st} {w:.1f}s gates={g}")
    if g:
        print("  witness mismatches:", sum(1 for p, q in zip(pins, tgt) if ev(g, p) != q))
    for seed in (0, 5, 9):
        st, _, w = solve(7, tlim=300, seed=seed)
        print(f"k=7 seed={seed}: {st} {w:.1f}s")
