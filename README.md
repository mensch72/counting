# Counting distributive and modular lattices by a frontier transfer matrix

This repository extends five OEIS sequences past their published records:

| sequence | meaning | previous record | here |
|---|---|---|---|
| [A006982](https://oeis.org/A006982) | unlabeled distributive lattices with n elements | n = 60 (Kohonen 2021) | n = 160 |
| [A072361](https://oeis.org/A072361) | vertically indecomposable ones | n = 49 in OEIS, n = 60 in Kohonen's paper | n = 160 |
| [A006981](https://oeis.org/A006981) | unlabeled modular lattices with n elements | n = 35 (Kohonen 2021) | n = 38 |
| [A342132](https://oeis.org/A342132) | vertically indecomposable ones | n = 35 | n = 38 |
| [A229202](https://oeis.org/A229202) | unlabeled semimodular lattices with n elements | n = 25 (Kohonen 2017) | n = 26 |

The same idea, with a different frontier, also reproduces and extends the
modular lattices ([A006981](https://oeis.org/A006981), record n = 35); see the
section "Modular lattices" below for those results.

The tables are `data/b006982.txt` and `data/b072361.txt`. First new terms:

    A006982(61) = 1398297238937456
    A006982(62) = 2577577210993326
    A006982(63) = 4751419899674101

    A006981(36) = 681357605302
    A006981(37) = 1647135247659
    A006981(38) = 3985106742170   (from the N = 38 run only; not confirmed by a run with larger N)
    A229202(26) = 13759007833

The values are computed, not proved; see "Checks" for what supports them.
A write-up is in `paper/paper.tex` (`paper/paper.pdf`).

## Why the old methods stop at 60

All earlier counts *generate* lattices one by one and reject isomorphs
(Erné–Heitzig–Reinhold 2002 to n = 49; Kohonen 2021 to n = 60, generating only the
lattices that are not vertical 2-sums). The cost grows like the number of
objects: Kohonen reports 17.2 core-days for n = 60 alone, ×1.66 per extra element.

## The method

By Birkhoff's theorem a distributive lattice with n elements is the lattice
J(P) of down-sets of a poset P with exactly n down-sets. Layer r of J(P) is the
set S_r of down-sets of size r, so n = Σ_r |S_r|.

Build P from the bottom. Let X_r = {x : |↓x| ≤ r}, the elements "born" before
rank r. Call x ∈ X_r *dead* if it lies in every down-set of size r, *live*
otherwise. Let Λ be X_r restricted to the live elements and ρ = r − #dead. Then:

1. S_r ↔ down-sets of Λ of size ρ (dead elements are in all of them).
2. The elements born at rank r are new maximal elements whose down-set is
   Dead ∪ J for a ρ-down-set J of Λ. Several may share the same J.
3. Dead elements lie below everything born later. So everything above rank r
   depends on (Λ, ρ) alone: the **frontier**.
4. |↓x| is an isomorphism invariant, so isomorphisms respect the filtration
   X_0 ⊆ X_1 ⊆ …. Two extensions of X_r are isomorphic iff their birth vectors
   (m_J) differ by an element of Γ = image of Aut(X_r) in Aut(Λ).

Hence the number of isomorphism classes is the number of weighted paths in an
automaton whose states are triples (Λ, ρ, Γ), a step being a Γ-orbit of birth
vectors, and the weight of a state being its layer size. A lattice is
vertically indecomposable iff the path never returns to the empty frontier
before the top, and

    f(n) = Σ_{k=2..n} vi(k) · f(n−k+1).

No lattice is ever generated: all lower parts with the same frontier are merged
into one counter. A frontier is small wherever the lattice is thin, and thin
lattices are the overwhelming majority, so the state count grows far more slowly
than the number of lattices:

| N | states | time (1 core) | memory |
|---|---|---|---|
| 60 | 4.5·10³ | 0.1 s | – |
| 100 | 1.9·10⁵ | 9 s | – |
| 120 | 9.7·10⁵ | 41 s | 0.4 GB |
| 150 | 8.8·10⁶ | 7.5 min | 3.9 GB |
| 160 | 1.75·10⁷ | 16 min | 7.9 GB |

States grow by about ×2.1 per 10 elements; the lattices themselves by ×450.
A state is kept only if it can still be completed within N elements (the forced
remaining weight is the number of down-sets of Λ larger than ρ, which is exact).

## Checks

1. **Known terms.** All 61 terms of A006982 (n = 0..60), all 49 terms of A072361
   in the OEIS, and the values of A072361 for n = 50..60 printed in Kohonen
   (2021), Table 2, are reproduced from scratch (`scripts/assemble.py` asserts this).
2. **Brute force beyond 60.** `src/brute_rank.cpp` reads all 49 519 391 posets on
   ≤ 11 points from nauty's `genposetg`, and tabulates the vertically
   indecomposable ones by (number of down-sets, number of points). The DP,
   refined by the number of layers, agrees in all 443 cells with n ≤ 110;
   192 of those cells (25 179 538 lattices) have n > 60.
3. **Duality.** The DP is bottom-up and not manifestly self-dual. The number of
   v.i. lattices with n elements, a atoms and b coatoms must be symmetric in
   (a, b). `scripts/check_dual.py` asserts this for every cell up to the full N.
4. **Planar case.** Restricted to posets of width ≤ 2 the automaton has only 23
   states. Its counts agree for every n ≤ 160 with an independent count of
   regions between two lattice paths (`scripts/planar_check.py`). This tests
   the long, thin regime that brute force cannot reach.
5. **Two implementations.** `src/frontier.cpp` (reference, `unordered_map`,
   nauty for every canonical form) and `src/frontier2.cpp` (compact, hashed
   invariants with nauty as fallback) agree for all n ≤ 120.
6. **Runs with different N** (120, 150, 160) agree on their common range,
   although the pruning depends on N.
7. **Guards.** The programs abort rather than continue on counter overflow
   (160 bits), more than 32 live elements, or a layer wider than 64.

What is not covered: for n > 110 and width ≥ 3 the checks are duality and
agreement between runs with different N, not an independent method. An
independent recomputation would be welcome.

## Modular lattices (A006981, A342132)

`src/modular.cpp` applies the same idea to modular lattices. A finite lattice
is modular iff it is upper and lower semimodular, and such lattices are graded,
so the lattice can again be built layer by layer.

*State.* Let T = L_r be the top layer of the lower part, and
Y = {a ∧ b : a, b ∈ T} with its order, the elements of rank r−1 marked. Call
a, b ∈ T adjacent if a ∧ b has rank r−1.

*Step.* The next layer is a family of sets D_c ⊆ T (the lower covers of the new
elements c) such that

1. the D_c with |D_c| ≥ 2 partition the adjacent pairs into cliques
   (the two semimodularity conditions),
2. every element of T lies in some D_c (graded),
3. for all c ≠ d the set {a ∧ b : a ∈ D_c, b ∈ D_d} has a maximum (it is c ∧ d;
   this makes the result a lattice).

The new Y′ consists of the new layer and these maxima, so everything is local
to (Y, marks). The symmetry group Γ is stored as twin classes (on which Γ acts
as the full symmetric group) plus an explicit list of the remaining elements;
this matters because modular lattices contain large M_k's.

*Pruning.* A frontier is dropped if it cannot be completed within N elements.
Two lower bounds are used:

- the adjacency graph of a layer has diameter Δ equal to the number of layers
  still needed, and layer j above must contain a set of elements with pairwise
  distance > j;
- **duality**: rank(a ∨ b) − r = r − rank(a ∧ b) = distance of a and b in the
  adjacency graph. The part of the lattice above a layer is, upside down, a
  lower part of the dual modular lattice with the same distance matrix. So a
  frontier needs at least as many further elements as the smallest lower part
  seen so far with the same distance profile (the DP runs in increasing weight,
  so "first seen" is "smallest"). This removes about three quarters of the
  states.

Enumerating the clique partitions (linear spaces) is the expensive part; partial
partitions are rejected up to isomorphism, and de Bruijn–Erdős and pair-counting
bounds cut the search.

*Cost.* One core, under 2 GB:

| N | states | time |
|---|---|---|
| 30 | 3.7·10⁴ | 47 s |
| 32 | 8.4·10⁴ | 2.7 min |
| 35 | 3.0·10⁵ | 19 min |
| 36 | 4.5·10⁵ | 37 min |
| 37 | 6.9·10⁵ | 73 min |
| 38 | 1.06·10⁶ | 142 min |

For comparison, Kohonen (2021) reports 63 core-days for n = 35 alone.

*Checks.* `scripts/assemble_mod.py` asserts: all known terms of A006981 (n ≤ 35)
and A342132; symmetry of the (atoms, coatoms) table; agreement between runs with
different N (the pruning depends on N, and the largest n of each run is computed
with no slack). In addition, `modular N file dist` restricts the same program to distributive
lattices (no interval of length 2 with three atoms). Its output equals that of
the distributive DP above for every n ≤ 40 (`runs/moddist_*.txt`): two programs
with different states, symmetry handling and pruning agree, including at
budgets N = 36, 38, 40 where the last term is computed with no slack.

There is no independent second method for the non-distributive modular
lattices with n > 35; the new terms rest on the checks above.

## Semimodular and geometric lattices (A229202, A281574)

`src/layers.cpp` is `modular.cpp` with the class as a parameter. The proof that the
frontier (pairwise meets of the top layer) suffices does not use modularity: "graded"
and "meet-semilattice" are separate conditions, and the two semimodularity rules are
the two directions of rule 1. So `layers N - usm` counts (upper) semimodular lattices,
`lsm` the dual class, `graded` all graded lattices, `geometric` the atomistic
semimodular ones. The modularity-based pruning is switched off in these modes.

- **Semimodular:** works well from the bottom. N = 24 needs 8.9·10⁵ states for about
  1.5·10⁹ lattices; N = 26 took 69 min and 7.9 GB (5.9·10⁶ states) and gives one new
  term. Memory is the limit. Checks: known terms to n = 25, runs with N = 24, 25, 26,
  and equality with the dual route (`lsm`) for n ≤ 16 (`scripts/assemble_layers.py`,
  `runs/lay_lsm_16.txt`).
- **Geometric:** known terms reproduced to n = 35, but no advantage: the frontier is
  essentially the whole lattice, so this is plain generation. Not extended.
- **Graded, and the dual directions:** far too many families or states; not competitive.

## Reproduce

Needs g++ and nauty (`apt-get install nauty libnauty-dev`).

    cd src
    g++ -O2 -march=native -o frontier  frontier.cpp  -lnauty
    g++ -O2 -march=native -o frontier2 frontier2.cpp -lnauty
    g++ -O2 -o brute_rank brute_rank.cpp
    ./frontier 60                       # n, vi(n), f(n): 0.1 s
    ./frontier2 160 > ../runs/vi_160.txt
    python3 ../scripts/assemble.py ../runs/vi_160.txt      # b-files + check of known terms
    for t in 1 2 3 4 5 6 7; do ./frontier2 160 $t > ../runs/dual_160_t$t.txt; done
    python3 ../scripts/check_dual.py ../runs/vi_160.txt ../runs/dual_160_t*.txt
    ./frontier2 160 0 2 > planar.txt && python3 ../scripts/planar_check.py 160 planar.txt
    # modular lattices
    g++ -O2 -march=native -o modular modular.cpp -lnauty
    ./modular 36 ../runs/mod_dual_36.txt > ../runs/mod_36.txt      # 37 min
    python3 ../scripts/assemble_mod.py ../runs/mod_35.txt ../runs/mod_36.txt ../runs/mod_37.txt
    ./modular 40 /dev/null dist > ../runs/moddist_40.txt           # distributive cross-check
    # brute-force check
    for k in 1 2 3 4 5 6 7 8 9 10 11; do nauty-genposetg $k t q; done | ./brute_rank 110 > brute.txt
    ./frontier 110 rank > rank.txt      # compare "n k count" with "n k 0 count"

## Files

- `src/frontier.cpp`: reference DP, with the `dual` and `rank` refinements.
- `src/frontier2.cpp`: production DP.
- `src/brute_rank.cpp`: brute-force tabulation for check 2.
- `src/modular.cpp`: frontier DP for modular lattices.
- `src/layers.cpp`: the same program for semimodular, geometric and graded lattices.
- `src/explore.cpp`: an abandoned first attempt (generating prime posets for a
  modular-decomposition count); kept because it shows why generation does not
  scale: the number of prime posets with n down-sets still grows like 1.64^n.
- `scripts/assemble.py`, `scripts/check_dual.py`, `scripts/planar_check.py`: assembly and checks.
- `docs/oeis_submission.md`: draft text for the OEIS edits (not submitted).
- `paper/`: the write-up (`paper.tex`, `paper.pdf`); `scripts/make_tables.py` regenerates its tables from `data/`.
- `data/`: the new b-files, and the OEIS b-files used as reference.
- `runs/`: raw outputs and logs.

## References

- M. Erné, J. Heitzig, J. Reinhold, *On the number of distributive lattices*,
  Electron. J. Combin. 9 (2002), R24.
- J. Kohonen, *Cartesian lattice counting by the vertical 2-sum*, Order (2021),
  arXiv:2007.03232.
- B. D. McKay, A. Piperno, *Practical graph isomorphism, II*, J. Symbolic Comput.
  60 (2014), 94–112 (nauty).
