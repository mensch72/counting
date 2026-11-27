/-
Reduced Euler characteristic of a finite subposet, cones, and closure operators.
-/
import Mathlib

open Finset

namespace PosetCount

variable {α : Type*} [PartialOrder α] [DecidableEq α]

/-- Toggle membership of `m` in `c`. -/
def toggle (m : α) (c : Finset α) : Finset α :=
  if m ∈ c then c.erase m else insert m c

theorem toggle_toggle (m : α) (c : Finset α) : toggle m (toggle m c) = c := by
  unfold toggle
  by_cases h : m ∈ c
  · simp [h, insert_erase h]
  · simp [h, erase_insert h]

theorem toggle_ne (m : α) (c : Finset α) : toggle m c ≠ c := by
  unfold toggle
  by_cases h : m ∈ c
  · simp only [h, ite_true]
    intro he
    have : m ∈ c.erase m := by rw [he]; exact h
    simp at this
  · simp only [h, ite_false]
    intro he
    exact h (he ▸ mem_insert_self m c)

theorem neg_one_pow_card_toggle (m : α) (c : Finset α) :
    ((-1 : ℤ)) ^ c.card + (-1) ^ (toggle m c).card = 0 := by
  unfold toggle
  by_cases h : m ∈ c
  · have hc : c.card = (c.erase m).card + 1 := (card_erase_add_one h).symm
    simp only [h, ite_true]
    rw [hc, pow_succ]; ring
  · simp only [h, ite_false]
    rw [card_insert_of_notMem h, pow_succ]; ring

theorem mem_toggle {m a : α} {c : Finset α} (ha : a ≠ m) : a ∈ toggle m c ↔ a ∈ c := by
  unfold toggle
  by_cases h : m ∈ c <;> simp [h, ha]

/-- If a family of finite sets is closed under toggling `m`, its signed count vanishes. -/
theorem sum_neg_one_pow_card_eq_zero_of_toggle (T : Finset (Finset α)) (m : α)
    (hT : ∀ c ∈ T, toggle m c ∈ T) : ∑ c ∈ T, ((-1 : ℤ)) ^ c.card = 0 :=
  sum_involution (fun c _ => toggle m c) (fun c _ => neg_one_pow_card_toggle m c)
    (fun c _ _ => toggle_ne m c) hT (fun c _ => toggle_toggle m c)

open Classical in
/-- The chains contained in `s` (including the empty chain). -/
noncomputable def chainsOf (s : Finset α) : Finset (Finset α) :=
  s.powerset.filter (fun c => IsChain (· ≤ ·) (c : Set α))

theorem mem_chainsOf {s c : Finset α} :
    c ∈ chainsOf s ↔ c ⊆ s ∧ IsChain (· ≤ ·) (c : Set α) := by
  classical
  simp [chainsOf]

/-- The reduced Euler characteristic of the order complex of `s`, up to sign:
the sum of `(-1)^|c|` over all chains `c ⊆ s`, including the empty one.
The (unreduced) Euler characteristic is `1 - redEuler s`. -/
noncomputable def redEuler (s : Finset α) : ℤ := ∑ c ∈ chainsOf s, (-1) ^ c.card

/-- Toggling an element comparable to everything in `s` keeps chains of `s`. -/
theorem toggle_mem_chainsOf {s c : Finset α} {m : α} (hm : m ∈ s)
    (hc : c ∈ chainsOf s) (hcomp : ∀ b ∈ c, m ≤ b ∨ b ≤ m) : toggle m c ∈ chainsOf s := by
  obtain ⟨hcs, hch⟩ := mem_chainsOf.1 hc
  unfold toggle
  by_cases h : m ∈ c
  · simp only [h, ite_true]
    refine mem_chainsOf.2 ⟨(erase_subset _ _).trans hcs, hch.mono ?_⟩
    exact_mod_cast erase_subset m c
  · simp only [h, ite_false]
    refine mem_chainsOf.2 ⟨insert_subset hm hcs, ?_⟩
    rw [coe_insert]
    exact hch.insert (fun b hb _ => hcomp b (by exact_mod_cast hb))

/-- **Cone.** A finite poset with a least element has reduced Euler characteristic `0`. -/
theorem redEuler_eq_zero_of_least {s : Finset α} {m : α} (hm : m ∈ s)
    (hle : ∀ x ∈ s, m ≤ x) : redEuler s = 0 := by
  refine sum_neg_one_pow_card_eq_zero_of_toggle _ m (fun c hc => ?_)
  exact toggle_mem_chainsOf hm hc (fun b hb => Or.inl (hle b ((mem_chainsOf.1 hc).1 hb)))

