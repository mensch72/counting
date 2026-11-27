/-
Band posets (Proposition 11 of notes/poset_complexity/proof.tex, in the generalised form of
notes/poset_complexity/narrow_bounds): a family of posets that are unions of `w` chains,
showing that there are many narrow posets.
-/
import Mathlib

namespace PosetCount

variable {ι : Type*} [DecidableEq ι]

/-- Band data over a height bound `g`.  Heights start at `0`.  `g t ≤ t` is the largest number of
elements of another chain that may lie below an element of height `t`.  For chains `i ≠ j`,
`e i j t` is the number of elements of chain `j` below the element of chain `i` at height `t`;
it is monotone in `t`, at most `g t`, and at least `g s` for every `s < g t`
(two steps down are always covered). -/
structure BandData (ι : Type*) (g : ℕ → ℕ) where
  e : ι → ι → ℕ → ℕ
  mono : ∀ i j, Monotone (e i j)
  upper : ∀ i j t, e i j t ≤ g t
  lower : ∀ i j t s, s < g t → g s ≤ e i j t

namespace BandData

variable {g : ℕ → ℕ} (b : BandData ι g)

/-- The relation: inside a chain by height; `(j,s) < (i,t)` for `i ≠ j` iff `s < e i j t`. -/
def lt (p q : ι × ℕ) : Prop :=
  if p.1 = q.1 then p.2 < q.2 else p.2 < b.e q.1 p.1 q.2

theorem lt_of_ne {p q : ι × ℕ} (h : b.lt p q) (hne : p.1 ≠ q.1) : p.2 < b.e q.1 p.1 q.2 := by
  unfold lt at h
  rwa [if_neg hne] at h

theorem lt_of_eq {p q : ι × ℕ} (h : b.lt p q) (he : p.1 = q.1) : p.2 < q.2 := by
  unfold lt at h
  rwa [if_pos he] at h

/-- A relation `p < q` raises the height. -/
theorem height_lt (hg : ∀ t, g t ≤ t) {p q : ι × ℕ} (h : b.lt p q) : p.2 < q.2 := by
  by_cases h1 : p.1 = q.1
  · exact b.lt_of_eq h h1
  · have h2 := b.lt_of_ne h h1
    have h3 := b.upper q.1 p.1 q.2
    have h4 := hg q.2
    omega

/-- **Band posets are posets.** If `g t ≤ t` for all `t`, the relation is a strict partial
order. -/
theorem isStrictOrder (hg : ∀ t, g t ≤ t) : IsStrictOrder (ι × ℕ) b.lt where
  irrefl := fun p h => lt_irrefl _ (b.height_lt hg h)
  trans := by
    intro p q r hpq hqr
    by_cases h13 : p.1 = r.1
    · -- same chain at both ends: heights decide
      have h1 := b.height_lt hg hpq
      have h2 := b.height_lt hg hqr
      unfold lt
      rw [if_pos h13]
      omega
    · unfold lt
      rw [if_neg h13]
      by_cases h12 : p.1 = q.1
      · -- p, q in the same chain, r in another
        have hqr' : q.1 ≠ r.1 := fun h => h13 (h12.trans h)
        have h1 := b.lt_of_eq hpq h12
        have h2 := b.lt_of_ne hqr hqr'
        rw [h12]
        omega
      · by_cases h23 : q.1 = r.1
        · -- q, r in the same chain, p in another
          have h1 := b.lt_of_ne hpq h12
          have h2 := b.lt_of_eq hqr h23
          have hm := b.mono q.1 p.1 (le_of_lt h2)
          rw [← h23]
          omega
        · -- three different chains: two steps down are covered
          have h1 := b.lt_of_ne hpq h12
          have h2 := b.lt_of_ne hqr h23
          have h3 := b.upper q.1 p.1 q.2
          have h4 := b.upper r.1 q.1 r.2
          have h5 := b.lower r.1 p.1 r.2 q.2 (by omega)
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

/-- The bands of the note: offsets between `a` and `2a`, i.e.
`t + 1 - 2a ≤ e i j t ≤ t + 1 - a`. -/
def BandData.ofOffset {a : ℕ} (e : ι → ι → ℕ → ℕ) (mono : ∀ i j, Monotone (e i j))
    (upper : ∀ i j t, e i j t ≤ t + 1 - a) (lower : ∀ i j t, t + 1 - 2 * a ≤ e i j t) :
    BandData ι (fun t => t + 1 - a) where
  e := e
  mono := mono
  upper := upper
  lower := by
    intro i j t s hs
    have := lower i j t
    omega

end PosetCount
