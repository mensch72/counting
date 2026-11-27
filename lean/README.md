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
| `PosetCount/Insertion.lean` | inserting an antichain along a cut, and the converse |
| `PosetCount/Flags.lean` | the relation `≼` on antichains; structure of a flag |
| `PosetCount/Band.lean` | band posets: many posets of small width |
| `PosetCount/Threshold.lean` | general threshold theorem for supermodular functions on finite lattices of sets; pairs of down-sets avoiding a set of pairs |

## Coverage

| Note | Status | Lean |
|---|---|---|
| Lemma 2 (submodularity of the number of maximal elements) | ✓ | `card_maxs_add_le` |
| Theorem 3, Euler-characteristic form (`J_k(P)` non-empty ⇒ reduced Euler characteristic 0) | ✓ | `redEuler_Jk_eq_zero` |
| Theorem 3, flag identity (signed number of `k`-flags is 1 or 0) | ✓ | `flag_identity` |
| `J_k(P)` non-empty ⇔ an antichain of size ≥ k exists | ✓ | `Jk_nonempty_iff` |
| Theorem 3, contractibility of the order complex | — | not formalised; only the Euler characteristic is used in the note |
| Lemma 4 (insertion: the constructed relation is a strict partial order) | ✓ | `InsData.lt`, instance `IsStrictOrder` |
| Converse of Lemma 4 (every order with the new elements as an antichain arises this way) | ✓ | `InsData.ofOrder`, `InsData.ofOrder_lt` |
| Lemma 5 (b) (parts `N_i ∩ M` increase) | ✓ | `mem_of_dominated` |
| Lemma 5 (d) (interval property) | ✓ | `notMem_of_dominated` |
| Lemma 5 (a), (c); Proposition 7 (bijection with valid configurations) | — | |
| Lemma 8, Theorem 9 (counting formula) | — | |
| Proposition 11 (band posets are posets; chains are total; data recovered from the order) | ✓ | `BandData.isStrictOrder`, `BandData.chain_total`, `BandData.lt_iff_of_ne` |
| Proposition 11, the count `c(ℓ,a)^(w(w-1))` | — | |
| (new, not in the note) Threshold theorem: in a finite family closed under `⊔`, `⊓`, the members with a supermodular `s ≥ k` have Euler characteristic 1 | ✓ | `redEuler_threshold_eq_zero` |
| (new) Pairs of down-sets `I' ⊆ I` whose difference avoids a set `R` of pairs and has ≥ k points | ✓ | `redEuler_pairsAvoiding_eq_zero` |
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
3. Lemma 5 (d) follows directly from Lemma 5 (b) (`notMem_of_dominated`); the separate
   argument in the note is not needed.
4. In the insertion lemma the cut `A` need not be a down-set; only `D x ⊆ A` and
   `U x ⊆ Aᶜ` are used.
5. Band posets are formalised on `ι × ℕ` with heights starting at 0; `e i j t` is the number of
   elements of chain `j` below the element of chain `i` at height `t`, so the band condition
   reads `t + 1 - 2a ≤ e i j t ≤ t + 1 - a` (truncated subtraction). The finite posets of the
   note are the restrictions to heights below `ℓ`.
