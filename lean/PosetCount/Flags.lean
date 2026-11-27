/-
Structure of a flag of antichains (Lemma 5 (b), (d) of notes/poset_complexity/proof.tex).
-/
import Mathlib

namespace PosetCount

variable {P : Type*} [PartialOrder P]

/-- `N ≼ N'`: every element of `N` is below or equal to some element of `N'`
(for antichains: `↓N ⊆ ↓N'`). -/
def Dominated (N N' : Set P) : Prop := ∀ a ∈ N, ∃ b ∈ N', a ≤ b

theorem Dominated.refl (N : Set P) : Dominated N N := fun a ha => ⟨a, ha, le_rfl⟩

theorem Dominated.trans {N N' N'' : Set P} (h : Dominated N N') (h' : Dominated N' N'') :
    Dominated N N'' := by
  intro a ha
  obtain ⟨b, hb, hab⟩ := h a ha
  obtain ⟨c, hc, hbc⟩ := h' b hb
  exact ⟨c, hc, hab.trans hbc⟩

/-- For antichains, `≼` is antisymmetric. -/
theorem Dominated.antisymm {N N' : Set P} (hN : IsAntichain (· ≤ ·) N)
    (hN' : IsAntichain (· ≤ ·) N') (h : Dominated N N') (h' : Dominated N' N) : N = N' := by
  have key : ∀ {X Y : Set P}, IsAntichain (· ≤ ·) X → Dominated X Y → Dominated Y X → X ⊆ Y := by
    intro X Y hX hXY hYX a ha
    obtain ⟨b, hb, hab⟩ := hXY a ha
    obtain ⟨c, hc, hbc⟩ := hYX b hb
    have hac : a = c := hX.eq ha hc (hab.trans hbc)
    subst hac
    exact (le_antisymm hab hbc) ▸ hb
  exact Set.Subset.antisymm (key hN h h') (key hN' h' h)

/-- **Lemma 5 (b).** In a chain `N ≼ N' ≼ M` with `M` an antichain, an element of `N ∩ M`
lies in `N'`. Hence the parts `N_i ∩ M` of a flag with top `M` increase with `i`. -/
theorem mem_of_dominated {N N' M : Set P} (hM : IsAntichain (· ≤ ·) M)
    (h : Dominated N N') (h' : Dominated N' M) {x : P} (hxN : x ∈ N) (hxM : x ∈ M) : x ∈ N' := by
  obtain ⟨z, hz, hxz⟩ := h x hxN
  obtain ⟨y, hy, hzy⟩ := h' z hz
  have hxy : x = y := hM.eq hxM hy (hxz.trans hzy)
  subst hxy
  exact (le_antisymm hxz hzy) ▸ hz

/-- **Lemma 5 (d).** In a chain `N ≼ N' ≼ N''` with `N''` an antichain, an element of `N` that
is not in `N'` is not in `N''`. Hence every element lies in the antichains of a flag for an
interval of indices. -/
theorem notMem_of_dominated {N N' N'' : Set P} (hN'' : IsAntichain (· ≤ ·) N'')
    (h : Dominated N N') (h' : Dominated N' N'') {e : P} (heN : e ∈ N) (heN' : e ∉ N') :
    e ∉ N'' := by
  intro he
  exact heN' (mem_of_dominated hN'' h h' heN he)

end PosetCount
