# L-meta-23652 (cut unit): the posted bar of 8 gates is unreachable (least is 9)

Posted statement: two-lit function, six shared wires, mask 35889, `FanInTwo C ∧ C.size ≤ 8`,
judged on the 36 pairs `(i, j) ∈ Fin 6 × Fin 6`.

Desk sketch: it holds a 9-gate circuit and says "A met unit may be a better order of the points and
not a saving from a NOT gate. A proof exhibits 8 gates and evaluates the 21 inputs."

Exact search over all 36 points, same encoding as L-meta-24384 (gates read two earlier wires, and/or/not,
output last; validated there against the desk's own held circuit with 0 mismatches):

    k = 8: INFEASIBLE in 27.6 s (CP-SAT proof of unsatisfiability, not a timeout)

So the least size is 9, matching the desk's own hold, and the posted bar of 8 is false. Released to
the desk with `reason=statement_seems_false` and `program=<sha256 of synth_23652.py>`, i.e. the
evidence channel the join text documents for a disproved row (`POST /desk/release?lease=..&reason=..&program=..`).

## Reproduce

    pip install ortools
    python3 evidence/L_meta_23652/synth_23652.py 8
