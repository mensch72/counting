/-
A general threshold theorem: in a finite family closed under joins and meets, the members on
which a supermodular function is at least `k` form a poset of Euler characteristic 1.
Instance: pairs of down-sets whose difference avoids a prescribed set of comparable pairs.
-/
import PosetCount.EulerChar

open Finset

namespace PosetCount

section General

variable {α : Type*} [Lattice α] [DecidableEq α]

/-- **Threshold theorem.** Let `L` be a finite set closed under `⊔` and `⊓` and let `s` be
supermodular on `L`.  If some member of `L` has `s ≥ k`, then the members with `s ≥ k` have
reduced Euler characteristic `0`. -/
theorem redEuler_threshold_eq_zero (L : Finset α) (s : α → ℤ) (k : ℤ)
    (hsup : ∀ p ∈ L, ∀ q ∈ L, p ⊔ q ∈ L) (hinf : ∀ p ∈ L, ∀ q ∈ L, p ⊓ q ∈ L)
    (hs : ∀ p ∈ L, ∀ q ∈ L, s p + s q ≤ s (p ⊔ q) + s (p ⊓ q))
    (hne : (L.filter (fun p => k ≤ s p)).Nonempty) :
    redEuler (L.filter (fun p => k ≤ s p)) = 0 := by
  obtain ⟨p₀, hp₀⟩ := hne
  obtain ⟨hp₀L, hp₀k⟩ := mem_filter.1 hp₀
  obtain ⟨m, hmL, hmax⟩ := exists_max_image L s ⟨p₀, hp₀L⟩
  have hmk : k ≤ s m := hp₀k.trans (hmax p₀ hp₀L)
  have hmap : ∀ p ∈ L.filter (fun p => k ≤ s p), p ⊔ m ∈ L.filter (fun p => k ≤ s p) := by
    intro p hp
    obtain ⟨hpL, hpk⟩ := mem_filter.1 hp
    refine mem_filter.2 ⟨hsup p hpL m hmL, ?_⟩
    have h1 := hs p hpL m hmL
    have h2 := hmax _ (hinf p hpL m hmL)
    linarith
  refine redEuler_eq_zero_of_closure_cone (fun p => p ⊔ m) _ m hmap ?_ ?_ ?_
    (mem_filter.2 ⟨hmL, hmk⟩) ?_ ?_
  · intro p _ q _ hpq
    exact sup_le_sup_right hpq m
  · intro p _
    exact le_sup_left
  · intro p _
    simp
  · simp
  · intro p _
    exact le_sup_right

end General

section Pairs

variable {P : Type*} [PartialOrder P] [Fintype P] [DecidableEq P]

open Classical in
/-- Pairs of down-sets `I' ⊆ I` such that no pair `(x, y) ∈ R` has both `x` and `y` in
`I \ I'`; that is, `y ∈ I` implies `x ∈ I'`. -/
noncomputable def pairsAvoiding (R : Set (P × P)) : Finset (Finset P × Finset P) :=
  univ.filter (fun p => IsLowerSet (p.1 : Set P) ∧ IsLowerSet (p.2 : Set P) ∧ p.1 ⊆ p.2 ∧
    ∀ x y, (x, y) ∈ R → y ∈ p.2 → x ∈ p.1)

theorem mem_pairsAvoiding {R : Set (P × P)} {p : Finset P × Finset P} :
    p ∈ pairsAvoiding R ↔ IsLowerSet (p.1 : Set P) ∧ IsLowerSet (p.2 : Set P) ∧ p.1 ⊆ p.2 ∧
      ∀ x y, (x, y) ∈ R → y ∈ p.2 → x ∈ p.1 := by
  classical
  simp [pairsAvoiding]

/-- **Pairs of down-sets with a large difference.** For every set `R` of pairs, the pairs of
down-sets `I' ⊆ I` avoiding `R` with `|I \ I'| ≥ k`, ordered componentwise, have reduced Euler
characteristic `0` as soon as there is one. -/
theorem redEuler_pairsAvoiding_eq_zero (R : Set (P × P)) (k : ℤ)
    (hne : ((pairsAvoiding R).filter
      (fun p => k ≤ (p.2.card : ℤ) - p.1.card)).Nonempty) :
    redEuler ((pairsAvoiding R).filter (fun p => k ≤ (p.2.card : ℤ) - p.1.card)) = 0 := by
  refine redEuler_threshold_eq_zero (pairsAvoiding R) (fun p => (p.2.card : ℤ) - p.1.card) k
    ?_ ?_ ?_ hne
  · intro p hp q hq
    obtain ⟨hp1, hp2, hp3, hp4⟩ := mem_pairsAvoiding.1 hp
    obtain ⟨hq1, hq2, hq3, hq4⟩ := mem_pairsAvoiding.1 hq
    refine mem_pairsAvoiding.2 ⟨?_, ?_, ?_, ?_⟩
    · simpa using hp1.union hq1
    · simpa using hp2.union hq2
    · exact union_subset_union hp3 hq3
    · intro x y hxy hy
      rcases mem_union.1 hy with h | h
      · exact mem_union_left _ (hp4 x y hxy h)
      · exact mem_union_right _ (hq4 x y hxy h)
  · intro p hp q hq
    obtain ⟨hp1, hp2, hp3, hp4⟩ := mem_pairsAvoiding.1 hp
    obtain ⟨hq1, hq2, hq3, hq4⟩ := mem_pairsAvoiding.1 hq
    refine mem_pairsAvoiding.2 ⟨?_, ?_, ?_, ?_⟩
    · simpa using hp1.inter hq1
    · simpa using hp2.inter hq2
    · exact inter_subset_inter hp3 hq3
    · intro x y hxy hy
      obtain ⟨h1, h2⟩ := mem_inter.1 hy
      exact mem_inter.2 ⟨hp4 x y hxy h1, hq4 x y hxy h2⟩
  · intro p _ q _
    have h1 := card_union_add_card_inter p.1 q.1
    have h2 := card_union_add_card_inter p.2 q.2
    show ((p.2.card : ℤ) - p.1.card) + ((q.2.card : ℤ) - q.1.card)
      ≤ (((p.2 ∪ q.2).card : ℤ) - (p.1 ∪ q.1).card) + (((p.2 ∩ q.2).card : ℤ) - (p.1 ∩ q.1).card)
    have h1' : (((p.1 ∪ q.1).card : ℤ)) + (p.1 ∩ q.1).card = p.1.card + q.1.card := by
      exact_mod_cast h1
    have h2' : (((p.2 ∪ q.2).card : ℤ)) + (p.2 ∩ q.2).card = p.2.card + q.2.card := by
      exact_mod_cast h2
    linarith

end Pairs

end PosetCount
