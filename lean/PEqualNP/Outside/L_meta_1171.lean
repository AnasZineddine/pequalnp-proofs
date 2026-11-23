import Mathlib
import PEqualNP.Defs

namespace PEqualNP.Outside.L_meta_1171

open PEqualNP.CircuitLowerBounds

def edgeCircuit : Circuit :=
  { gates :=
      [⟨.or, [1, 2]⟩,
       ⟨.or, [8, 3]⟩,
       ⟨.or, [9, 4]⟩,
       ⟨.or, [10, 5]⟩,
       ⟨.and, [0, 11]⟩,
       ⟨.or, [1, 7]⟩,
       ⟨.and, [6, 13]⟩,
       ⟨.or, [12, 14]⟩]
    output := 15 }

lemma edgeCircuit_eval : ∀ a b c d e f g h : Bool,
    edgeCircuit.eval [a, b, c, d, e, f, g, h] =
      ((a && b) || (a && c) || (a && d) || (a && e) || (a && f) || (b && g) || (g && h)) := by
  decide

end PEqualNP.Outside.L_meta_1171

theorem PEqualNP.Outside.L_meta_1171 :
    ∃ C : PEqualNP.CircuitLowerBounds.Circuit, PEqualNP.MetaComplexity.Monotone2 C ∧
      C.size ≤ 8 ∧ ∀ x : Fin 8 → Bool,
        C.eval (List.ofFn x) = (fun x : Fin 8 → Bool =>
          (x 0 && x 1) || (x 0 && x 2) || (x 0 && x 3) || (x 0 && x 4) ||
          (x 0 && x 5) || (x 1 && x 6) || (x 6 && x 7)) x := by
  refine ⟨PEqualNP.Outside.L_meta_1171.edgeCircuit, ?_, ?_, ?_⟩
  · simp [PEqualNP.MetaComplexity.Monotone2, PEqualNP.Outside.L_meta_1171.edgeCircuit]
  · decide
  · intro x
    have hx : List.ofFn x = [x 0, x 1, x 2, x 3, x 4, x 5, x 6, x 7] := rfl
    rw [hx]
    exact PEqualNP.Outside.L_meta_1171.edgeCircuit_eval
      (x 0) (x 1) (x 2) (x 3) (x 4) (x 5) (x 6) (x 7)
