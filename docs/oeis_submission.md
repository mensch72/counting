# Draft OEIS submissions

These are drafts for a human contributor to submit; nothing has been sent to the OEIS.

## A006982 (unlabeled distributive lattices on n nodes)

- Replace the b-file by `data/b006982.txt` (n = 0..160; previously n = 0..60).
- LINKS: `<name>, Table of n, a(n) for n = 0..160` (terms n <= 60 from Jukka Kohonen).
- LINKS: link to this repository (method, programs, checks).
- COMMENT: a(n) is also the number of unlabeled posets with exactly n down-sets (order ideals), by Birkhoff's representation theorem.
- EXTENSIONS: a(61)-a(160) (b-file) from `<name>`, computed by a transfer matrix over the rank layers of the lattice whose states are the posets of live join-irreducibles; all terms up to n = 60 agree with Kohonen (2021).

First new terms:

    a(61) = 1398297238937456
    a(62) = 2577577210993326
    a(63) = 4751419899674101
    a(64) = 8758621005139604
    a(65) = 16145360828911176
    a(66) = 29761867322814983
    a(67) = 54862096251848441
    a(68) = 101131136719043728
    a(69) = 186422036415293546
    a(70) = 343644809421288784
    ...
    a(160) = 276215655494051950398467067725855360399901

## A072361 (vertically indecomposable distributive lattices on n nodes)

- Replace the b-file by `data/b072361.txt` (n = 1..160; previously n = 1..49; Kohonen's paper has n <= 60).
- FORMULA: A006982(n) = Sum_{k=2..n} a(k)*A006982(n-k+1) for n >= 2.
- EXTENSIONS: a(50)-a(160) (b-file) from `<name>`.

First terms beyond the current b-file:

    a(50) = 8863372090
    a(51) = 15066614003
    a(52) = 26376230858
    a(53) = 44977519230
    a(54) = 78519416987
    a(55) = 134229841861
    a(56) = 233808824537
    a(57) = 400499677825
    a(58) = 696369403331
    a(59) = 1194743684703
    a(60) = 2074408477477
    ...
    a(160) = 1079689902088453963903370538000719118