/-- **Removing a point whose upper link is a cone.** If the elements of `s` strictly above `x`
have a least element `m`, then removing `x` does not change the reduced Euler characteristic. -/
theorem redEuler_erase {s : Finset α} {x m : α} (hm : m ∈ s) (hxm : x < m)
    (hmin : ∀ y ∈ s, x < y → m ≤ y) : redEuler (s.erase x) = redEuler s := by
  classical
  have hsplit : redEuler s = ∑ c ∈ (chainsOf s).filter (fun c => x ∈ c), ((-1 : ℤ)) ^ c.card
      + ∑ c ∈ (chainsOf s).filter (fun c => ¬ x ∈ c), ((-1 : ℤ)) ^ c.card := by
    unfold redEuler
    rw [sum_filter_add_sum_filter_not]
  have hzero : ∑ c ∈ (chainsOf s).filter (fun c => x ∈ c), ((-1 : ℤ)) ^ c.card = 0 := by
    refine sum_neg_one_pow_card_eq_zero_of_toggle _ m (fun c hc => ?_)
    obtain ⟨hc1, hxc⟩ := mem_filter.1 hc
    obtain ⟨hcs, hch⟩ := mem_chainsOf.1 hc1
    refine mem_filter.2 ⟨toggle_mem_chainsOf hm hc1 (fun b hb => ?_), (mem_toggle hxm.ne).2 hxc⟩
    by_cases hbx : b = x
    · exact Or.inr (hbx ▸ hxm.le)
    · rcases hch (by exact_mod_cast hb) (by exact_mod_cast hxc) hbx with h | h
      · exact Or.inr (h.trans hxm.le)
      · exact Or.inl (hmin b (hcs hb) (lt_of_le_of_ne h (Ne.symm hbx)))
  have hrest : (chainsOf s).filter (fun c => ¬ x ∈ c) = chainsOf (s.erase x) := by
    ext c
    simp only [mem_filter, mem_chainsOf, subset_erase]
    tauto
  rw [hsplit, hzero, zero_add, hrest, redEuler]

/-- **Closure operators preserve the Euler characteristic.**  Let `f` map `s` into `s`, be
monotone, extensive and idempotent on `s`.  Then `s` and its image have the same reduced Euler
characteristic. -/
theorem redEuler_image_closure (f : α → α) :
    ∀ (s : Finset α), (∀ x ∈ s, f x ∈ s) → (∀ x ∈ s, ∀ y ∈ s, x ≤ y → f x ≤ f y) →
      (∀ x ∈ s, x ≤ f x) → (∀ x ∈ s, f (f x) = f x) → redEuler (s.image f) = redEuler s := by
  intro s
  induction s using Finset.strongInduction with
  | H s ih =>
    intro hmap hmono hext hidem
    by_cases hall : ∀ x ∈ s, f x = x
    · have : s.image f = s := by
        ext y
        simp only [mem_image]
        constructor
        · rintro ⟨x, hx, rfl⟩; rw [hall x hx]; exact hx
        · intro hy; exact ⟨y, hy, hall y hy⟩
      rw [this]
    · push Not at hall
      -- choose a maximal non-fixed element
      have hne : (s.filter (fun x => f x ≠ x)).Nonempty := by
        obtain ⟨x, hx, hfx⟩ := hall
        exact ⟨x, mem_filter.2 ⟨hx, hfx⟩⟩
      obtain ⟨x, hxmem, hxmax⟩ := (s.filter (fun x => f x ≠ x)).exists_maximal hne
      obtain ⟨hxs, hfx⟩ := mem_filter.1 hxmem
      have hxlt : x < f x := lt_of_le_of_ne (hext x hxs) (Ne.symm hfx)
      have hmin : ∀ y ∈ s, x < y → f x ≤ y := by
        intro y hy hxy
        have hfy : f y = y := by
          by_contra hne'
          have hym : y ∈ s.filter (fun x => f x ≠ x) := mem_filter.2 ⟨hy, hne'⟩
          exact absurd (hxmax hym hxy.le) (not_le_of_gt hxy)
        calc f x ≤ f y := hmono x hxs y hy hxy.le
          _ = y := hfy
      have hfxne : ∀ z ∈ s, f z ≠ x := by
        intro z hz h
        have := hidem z hz
        rw [h] at this
        exact hfx this
      have h1 : redEuler (s.erase x) = redEuler s :=
        redEuler_erase (hmap x hxs) hxlt hmin
      have himg : (s.erase x).image f = s.image f := by
        ext y
        simp only [mem_image, mem_erase]
        constructor
        · rintro ⟨z, ⟨_, hz⟩, rfl⟩; exact ⟨z, hz, rfl⟩
        · rintro ⟨z, hz, rfl⟩
          by_cases hzx : z = x
          · subst hzx
            exact ⟨f z, ⟨hfxne z hz, hmap z hz⟩, hidem z hz⟩
          · exact ⟨z, ⟨hzx, hz⟩, rfl⟩
      have h2 := ih (s.erase x) (erase_ssubset hxs)
        (fun z hz => mem_erase.2 ⟨hfxne z (mem_of_mem_erase hz), hmap z (mem_of_mem_erase hz)⟩)
        (fun a ha b hb => hmono a (mem_of_mem_erase ha) b (mem_of_mem_erase hb))
        (fun z hz => hext z (mem_of_mem_erase hz))
        (fun z hz => hidem z (mem_of_mem_erase hz))
      rw [← himg, h2, h1]

/-- **Closure onto a cone.** If a closure operator on `s` has an image with a least element,
the reduced Euler characteristic of `s` is `0` (so the Euler characteristic is `1`). -/
theorem redEuler_eq_zero_of_closure_cone (f : α → α) (s : Finset α) (m : α)
    (hmap : ∀ x ∈ s, f x ∈ s) (hmono : ∀ x ∈ s, ∀ y ∈ s, x ≤ y → f x ≤ f y)
    (hext : ∀ x ∈ s, x ≤ f x) (hidem : ∀ x ∈ s, f (f x) = f x)
    (hm : m ∈ s) (hfm : f m = m) (hleast : ∀ x ∈ s, m ≤ f x) : redEuler s = 0 := by
  rw [← redEuler_image_closure f s hmap hmono hext hidem]
  refine redEuler_eq_zero_of_least (m := m) (mem_image.2 ⟨m, hm, hfm⟩) ?_
  intro y hy
  obtain ⟨x, hx, rfl⟩ := mem_image.1 hy
  exact hleast x hx

end PosetCount
