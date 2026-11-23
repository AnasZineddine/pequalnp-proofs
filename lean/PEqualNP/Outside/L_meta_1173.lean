import Mathlib
import PEqualNP.Defs

namespace PEqualNP.Outside.L_meta_1173

open PEqualNP.CircuitLowerBounds

def edgeCircuit : Circuit :=
  { gates :=
      [⟨.or, [1, 2]⟩,
       ⟨.or, [8, 3]⟩,
       ⟨.or, [9, 4]⟩,
       ⟨.and, [0, 10]⟩,
       ⟨.and, [1, 2]⟩,
       ⟨.and, [3, 5]⟩,
       ⟨.and, [6, 7]⟩,
       ⟨.or, [11, 12]⟩,
       ⟨.or, [15, 13]⟩,
       ⟨.or, [16, 14]⟩]
    output := 17 }

lemma edgeCircuit_eval : ∀ a b c d e f g h : Bool,
    edgeCircuit.eval [a, b, c, d, e, f, g, h] =
      ((a && b) || (a && c) || (a && d) || (a && e) || (b && c) || (d && f) || (g && h)) := by
  decide

end PEqualNP.Outside.L_meta_1173

theorem PEqualNP.Outside.L_meta_1173 :
    ∃ C : PEqualNP.CircuitLowerBounds.Circuit, PEqualNP.MetaComplexity.Monotone2 C ∧
      C.size ≤ 10 ∧ ∀ x : Fin 8 → Bool,
        C.eval (List.ofFn x) = (fun x : Fin 8 → Bool =>
          (x 0 && x 1) || (x 0 && x 2) || (x 0 && x 3) || (x 0 && x 4) ||
          (x 1 && x 2) || (x 3 && x 5) || (x 6 && x 7)) x := by
  refine ⟨PEqualNP.Outside.L_meta_1173.edgeCircuit, ?_, ?_, ?_⟩
  · simp [PEqualNP.MetaComplexity.Monotone2, PEqualNP.Outside.L_meta_1173.edgeCircuit]
  · decide
  · intro x
    have hx : List.ofFn x = [x 0, x 1, x 2, x 3, x 4, x 5, x 6, x 7] := rfl
    rw [hx]
    exact PEqualNP.Outside.L_meta_1173.edgeCircuit_eval
      (x 0) (x 1) (x 2) (x 3) (x 4) (x 5) (x 6) (x 7)
