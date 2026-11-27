/-
Inserting an antichain into a poset along a cut (Lemma 4 of notes/poset_complexity/proof.tex).
-/
import Mathlib

namespace PosetCount

variable {α ι : Type*} [PartialOrder α]

/-- Insertion data: a cut `A` of the core poset `α` and, for every new element `i : ι`, a *type*
`(D i, U i)`: a down-set inside `A`, an up-set outside `A`, with `D i` entirely below `U i`. -/
structure InsData (α ι : Type*) [PartialOrder α] where
  /-- the cut -/
  A : Set α
  /-- the elements below the new element `i` -/
  D : ι → Set α
  /-- the elements above the new element `i` -/
  U : ι → Set α
  hD : ∀ i, IsLowerSet (D i)
  hU : ∀ i, IsUpperSet (U i)
  hDA : ∀ i, D i ⊆ A
  hUA : ∀ i, U i ⊆ Aᶜ
  hDU : ∀ i, ∀ d ∈ D i, ∀ u ∈ U i, d < u

namespace InsData

variable (d : InsData α ι)

/-- The strict order on `α ⊕ ι` obtained by inserting the new elements as an antichain. -/
def lt : α ⊕ ι → α ⊕ ι → Prop
  | .inl q, .inl q' => q < q'
  | .inl q, .inr x => q ∈ d.D x
  | .inr x, .inl q => q ∈ d.U x
  | .inr _, .inr _ => False

theorem lt_irrefl' (a : α ⊕ ι) : ¬ d.lt a a := by
  cases a with
  | inl q => exact lt_irrefl q
  | inr x => exact id

theorem lt_trans' {a b c : α ⊕ ι} (hab : d.lt a b) (hbc : d.lt b c) : d.lt a c := by
  rcases a with a | x <;> rcases b with b | y <;> rcases c with c | z
  · exact lt_trans hab hbc
  · exact d.hD z (le_of_lt hab) hbc
  · exact d.hDU y a hab c hbc
  · exact hbc.elim
  · exact d.hU x (le_of_lt hbc) hab
  · exact (d.hUA x hab (d.hDA z hbc)).elim
  · exact hab.elim
  · exact hab.elim

/-- **Insertion lemma.** The relation is a strict partial order. -/
instance : IsStrictOrder (α ⊕ ι) d.lt where
  irrefl := d.lt_irrefl'
  trans := fun _ _ _ => d.lt_trans'

/-- It restricts to the given order on the core. -/
theorem lt_inl_inl (q q' : α) : d.lt (.inl q) (.inl q') ↔ q < q' := Iff.rfl

/-- The new elements form an antichain. -/
theorem not_lt_inr_inr (x y : ι) : ¬ d.lt (.inr x) (.inr y) := id

/-- The core elements below the new element `x` are exactly `D x`. -/
theorem lt_inl_inr (q : α) (x : ι) : d.lt (.inl q) (.inr x) ↔ q ∈ d.D x := Iff.rfl

/-- The core elements above the new element `x` are exactly `U x`. -/
theorem lt_inr_inl (x : ι) (q : α) : d.lt (.inr x) (.inl q) ↔ q ∈ d.U x := Iff.rfl

/-- The core elements below some new element are the union of the `D x`, a subset of the cut. -/
theorem below_new_subset_cut (q : α) (h : ∃ x, d.lt (.inl q) (.inr x)) : q ∈ d.A := by
  obtain ⟨x, hx⟩ := h
  exact d.hDA x hx

/-- No element of the cut lies above a new element. -/
theorem cut_not_above_new (q : α) (hq : q ∈ d.A) (x : ι) : ¬ d.lt (.inr x) (.inl q) :=
  fun h => d.hUA x h hq

end InsData

/-- **Converse.** Every strict order on `α ⊕ ι` that extends the order of `α` and in which the new
elements form an antichain arises from insertion data, with the cut "below some new element". -/
def InsData.ofOrder (r : α ⊕ ι → α ⊕ ι → Prop) [IsStrictOrder (α ⊕ ι) r]
    (hcore : ∀ q q' : α, r (.inl q) (.inl q') ↔ q < q')
    (hanti : ∀ x y : ι, ¬ r (.inr x) (.inr y)) : InsData α ι where
  A := {q | ∃ x, r (.inl q) (.inr x)}
  D := fun x => {q | r (.inl q) (.inr x)}
  U := fun x => {q | r (.inr x) (.inl q)}
  hD := by
    intro x a b hba ha
    rcases eq_or_lt_of_le hba with h | h
    · exact h ▸ ha
    · exact _root_.trans ((hcore b a).2 h) ha
  hU := by
    intro x a b hab ha
    rcases eq_or_lt_of_le hab with h | h
    · exact h ▸ ha
    · exact _root_.trans (show r (.inr x) (.inl a) from ha) ((hcore a b).2 h)
  hDA := fun x q hq => ⟨x, hq⟩
  hUA := by
    rintro x q hq ⟨y, hy⟩
    exact hanti x y (_root_.trans (show r (.inr x) (.inl q) from hq) hy)
  hDU := by
    intro x a ha u hu
    exact (hcore a u).1 (_root_.trans (show r (.inl a) (.inr x) from ha) hu)

/-- The insertion data of an order reproduce that order. -/
theorem InsData.ofOrder_lt (r : α ⊕ ι → α ⊕ ι → Prop) [IsStrictOrder (α ⊕ ι) r]
    (hcore : ∀ q q' : α, r (.inl q) (.inl q') ↔ q < q')
    (hanti : ∀ x y : ι, ¬ r (.inr x) (.inr y)) (a b : α ⊕ ι) :
    (InsData.ofOrder r hcore hanti).lt a b ↔ r a b := by
  rcases a with a | x <;> rcases b with b | y
  · exact (hcore a b).symm
  · exact Iff.rfl
  · exact Iff.rfl
  · exact ⟨False.elim, hanti x y⟩

end PosetCount
