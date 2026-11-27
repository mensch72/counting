# PosetCount — Lean 4 formalisation

Machine-checked parts of `notes/poset_complexity/proof.tex`
("Counting labelled posets in time 2^(c n²) with c < 1/4").

Lean `v4.37.0-rc1`, Mathlib `v4.37.0-rc1`. No `sorry`, no `admit`, no added axiom;
`#print axioms` on the main theorems shows only `propext`, `Classical.choice`, `Quot.sound`.

## Building

    export PATH=$HOME/.elan/bin:$PATH
    lake exe cache get      # Mathlib build cache
    lake build

## Files

| File | Content |
|---|---|
| `PosetCount/Submodular.lean` | maximal elements of a finite set; submodularity lemma |
| `PosetCount/EulerChar.lean` | reduced Euler characteristic of a finite subposet; cones; removing a point whose upper link is a cone; closure operators |
| `PosetCount/WideDownsets.lean` | the poset `J_k(P)`; Euler characteristic; flag identity |

## Coverage

| Note | Status | Lean |
|---|---|---|
| Lemma 2 (submodularity of the number of maximal elements) | ✓ | `card_maxs_add_le` |
| Theorem 3, Euler-characteristic form (`J_k(P)` non-empty ⇒ reduced Euler characteristic 0) | ✓ | `redEuler_Jk_eq_zero` |
| Theorem 3, flag identity (signed number of `k`-flags is 1 or 0) | ✓ | `flag_identity` |
| `J_k(P)` non-empty ⇔ an antichain of size ≥ k exists | ✓ | `Jk_nonempty_iff` |
| Theorem 3, contractibility of the order complex | — | not formalised; only the Euler characteristic is used in the note |
| Lemma 4 (insertion) | — | |
| Lemma 5, Proposition 7 (structure of a flag, bijection) | — | |
| Lemma 8, Theorem 9 (counting formula) | — | |
| Complexity statements (Theorem 1, Propositions 10, 11) | — | not planned: running-time claims are outside the formalisation |

## Design

- A finite poset is a type `P` with `PartialOrder`, `Fintype`, `DecidableEq`.
  Down-sets are `Finset P` with `IsLowerSet`.
- `maxs I` is the finset of maximal elements of `I`.
- For a finite subset `s` of any partial order, `redEuler s` is the sum of `(-1)^|c|` over all
  chains `c ⊆ s`, the empty chain included. The Euler characteristic of the order complex is
  `1 - redEuler s`.
- `J_k(P)` is a `Finset (Finset P)`, a finite subset of the poset `Finset P` under inclusion.

## Differences from the note

1. The note proves Theorem 3 by citing Quillen's homotopy property. The Lean proof is
   self-contained and purely combinatorial: a sign-reversing involution for cones
   (`redEuler_eq_zero_of_least`), the same involution for a point whose upper link is a cone
   (`redEuler_erase`), and induction on the number of non-closed elements
   (`redEuler_image_closure`). It establishes the Euler characteristic only, which is all the
   counting formula needs.
2. The Lean proof does not use a maximum antichain. It takes a down-set in `J_k(P)` with the
   largest number of maximal elements, which is all that the argument needs.
