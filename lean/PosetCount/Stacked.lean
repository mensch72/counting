/-
Stacked antichains: several antichains `S_j = I_j \ I'_j` separated by gaps, with
`I_j` entirely below everything outside `I'_{j'}` for `j < j'`.  The family is closed under
componentwise union and intersection, so the threshold theorem applies.
-/
import PosetCount.Threshold

open Finset

namespace PosetCount

variable {P : Type*} [PartialOrder P] [Fintype P] [DecidableEq P]
variable {ι : Type*} [Fintype ι] [DecidableEq ι] [LinearOrder ι]

/-- The conditions defining a stack of antichains indexed by `ι`. -/
def IsStack (f : ι → Finset P × Finset P) : Prop :=
  (∀ j, IsLowerSet ((f j).1 : Set P) ∧ IsLowerSet ((f j).2 : Set P) ∧ (f j).1 ⊆ (f j).2 ∧
    ∀ x y, x < y → y ∈ (f j).2 → x ∈ (f j).1) ∧
  ∀ j j', j < j' → (f j).2 ⊆ (f j').1 ∧ ∀ x ∈ (f j).2, ∀ y, y ∉ (f j').1 → x < y

/-- In a stack, each layer `I_j \ I'_j` is an antichain. -/
theorem IsStack.layer_antichain {f : ι → Finset P × Finset P} (hf : IsStack f) (j : ι) :
    IsAntichain (· ≤ ·) (((f j).2 \ (f j).1 : Finset P) : Set P) := by
  intro x hx y hy hxy hle
  have hx' := mem_sdiff.1 (by exact_mod_cast hx)
  have hy' := mem_sdiff.1 (by exact_mod_cast hy)
  exact hx'.2 ((hf.1 j).2.2.2 x y (lt_of_le_of_ne hle hxy) hy'.1)

/-- In a stack, every element of a lower layer is below every element of a higher layer. -/
theorem IsStack.layer_lt {f : ι → Finset P × Finset P} (hf : IsStack f) {j j' : ι} (h : j < j')
    {x y : P} (hx : x ∈ (f j).2) (hy : y ∈ (f j').2 \ (f j').1) : x < y :=
  (hf.2 j j' h).2 x hx y (mem_sdiff.1 hy).2

open Classical in
/-- The finite set of all stacks. -/
noncomputable def stackSet (P : Type*) [PartialOrder P] [Fintype P] [DecidableEq P]
    (ι : Type*) [Fintype ι] [DecidableEq ι] [LinearOrder ι] :
    Finset (ι → Finset P × Finset P) :=
  univ.filter IsStack

theorem mem_stackSet {f : ι → Finset P × Finset P} : f ∈ stackSet P ι ↔ IsStack f := by
  classical
  simp [stackSet]

/-- The total number of points in the layers of a stack. -/
def stackSize (f : ι → Finset P × Finset P) : ℤ :=
  ∑ j, (((f j).2.card : ℤ) - (f j).1.card)

theorem isStack_sup {f g : ι → Finset P × Finset P} (hf : IsStack f) (hg : IsStack g) :
    IsStack (f ⊔ g) := by
  refine ⟨fun j => ?_, fun j j' h => ?_⟩
  · obtain ⟨a1, a2, a3, a4⟩ := hf.1 j
    obtain ⟨b1, b2, b3, b4⟩ := hg.1 j
    refine ⟨?_, ?_, ?_, ?_⟩
    · simpa using a1.union b1
    · simpa using a2.union b2
    · exact union_subset_union a3 b3
    · intro x y hxy hy
      rcases mem_union.1 hy with h | h
      · exact mem_union_left _ (a4 x y hxy h)
      · exact mem_union_right _ (b4 x y hxy h)
  · obtain ⟨a1, a2⟩ := hf.2 j j' h
    obtain ⟨b1, b2⟩ := hg.2 j j' h
    refine ⟨union_subset_union a1 b1, ?_⟩
    intro x hx y hy
    have hy' : y ∉ (f j').1 ∧ y ∉ (g j').1 := by
      constructor
      · exact fun h' => hy (mem_union_left _ h')
      · exact fun h' => hy (mem_union_right _ h')
    rcases mem_union.1 hx with h' | h'
    · exact a2 x h' y hy'.1
    · exact b2 x h' y hy'.2

theorem isStack_inf {f g : ι → Finset P × Finset P} (hf : IsStack f) (hg : IsStack g) :
    IsStack (f ⊓ g) := by
  refine ⟨fun j => ?_, fun j j' h => ?_⟩
  · obtain ⟨a1, a2, a3, a4⟩ := hf.1 j
    obtain ⟨b1, b2, b3, b4⟩ := hg.1 j
    refine ⟨?_, ?_, ?_, ?_⟩
    · simpa using a1.inter b1
    · simpa using a2.inter b2
    · exact inter_subset_inter a3 b3
    · intro x y hxy hy
      obtain ⟨h1, h2⟩ := mem_inter.1 hy
      exact mem_inter.2 ⟨a4 x y hxy h1, b4 x y hxy h2⟩
  · obtain ⟨a1, a2⟩ := hf.2 j j' h
    obtain ⟨b1, b2⟩ := hg.2 j j' h
    refine ⟨inter_subset_inter a1 b1, ?_⟩
    intro x hx y hy
    obtain ⟨h1, h2⟩ := mem_inter.1 hx
    by_cases hyf : y ∈ (f j').1
    · have hyg : y ∉ (g j').1 := fun h' => hy (mem_inter.2 ⟨hyf, h'⟩)
      exact b2 x h2 y hyg
    · exact a2 x h1 y hyf

/-- **Stacks with many points.** If some stack has at least `k` points in its layers, the stackSet
with at least `k` points, ordered componentwise, have reduced Euler characteristic `0`. -/
theorem redEuler_stackSet_eq_zero (k : ℤ)
    (hne : ((stackSet P ι).filter (fun f => k ≤ stackSize f)).Nonempty) :
    redEuler ((stackSet P ι).filter (fun f => k ≤ stackSize f)) = 0 := by
  refine redEuler_threshold_eq_zero (stackSet P ι) stackSize k ?_ ?_ ?_ hne
  · intro f hf g hg
    exact mem_stackSet.2 (isStack_sup (mem_stackSet.1 hf) (mem_stackSet.1 hg))
  · intro f hf g hg
    exact mem_stackSet.2 (isStack_inf (mem_stackSet.1 hf) (mem_stackSet.1 hg))
  · intro f _ g _
    unfold stackSize
    rw [← sum_add_distrib, ← sum_add_distrib]
    refine sum_le_sum (fun j _ => ?_)
    have h1 := card_union_add_card_inter (f j).1 (g j).1
    have h2 := card_union_add_card_inter (f j).2 (g j).2
    show (((f j).2.card : ℤ) - (f j).1.card) + (((g j).2.card : ℤ) - (g j).1.card)
      ≤ ((((f j).2 ∪ (g j).2).card : ℤ) - ((f j).1 ∪ (g j).1).card)
        + ((((f j).2 ∩ (g j).2).card : ℤ) - ((f j).1 ∩ (g j).1).card)
    have h1' : ((((f j).1 ∪ (g j).1).card : ℤ)) + ((f j).1 ∩ (g j).1).card
        = (f j).1.card + (g j).1.card := by exact_mod_cast h1
    have h2' : ((((f j).2 ∪ (g j).2).card : ℤ)) + ((f j).2 ∩ (g j).2).card
        = (f j).2.card + (g j).2.card := by exact_mod_cast h2
    linarith

end PosetCount
