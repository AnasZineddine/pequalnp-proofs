# L-meta-24384: the posted bar of 7 gates is unreachable (least is 8)

Posted statement (exactly as the desk wrote it, upstream `c8054cf44`):

```
∃ C : Circuit, FanInTwo C ∧ C.size ≤ 7 ∧
  ∀ i j : Fin 6, C.eval (List.ofFn fun k : Fin 6 => decide (k = i ∨ k = j))
    = (34630324157 : ℕ).testBit (6 * min i.val j.val + max i.val j.val)
```

The desk's own sketch holds an 8-gate circuit and says *"No complete search of ours has run at
six points."* One has now run. The result is a refutation, not a timeout.

## Result

| k | verdict | wall |
|---|---|---|
| 8 | SAT (also reproduces the desk's own 8-gate circuit, 0/36 mismatches) | 0.6 s |
| 7 | **INFEASIBLE** — seeds 0, 5, 9 | 2.9 s / 3.8 s / 3.9 s |

So the least circuit size is 8 and the posted bar of 7 is false. The row was released to the desk
with `reason=statement_seems_false`.

## Model, and why it is trusted

Six inputs (`Fin 6`), 36 evaluation points `(i, j) ∈ Fin 6 × Fin 6`, the point `(i, j)` turning on
input `i` and input `j` (`i = j` gives the one-hot vector), target the mask bit at
`6 * min i j + max i j`. Each gate reads two earlier wires (`a ≤ b < i`) and is `and`, `or` or
`not`; the output is the last gate. This is exactly `FanInTwo` with `C.size` counted per gate.

The model is validated two independent ways before its UNSAT is trusted:

1. the desk's own held construction
   `OR(2,3), OR(5,6), AND(4,7), AND(5,6), AND(0,1), OR(8,9), OR(10,11), NOT(12)`
   replays with **0 mismatches on all 36 points**;
2. CP-SAT returns a 0.6 s solution at k = 8, so the encoding is not trivially unsatisfiable.

`INFEASIBLE` from CP-SAT is a proof of unsatisfiability, not a timeout; `UNKNOWN` would have been
reported as such.

## Reproduce

```
pip install ortools
python3 evidence/L_meta_24384/synth_24384.py
```

prints the truthy-point count, the k = 8 witness, the desk-circuit replay check, and the k = 7
status on three seeds.
