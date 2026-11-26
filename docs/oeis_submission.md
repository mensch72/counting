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

## A006981 (unlabeled modular lattices on n nodes)

- DATA / b-file: add a(36)..a(38) (`data/b006981.txt`).
- EXTENSIONS: a(36)-a(38) from `<name>`, computed by a transfer matrix over the rank layers whose states are the posets of pairwise meets of a layer; a(0)-a(35) agree with Kohonen (2021).

New terms:

    a(36) = 681357605302
    a(37) = 1647135247659
    a(38) = 3985106742170

## A342132 (vertically indecomposable modular lattices on n nodes)

- DATA / b-file: add a(36)..a(38) (`data/b342132.txt`).
- EXTENSIONS: a(36)-a(38) from `<name>`.

New terms:

    a(36) = 90998884153
    a(37) = 218856768070
    a(38) = 526836817969

## A229202 (semimodular lattices on n nodes)

- DATA: add a(26)..a(27).
- EXTENSIONS: a(26)-a(27) from `<name>`, computed with the layer transfer matrix of the modular case without the lower semimodularity rule; a(0)-a(25) agree with Kohonen (2017).

New terms:

    a(26) = 13759007833
    a(27) = 49997352868
