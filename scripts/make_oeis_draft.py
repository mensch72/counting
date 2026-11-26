#!/usr/bin/env python3
"""Regenerate docs/oeis_submission.md from the b-files in data/."""
import os
here = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(here, '..', 'data')
def rb(name):
    d = {}
    for l in open(os.path.join(D, name)):
        if l.strip() and l[0] != '#':
            a, b = l.split(); d[int(a)] = int(b)
    return d
f, vi = rb('b006982.txt'), rb('b072361.txt')
o = ["# Draft OEIS submissions\n",
     "Drafts for a human contributor; nothing has been sent to the OEIS. `<name>` is a placeholder.\n",
     "## A006982 (unlabeled distributive lattices on n nodes)\n",
     f"- Replace the b-file by `data/b006982.txt` (n = 0..{max(f)}; currently n = 0..60).",
     "- COMMENT: a(n) is also the number of unlabeled posets with exactly n down-sets, by Birkhoff's representation theorem.",
     f"- EXTENSIONS: a(61)-a({max(f)}) (b-file) from `<name>`, computed by a transfer matrix over the rank layers of the lattice whose states are the posets of live join-irreducibles; all terms up to n = 60 agree with Kohonen (2021).\n",
     "First new terms:\n"]
o += [f"    a({n}) = {f[n]}" for n in range(61, 66)] + [f"    ...\n    a({max(f)}) = {f[max(f)]}\n"]
o += ["## A072361 (vertically indecomposable distributive lattices on n nodes)\n",
      f"- Replace the b-file by `data/b072361.txt` (n = 1..{max(vi)}; currently n = 1..49; Kohonen (2021) has n <= 60).",
      "- FORMULA: A006982(n) = Sum_{k=2..n} a(k)*A006982(n-k+1) for n >= 2.",
      f"- EXTENSIONS: a(50)-a({max(vi)}) (b-file) from `<name>`.\n",
      "First terms beyond the current b-file:\n"]
o += [f"    a({n}) = {vi[n]}" for n in range(50, 55)] + [f"    ...\n    a({max(vi)}) = {vi[max(vi)]}\n"]
if os.path.exists(os.path.join(D, 'b006981.txt')):
    m, mv = rb('b006981.txt'), rb('b342132.txt')
    o += ["## A006981 (unlabeled modular lattices on n nodes)\n",
          f"- DATA / b-file: add a(36)..a({max(m)}) (`data/b006981.txt`).",
          f"- EXTENSIONS: a(36)-a({max(m)}) from `<name>`, computed by a transfer matrix over the rank layers whose states are the posets of pairwise meets of a layer; a(0)-a(35) agree with Kohonen (2021).\n",
          "New terms:\n"]
    o += [f"    a({n}) = {m[n]}" for n in range(36, max(m) + 1)]
    o += ["\n## A342132 (vertically indecomposable modular lattices on n nodes)\n",
          f"- DATA / b-file: add a(36)..a({max(mv)}) (`data/b342132.txt`).",
          f"- EXTENSIONS: a(36)-a({max(mv)}) from `<name>`.\n", "New terms:\n"]
    o += [f"    a({n}) = {mv[n]}" for n in range(36, max(mv) + 1)]
if os.path.exists(os.path.join(D, 'b229202.txt')):
    sm = rb('b229202.txt')
    o += ["\n## A229202 (semimodular lattices on n nodes)\n",
          f"- DATA: add a(26)..a({max(sm)}).",
          f"- EXTENSIONS: a(26) from `<name>`, computed with the layer transfer matrix of the modular case without the lower semimodularity rule; a(0)-a(25) agree with Kohonen (2017).\n",
          "New terms:\n"]
    o += [f"    a({n}) = {sm[n]}" for n in range(26, max(sm) + 1)]
open(os.path.join(here, '..', 'docs', 'oeis_submission.md'), 'w').write("\n".join(o) + "\n")
print('wrote docs/oeis_submission.md')
