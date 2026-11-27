/-
The poset `J_k(P)` of down-sets with at least `k` maximal elements has Euler characteristic 1
whenever it is non-empty (Theorem 3 of notes/poset_complexity/proof.tex).
-/
import PosetCount.Submodular
import PosetCount.EulerChar

open Finset

namespace PosetCount

variable {P : Type*} [PartialOrder P] [Fintype P] [DecidableEq P]

open Classical in
/-- `J_k(P)`: the down-sets of `P` with at least `k` maximal elements, as a finite subset of the
poset `Finset P` (ordered by inclusion). -/
noncomputable def Jk (P : Type*) [PartialOrder P] [Fintype P] (k : ℕ) : Finset (Finset P) :=
  univ.filter (fun I => IsLowerSet (I : Set P) ∧ k ≤ (maxs I).card)

theorem mem_Jk {k : ℕ} {I : Finset P} :
    I ∈ Jk P k ↔ IsLowerSet (I : Set P) ∧ k ≤ (maxs I).card := by
  classical
  simp [Jk]

/-- **Contractibility, in Euler-characteristic form.** If `J_k(P)` is non-empty, its reduced
Euler characteristic vanishes. -/
theorem redEuler_Jk_eq_zero {k : ℕ} (hne : (Jk P k).Nonempty) : redEuler (Jk P k) = 0 := by
  obtain ⟨Is, hIs, hmax⟩ := exists_max_image (Jk P k) (fun I => (maxs I).card) hne
  obtain ⟨hIslow, hIsk⟩ := mem_Jk.1 hIs
  have hmap : ∀ I ∈ Jk P k, I ∪ Is ∈ Jk P k := by
    intro I hI
    obtain ⟨hlow, hk⟩ := mem_Jk.1 hI
    have hlowU : IsLowerSet ((I ∪ Is : Finset P) : Set P) := by
      rw [coe_union]; exact hlow.union hIslow
    have hlowI : IsLowerSet ((I ∩ Is : Finset P) : Set P) := by
      rw [coe_inter]; exact hlow.inter hIslow
    refine mem_Jk.2 ⟨hlowU, ?_⟩
    have hsub := card_maxs_add_le hlow hIslow
    have hcap : (maxs (I ∩ Is)).card ≤ (maxs Is).card := by
      by_cases h : k ≤ (maxs (I ∩ Is)).card
      · exact hmax _ (mem_Jk.2 ⟨hlowI, h⟩)
      · omega
    omega
  refine redEuler_eq_zero_of_closure_cone (fun I => I ∪ Is) (Jk P k) Is hmap ?_ ?_ ?_ hIs ?_ ?_
  · intro I _ J _ hIJ
    exact union_subset_union_left hIJ
  · intro I _
    exact subset_union_left
  · intro I _
    simp
  · simp
  · intro I _
    exact subset_union_right

/-- `J_k(P)` is non-empty iff `P` has an antichain with at least `k` elements. -/
theorem Jk_nonempty_iff {k : ℕ} :
    (Jk P k).Nonempty ↔ ∃ A : Finset P, IsAntichain (· ≤ ·) (A : Set P) ∧ k ≤ A.card := by
  classical
  constructor
  · rintro ⟨I, hI⟩
    exact ⟨maxs I, maxs_antichain I, (mem_Jk.1 hI).2⟩
  · rintro ⟨A, hA, hk⟩
    refine ⟨univ.filter (fun x => ∃ a ∈ A, x ≤ a), mem_Jk.2 ⟨?_, ?_⟩⟩
    · intro x y hyx hx
      simp only [coe_filter, mem_univ, true_and, Set.mem_ofPred_eq] at hx ⊢
      obtain ⟨a, ha, hxa⟩ := hx
      exact ⟨a, ha, hyx.trans hxa⟩
    · refine hk.trans (card_le_card ?_)
      intro a ha
      refine mem_maxs.2 ⟨by simp only [mem_filter, mem_univ, true_and]; exact ⟨a, ha, le_rfl⟩, ?_⟩
      intro b hb hab
      simp only [mem_filter, mem_univ, true_and] at hb
      obtain ⟨a', ha', hba'⟩ := hb
      have haa' : a = a' := by
        by_contra hne
        exact hA (by exact_mod_cast ha) (by exact_mod_cast ha') hne (hab.trans hba')
      subst haa'
      exact le_antisymm hba' hab

open Classical in
/-- **The flag identity.**  The signed number of non-empty chains `I₀ ⊂ ⋯ ⊂ I_r` in `J_k(P)`,
with sign `(-1)^r`, is `1` if `P` has an antichain of size at least `k`, and `0` otherwise. -/
theorem flag_identity (k : ℕ) :
    ∑ c ∈ (chainsOf (Jk P k)).filter (fun c => c.Nonempty), ((-1 : ℤ)) ^ (c.card + 1)
      = if ∃ A : Finset P, IsAntichain (· ≤ ·) (A : Set P) ∧ k ≤ A.card then 1 else 0 := by
  classical
  have hsplit : redEuler (Jk P k)
      = 1 - ∑ c ∈ (chainsOf (Jk P k)).filter (fun c => c.Nonempty), ((-1 : ℤ)) ^ (c.card + 1) := by
    have hempty : (∅ : Finset (Finset P)) ∈ chainsOf (Jk P k) :=
      mem_chainsOf.2 ⟨empty_subset _, by simp⟩
    have h1 : (chainsOf (Jk P k)).filter (fun c => ¬ c.Nonempty) = {∅} := by
      ext c
      simp only [mem_filter, mem_singleton, not_nonempty_iff_eq_empty]
      constructor
      · exact fun h => h.2
      · rintro rfl; exact ⟨hempty, rfl⟩
    unfold redEuler
    rw [← sum_filter_add_sum_filter_not (chainsOf (Jk P k)) (fun c => c.Nonempty), h1]
    simp only [sum_singleton, card_empty, pow_zero, pow_succ, mul_neg, mul_one, sum_neg_distrib]
    ring
  split_ifs with h
  · have := redEuler_Jk_eq_zero (Jk_nonempty_iff.2 h)
    rw [hsplit] at this
    linarith
  · have hJ : Jk P k = ∅ := by
      rw [← not_nonempty_iff_eq_empty, Jk_nonempty_iff]; exact h
    rw [hJ]
    refine sum_eq_zero (fun c hc => ?_)
    obtain ⟨hc1, hc2⟩ := mem_filter.1 hc
    have : c = ∅ := subset_empty.1 (mem_chainsOf.1 hc1).1
    exact absurd hc2 (by simp [this])

end PosetCount
