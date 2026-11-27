/-
Band posets (Proposition 11 of notes/poset_complexity/proof.tex): a family of posets of
width at most `w` showing that there are many narrow posets.
-/
import Mathlib

namespace PosetCount

variable {ι : Type*} [DecidableEq ι]

/-- Band data: for chains `i ≠ j` and height `t` (heights start at `0`), `e i j t` is the number
of elements of chain `j` below the element of chain `i` at height `t`.  It is monotone in `t`
and confined to a band: `t + 1 - 2a ≤ e i j t ≤ t + 1 - a`. -/
structure BandData (ι : Type*) (a : ℕ) where
  e : ι → ι → ℕ → ℕ
  mono : ∀ i j, Monotone (e i j)
  upper : ∀ i j t, e i j t ≤ t + 1 - a
  lower : ∀ i j t, t + 1 - 2 * a ≤ e i j t

namespace BandData

variable {a : ℕ} (b : BandData ι a)

/-- The relation: inside a chain by height; `(j,s) < (i,t)` for `i ≠ j` iff `s < e i j t`. -/
def lt (p q : ι × ℕ) : Prop :=
  if p.1 = q.1 then p.2 < q.2 else p.2 < b.e q.1 p.1 q.2

/-- A relation `p < q` raises the height, by at least `a` between different chains. -/
theorem height_lt (ha : 1 ≤ a) {p q : ι × ℕ} (h : b.lt p q) : p.2 < q.2 := by
  unfold lt at h
  split_ifs at h with h1
  · exact h
  · have := b.upper q.1 p.1 q.2
    omega

theorem height_add_le {p q : ι × ℕ} (h : b.lt p q) (hne : p.1 ≠ q.1) : p.2 + a ≤ q.2 := by
  unfold lt at h
  rw [if_neg hne] at h
  have := b.upper q.1 p.1 q.2
  omega

/-- **Band posets are posets.** For `a ≥ 1` the relation is a strict partial order. -/
theorem isStrictOrder (ha : 1 ≤ a) : IsStrictOrder (ι × ℕ) b.lt where
  irrefl := fun p h => lt_irrefl _ (b.height_lt ha h)
  trans := by
    intro p q r hpq hqr
    by_cases h13 : p.1 = r.1
    · -- same chain at both ends: heights decide
      have h1 := b.height_lt ha hpq
      have h2 := b.height_lt ha hqr
      unfold lt
      rw [if_pos h13]
      omega
    · unfold lt
      rw [if_neg h13]
      by_cases h12 : p.1 = q.1
      · -- p, q in the same chain, r in another
        have hqr' : q.1 ≠ r.1 := fun h => h13 (h12.trans h)
        have h1 : p.2 < q.2 := by
          have := hpq; unfold lt at this; rwa [if_pos h12] at this
        have h2 : q.2 < b.e r.1 q.1 r.2 := by
          have := hqr; unfold lt at this; rwa [if_neg hqr'] at this
        rw [h12]
        omega
      · by_cases h23 : q.1 = r.1
        · -- q, r in the same chain, p in another
          have h1 : p.2 < b.e q.1 p.1 q.2 := by
            have := hpq; unfold lt at this; rwa [if_neg h12] at this
          have h2 : q.2 < r.2 := by
            have := hqr; unfold lt at this; rwa [if_pos h23] at this
          have hm := b.mono q.1 p.1 (le_of_lt h2)
          rw [← h23]
          omega
        · -- three different chains: two steps down cover at least `2a`
          have h1 := b.height_add_le hpq h12
          have h2 := b.height_add_le hqr h23
          have h3 := b.lower r.1 p.1 r.2
          omega

/-- Each chain `{i} × ℕ` is totally ordered. -/
theorem chain_total (i : ι) (s t : ℕ) (h : s ≠ t) : b.lt (i, s) (i, t) ∨ b.lt (i, t) (i, s) := by
  unfold lt
  simp only [if_true]
  omega

/-- The data are recovered from the order. -/
theorem lt_iff_of_ne {i j : ι} (hij : j ≠ i) (s t : ℕ) : b.lt (j, s) (i, t) ↔ s < b.e i j t := by
  unfold lt
  simp [hij]

end BandData

end PosetCount
