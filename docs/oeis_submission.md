# Draft OEIS submissions

Drafts for a human contributor; nothing has been sent to the OEIS. `<name>` is a placeholder.

## A006982 (unlabeled distributive lattices on n nodes)

- Replace the b-file by `data/b006982.txt` (n = 0..160; currently n = 0..60).
- COMMENT: a(n) is also the number of unlabeled posets with exactly n down-sets, by Birkhoff's representation theorem.
- EXTENSIONS: a(61)-a(160) (b-file) from `<name>`, computed by a transfer matrix over the rank layers of the lattice whose states are the posets of live join-irreducibles; all terms up to n = 60 agree with Kohonen (2021).

First new terms:

    a(61) = 1398297238937456
    a(62) = 2577577210993326
    a(63) = 4751419899674101
    a(64) = 8758621005139604
    a(65) = 16145360828911176
    ...
    a(160) = 276215655494051950398467067725855360399901

## A072361 (vertically indecomposable distributive lattices on n nodes)

- Replace the b-file by `data/b072361.txt` (n = 1..160; currently n = 1..49; Kohonen (2021) has n <= 60).
- FORMULA: A006982(n) = Sum_{k=2..n} a(k)*A006982(n-k+1) for n >= 2.
- EXTENSIONS: a(50)-a(160) (b-file) from `<name>`.

First terms beyond the current b-file:

    a(50) = 8863372090
    a(51) = 15066614003
    a(52) = 26376230858
    a(53) = 44977519230
    a(54) = 78519416987
    ...
    a(160) = 1079689902088453963903370538000719118

## A006981 and A342132 (modular lattices): nothing new to submit

- The OEIS entries stop at n = 35, but J. Kohonen, arXiv:2311.16643 (2023), Table 1, gives both sequences for n <= 40.
- The transfer matrix here reproduces n <= 38 and agrees with that table. The entries should be extended from Kohonen's paper, not from this computation.


## A229202 (semimodular lattices on n nodes)

- DATA: add a(26)..a(27).
- EXTENSIONS: a(26)-a(27) from `<name>`, computed with the layer transfer matrix of the modular case without the lower semimodularity rule; a(0)-a(25) agree with Kohonen (2017).

New terms:

    a(26) = 13759007833
    a(27) = 49997352868

## A368461 (planar modular lattices on n nodes)

- b-file: `data/b368461.txt` (n = 1..1000; currently n = 1..34).
- FORMULA / COMMENT: every planar modular lattice is a planar distributive lattice with eyes inserted into covering squares (Graetzer and Quackenbush, 2010); with the lattice-path description of planar distributive lattices and Burnside's lemma for the mirror symmetry this gives a(n) for all n (see scripts/planar_modular.py).
- EXTENSIONS: a(35)-a(1000) from `<name>`. Note: the method combines Kohonen (arXiv:2311.16643) and the path count of A345734 (Howroyd); cite both.

First new terms:

    a(35) = 126716031349
    a(36) = 292487244620
    a(37) = 675272703814
    a(38) = 1559330151206
    a(39) = 3601426216069
    a(40) = 8319180224765

## A072407 (canonically 2-indecomposable posets with n antichains)

- b-file: `data/b072407.txt` (n = 1..160; currently n = 1..49).
- FORMULA: A072361(k) = Sum_{j=0..k-1} a(k-j)*A072361(j) for k > 1, with A072361(0) = 1 (Erne, Heitzig, Reinhold, Corollary 7).
- EXTENSIONS: a(50)-a(160) from `<name>`, using the extension of A072361.

First new terms:

    a(50) = 2732626377
    a(51) = 4641069763
    a(52) = 8002548246
    a(53) = 13615245266
    a(54) = 23440714169

## A186808 (n such that A006982(n) is prime)

- DATA: 4, 5, 6, 10, 12, 13, 18, 21, 23, 26, 66, 88.
- EXTENSIONS: a(11)-a(12) from `<name>`; there are no further terms up to n = 160. Primality proved with PARI/GP.
