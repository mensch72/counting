# Counting distributive lattices by a frontier transfer matrix

This repository extends two OEIS sequences well past their published records:

| sequence | meaning | previous record | here |
|---|---|---|---|
| [A006982](https://oeis.org/A006982) | unlabeled distributive lattices with n elements | n = 60 (Kohonen 2021) | n = 160 |
| [A072361](https://oeis.org/A072361) | vertically indecomposable ones | n = 49 in OEIS, n = 60 in Kohonen's paper | n = 160 |

The tables are `data/b006982.txt` and `data/b072361.txt`. First new terms:

    A006982(61) = 1398297238937456
    A006982(62) = 2577577210993326
    A006982(63) = 4751419899674101

The values are computed, not proved; see "Checks" for what supports them.

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
| 160 | see `runs/runs.log` | | |

States grow by about ×2.1 per 10 elements; the lattices themselves by ×445.
A state is kept only if it can still be completed within N elements (the forced
remaining weight is the number of down-sets of Λ larger than ρ, which is exact).

## Checks

1. **Known terms.** All 61 terms of A006982 (n = 0..60) and all 49 of A072361 are
   reproduced from scratch (`scripts/assemble.py` asserts this).
2. **Brute force beyond 60.** `src/brute_rank.cpp` reads all 49 519 391 posets on
   ≤ 11 points from nauty's `genposetg`, and tabulates the vertically
   indecomposable ones by (number of down-sets, number of points). The DP,
   refined by the number of layers, agrees in all 443 cells with n ≤ 110;
   192 of those cells (25 179 538 lattices) have n > 60.
3. **Duality.** The DP is bottom-up and not manifestly self-dual. The number of
   v.i. lattices with n elements, a atoms and b coatoms must be symmetric in
   (a, b). `scripts/check_dual.py` asserts this for every cell up to the full N.
4. **Two implementations.** `src/frontier.cpp` (reference, `unordered_map`,
   nauty for every canonical form) and `src/frontier2.cpp` (compact, hashed
   invariants with nauty as fallback) agree for all n ≤ 120.
5. **Guards.** The programs abort rather than continue on counter overflow
   (160 bits), more than 32 live elements, or a layer wider than 64.

What is not covered: for n > 110 the only checks are duality and agreement
between runs with different N. An independent recomputation would be welcome.

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
    # brute-force check
    for k in 1 2 3 4 5 6 7 8 9 10 11; do nauty-genposetg $k t q; done | ./brute_rank 110 > brute.txt
    ./frontier 110 rank > rank.txt      # compare "n k count" with "n k 0 count"

## Files

- `src/frontier.cpp`: reference DP, with the `dual` and `rank` refinements.
- `src/frontier2.cpp`: production DP.
- `src/brute_rank.cpp`: brute-force tabulation for check 2.
- `src/explore.cpp`: an abandoned first attempt (generating prime posets for a
  modular-decomposition count); kept because it shows why generation does not
  scale: the number of prime posets with n down-sets still grows like 1.64^n.
- `scripts/assemble.py`, `scripts/check_dual.py`: assembly and checks.
- `data/`: the new b-files, and the OEIS b-files used as reference.
- `runs/`: raw outputs and logs.

## References

- M. Erné, J. Heitzig, J. Reinhold, *On the number of distributive lattices*,
  Electron. J. Combin. 9 (2002), R24.
- J. Kohonen, *Cartesian lattice counting by the vertical 2-sum*, Order (2021),
  arXiv:2007.03232.
- B. D. McKay, A. Piperno, *Practical graph isomorphism, II*, J. Symbolic Comput.
  60 (2014), 94–112 (nauty).
