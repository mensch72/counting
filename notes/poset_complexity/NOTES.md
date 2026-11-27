# Counting labelled posets below the 2^(n²/4) barrier: working notes

Status: AI-assisted. Full proofs are in `proof.pdf`; this file is the earlier overview.
The algorithm (Section 3) is a proof sketch and has been checked numerically
for n ≤ 5. Nothing here has been checked by a human.

L(n) is the number of partial orders on {1,…,n}; L(n) = 2^(n²/4 + o(n²)).
Generating all posets costs at least L(n). The claim is

**Claim.** L(n) can be computed in time 2^(c n² + O(n log n)) with
c = 2(5 − 2√6) ≈ 0.2021 < 1/4.

No lower bound is known for this problem; whether counting with a transitivity
axiom is tractable is an open problem in first-order model counting
(Beame, Van den Broeck, Gribkoff, Suciu, PODS 2015).

## 1. A contractible poset of wide down-sets

P is a finite poset, J(P) its lattice of down-sets, max(I) the set of maximal
elements of I. Antichains correspond to down-sets by N ↦ ↓N, I ↦ max(I).
For k ≥ 1 let

    J_k(P) = { I ∈ J(P) : |max(I)| ≥ k },   ordered by inclusion.

J_k(P) is non-empty iff width(P) ≥ k.

**Lemma 1.** |max(I₁ ∪ I₂)| + |max(I₁ ∩ I₂)| ≥ |max I₁| + |max I₂|.

*Proof.* Let A = max I₁, B = max I₂. Then max(I₁ ∪ I₂) is the set of maximal
elements of A ∪ B. An element of A ∪ B that is not maximal in A ∪ B, say
a ∈ A with a < b ∈ B, lies in I₁ ∩ I₂ and is maximal there, because it is
maximal in I₁. An element of A ∩ B is maximal in both I₁ ∪ I₂ and I₁ ∩ I₂.
So the left side is at least |A ∪ B| + |A ∩ B|. ∎

**Lemma 2.** If width(P) ≥ k, the order complex of J_k(P) is contractible.
Hence the signed number of chains I₀ ⊂ … ⊂ I_r in J_k(P), with sign (−1)^r,
is 1 if width(P) ≥ k and 0 otherwise.

*Proof.* Let A* be an antichain of maximum size w and I* = ↓A*. For I ∈ J_k,
Lemma 1 and |max(I ∩ I*)| ≤ w give |max(I ∪ I*)| ≥ |max I| ≥ k. So
f(I) = I ∪ I* is a closure operator on J_k(P). Its image has the least
element I*, so it is a cone, and a closure operator is a homotopy equivalence
onto its image. ∎

Numerical check: Euler characteristic 1 for all labelled posets on ≤ 5 points
and all k ≤ width (`test_euler_char.py`, 10 833 cases).

## 2. Inserting an antichain in product form

Let Q be a poset and A a down-set of Q. A *type* is a pair (D, U) with D a
down-set of Q inside A, U an up-set of Q inside Q∖A, and d < u for all
d ∈ D, u ∈ U. Adding new pairwise incomparable elements x₁,…,x_j with
↓x_i∖x_i = D_i and ↑x_i∖x_i = U_i gives a poset for every choice of types,
because D_i ⊆ A and U_{i'} ⊆ Q∖A never meet. Without the cut A the choices
are not independent (x below q below x' would force x < x'); an early version
of the formula missed this and failed the test at n = 3.

The condition "A = ↓M ∖ M", i.e. every maximal element of A lies below some
x_i, is handled by inclusion–exclusion over the uncovered subset of max(A).

## 3. The algorithm (sketch)

By Lemma 2,

    #{P on [n] : width(P) ≥ k} = Σ_P Σ_{flags} (−1)^r,

where a flag is a chain N₀ ≺ … ≺ N_r of antichains of size ≥ k
(N ≺ N' iff ↓N ⊊ ↓N'). Remove the top antichain M = N_r, with j = |M| ≥ k:

- core Q = P ∖ M on n − j points, with the cut A = ↓M ∖ M;
- each lower antichain is N_i = E_i ∪ {x ∈ M : b(x) ≤ i}, where E_i ⊆ A is an
  antichain of Q and b(x) is the first index with x ∈ N_i (an element of M
  that lies in N_i lies in N_{i+1}, …, N_r);
- conditions on x that depend only on its type and b(x): x is incomparable to
  E_i for all i ≥ b(x);
- covering conditions, handled by inclusion–exclusion over a subset Z of core
  elements: every maximal element of A is below some x; every e ∈ E_i that is
  not below an element of E_{i+1} is below some x with b(x) ≤ i + 1
  (each core element is "needy" at most once);
- size and strictness conditions |N_i| ≥ k, N_i ≠ N_{i+1}: these depend only
  on the numbers of x with each birth index, and are handled by a small
  dynamic programme with multinomial weights.

For fixed core data the count is a sum over Z of products of powers of type
counts. Per core there are at most 2^(O(n log n)) choices of (A, E₀,…,E_{r−1}, Z)
and at most 4^n types. So

    cost(width ≥ k) = Σ_{j ≥ k} L(n − j) · 2^(O(n log n)) = 2^((n−k)²/4 + O(n log n)).

Posets of width < k: a poset of width w is a union of w chains, and the order
between two chains of lengths a and b is given by two monotone staircases, at
most 2^(a+b) each way. So there are at most 2^(2kn + O(n log n)) such posets,
and they can be listed and de-duplicated in that time (and space).

With k = αn the total is 2^(max((1−α)²/4, 2α) n² + O(n log n)). The two terms
balance at α = 5 − 2√6 ≈ 0.1010, which gives c ≈ 0.2021.

Numerical check: the formula reproduces #{P : width ≥ k} for all n ≤ 4 and
all k, and for n = 5, k = 3, 4, 5 (`test_flag_formula.py`).

## 4. What is not done

- A written proof of Section 3 (in particular that the parametrisation of
  flags by core data, types and birth indices is a bijection).
- Unlabelled posets. An equivariant version (Lefschetz numbers on the same
  complex) should exist but has not been worked out.
- The constant. The bound 2^(2kn) for narrow posets is crude, and flags may be
  replaceable by a smaller complex; both would lower c.
- Practical value. The overhead 2^(O(n log n)) dominates for n ≈ 20, so this is
  a complexity statement, not a route to new terms.
- Literature. Lemma 2 may be known (it generalises Dilworth's lattice of
  maximum antichains); no search has been done.

## 5. Other identities found on the way

- **Balanced cut** (`test_cut_identity.py`): for every poset and every level
  1 ≤ m ≤ n, Σ (−1)^(|S|−1) = 1 over pairs (I, S) with I a down-set,
  ∅ ≠ S ⊆ max(I), |I| − |S| < m ≤ |I|. For m = 1 this is Robinson's
  inclusion–exclusion. An unlabelled version holds with orbits whose
  stabiliser acts oddly on S dropped. Checked for all posets on ≤ 6 points.
- **Threshold** (`test_threshold_and_cubes.py`): if C(P) is a canonical
  antichain with local membership (e.g. the minimal elements), then
  #{P : |C(P)| ≥ k} = Σ_{j ≥ k} (−1)^(j−k) C(j−1, k−1) #{(P, M) : M ⊆ C(P), |M| = j}.
  This does not give a better exponent: adding a chain of 1/α points to a
  typical three-level poset makes every level smaller than αn.
- The cube complex of J_k(P) (single-element removals only) is *not*
  contractible; the complete bipartite poset K_{2,2} with k = 2 is a
  counterexample. The order complex is needed.
