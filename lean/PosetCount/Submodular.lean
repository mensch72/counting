/-
Maximal elements of down-sets: the submodularity lemma
(Lemma 2 of notes/poset_complexity/proof.tex).
-/
import Mathlib

open Finset

namespace PosetCount

variable {α : Type*} [PartialOrder α]

open Classical in
/-- The set of maximal elements of a finite set `I`. -/
noncomputable def maxs (I : Finset α) : Finset α :=
  I.filter (fun a => ∀ b ∈ I, a ≤ b → b = a)

theorem mem_maxs {I : Finset α} {a : α} :
    a ∈ maxs I ↔ a ∈ I ∧ ∀ b ∈ I, a ≤ b → b = a := by
  classical
  simp [maxs]

theorem maxs_subset (I : Finset α) : maxs I ⊆ I := by
  classical
  exact filter_subset _ _

/-- `maxs I` is an antichain. -/
theorem maxs_antichain (I : Finset α) : IsAntichain (· ≤ ·) (maxs I : Set α) := by
  intro a ha b hb hab hle
  have ha' := mem_maxs.1 (by simpa using ha)
  have hb' := mem_maxs.1 (by simpa using hb)
  exact hab (ha'.2 b hb'.1 hle).symm

variable [DecidableEq α]

/-- An element that is maximal in a down-set `I₁` is maximal in `I₁ ∪ I₂` or in `I₁ ∩ I₂`. -/
theorem maxs_left_subset {I₁ I₂ : Finset α} (h₂ : IsLowerSet (I₂ : Set α)) :
    maxs I₁ ⊆ maxs (I₁ ∪ I₂) ∪ maxs (I₁ ∩ I₂) := by
  intro a ha
  obtain ⟨ha1, hmax⟩ := mem_maxs.1 ha
  by_cases h : ∀ b ∈ I₁ ∪ I₂, a ≤ b → b = a
  · exact mem_union_left _ (mem_maxs.2 ⟨mem_union_left _ ha1, h⟩)
  · push Not at h
    obtain ⟨c, hc, hac, hne⟩ := h
    have hc2 : c ∈ I₂ := by
      rcases mem_union.1 hc with h1 | h2
      · exact absurd (hmax c h1 hac) hne
      · exact h2
    have ha2 : a ∈ I₂ := h₂ hac hc2
    refine mem_union_right _ (mem_maxs.2 ⟨mem_inter.2 ⟨ha1, ha2⟩, ?_⟩)
    intro b hb hab
    exact hmax b (mem_inter.1 hb).1 hab

/-- **Submodularity of the number of maximal elements.** -/
theorem card_maxs_add_le {I₁ I₂ : Finset α}
    (h₁ : IsLowerSet (I₁ : Set α)) (h₂ : IsLowerSet (I₂ : Set α)) :
    (maxs I₁).card + (maxs I₂).card ≤ (maxs (I₁ ∪ I₂)).card + (maxs (I₁ ∩ I₂)).card := by
  have hU : maxs I₁ ∪ maxs I₂ ⊆ maxs (I₁ ∪ I₂) ∪ maxs (I₁ ∩ I₂) := by
    apply union_subset (maxs_left_subset h₂)
    have := maxs_left_subset (I₁ := I₂) (I₂ := I₁) h₁
    rwa [union_comm I₂ I₁, inter_comm I₂ I₁] at this
  have hI : maxs I₁ ∩ maxs I₂ ⊆ maxs (I₁ ∪ I₂) ∩ maxs (I₁ ∩ I₂) := by
    intro a ha
    obtain ⟨ha1, ha2⟩ := mem_inter.1 ha
    obtain ⟨h1, m1⟩ := mem_maxs.1 ha1
    obtain ⟨h2, m2⟩ := mem_maxs.1 ha2
    refine mem_inter.2 ⟨mem_maxs.2 ⟨mem_union_left _ h1, ?_⟩,
      mem_maxs.2 ⟨mem_inter.2 ⟨h1, h2⟩, ?_⟩⟩
    · intro b hb hab
      rcases mem_union.1 hb with h | h
      · exact m1 b h hab
      · exact m2 b h hab
    · intro b hb hab
      exact m1 b (mem_inter.1 hb).1 hab
  calc (maxs I₁).card + (maxs I₂).card
      = (maxs I₁ ∪ maxs I₂).card + (maxs I₁ ∩ maxs I₂).card := (card_union_add_card_inter _ _).symm
    _ ≤ (maxs (I₁ ∪ I₂) ∪ maxs (I₁ ∩ I₂)).card + (maxs (I₁ ∪ I₂) ∩ maxs (I₁ ∩ I₂)).card :=
        Nat.add_le_add (card_le_card hU) (card_le_card hI)
    _ = (maxs (I₁ ∪ I₂)).card + (maxs (I₁ ∩ I₂)).card := card_union_add_card_inter _ _

end PosetCount
